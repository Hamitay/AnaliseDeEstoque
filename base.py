import pandas as pd
import numpy as np
from constants import *

def load_input():
    '''
        Carrega base de dados e retorna
        como tupla de dataframes
    '''

    print('Carregando base de dados. Isto pode levar alguns segundos...')
    mvto_df = pd.read_excel(BASE_MVTO)
    saldo_df = pd.read_excel(BASE_SALDO)

    print('Base de dados carregadas!')
    return (mvto_df, saldo_df)

def create_output_dataframe(mvto_df, saldo_df):
    '''
        Cria um novo dataframe com as informacoes de movimentacao diaria por item
    '''
    #Lista com todos os itens
    itens = saldo_df[ITEM]
    
    #Lista com todos os dataframes processados
    #Os dataframes serao processados item por item
    df_parciais = []

    #Separamos o dataframe por tipo de itens
    for item in itens:
        mvto_filtrado = mvto_df.loc[mvto_df[ITEM] == item]

        #Informacoes iniciais do item
        info_item = saldo_df.loc[saldo_df[ITEM] == item]

        qnt_item = float(info_item[QT_INICIO])
        saldo_inicio = float(info_item[VAL_INICIO])

        #Funcao auxiliar para o processamento de cada linha do dataframe
        def cnt_tipo(row):
            nonlocal qnt_item, saldo_inicio

            qnt_ent = 0
            qnt_sai = 0
            val_ent = 0
            val_sai = 0
            qnt_anterior = qnt_item
            saldo_anterior = saldo_inicio
            nome_item = str(row[ITEM])
            data_transacao = row[DT_LAN]
            val_transacao = float(row[VAL])
            qnt_transaco = float(row[QTD])

            if row[TP_MOVT] == ENTRADA:
                qnt_ent=1
                qnt_item += qnt_transaco
                val_ent += val_transacao
                saldo_inicio += val_transacao
            else:
                qnt_sai=1
                qnt_item -= qnt_transaco
                val_sai += val_transacao
                saldo_inicio -= val_transacao

            saldo_final = saldo_inicio
            qnt_final = qnt_item
            return pd.Series({
                ITEM: nome_item, 
                DT_LAN: data_transacao, 
                LAN_ENT_QNT: qnt_ent, 
                LAN_ENT_VAL: val_ent,
                LAN_SAI_QNT: qnt_sai,
                LAN_SAI_VAL: val_sai,
                SLD_INICIO_VAL: saldo_anterior,
                SLD_FIM_VAL: saldo_final,
                SLD_INICIO_QNT: qnt_anterior,
                SLD_FIM_QNT: qnt_final
                })

        #Funcoes auxiliares para a agregacao no processo de downsampling
        get_last = lambda a: a[-1] if len(a) > 0 else np.nan
        get_first = lambda a: a[0] if len(a) > 0 else np.nan

        #Downsampling diarios
        output = mvto_filtrado.apply(cnt_tipo, axis=1).set_index(DT_LAN).resample('1D').agg({
            ITEM: get_last,
            LAN_ENT_QNT: np.sum,
            LAN_SAI_QNT: np.sum,
            LAN_ENT_VAL: np.sum,
            LAN_SAI_VAL: np.sum,
            SLD_INICIO_VAL: get_first,
            SLD_FIM_VAL: get_last,
            SLD_INICIO_QNT: get_first,
            SLD_FIM_QNT: get_last,
        }).dropna()

        df_parciais.append(output)

    #Concatenamos e ordenamos por data todos os dataframes processados
    df_total = pd.concat(df_parciais).sort_index()

    return df_total

def write_df_to_xlsx(df):
    '''
        Escreve dataframe para um arquivo do excel
    '''

    print('Iniciando processo de escrita')
    writer = pd.ExcelWriter(OUTPUT_FILE, datetime_format= DATE_FORMAT)
    df.to_excel(writer, 'Sheet1')
    writer.save()

    print('Processo de escrita finalizado, no output:'+OUTPUT_FILE)

if __name__ == '__main__':
    #Carrega dados
    inputs = load_input()
    mvto_df, saldo_df = inputs[0], inputs[1]
    
    #Processa dados
    df_output = create_output_dataframe(mvto_df, saldo_df)

    #Escreve dados em excel
    write_df_to_xlsx(df_output)