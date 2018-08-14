### Script para análise de movimentação de estoque

O script neste repositório admite como entrada dois arquivos (no formato .xlsx) contendo dados da movimentação de entrada e saídas de um sistema de estoque, são eles:

* MovtoITEM.xlsx
* SaldoITEM.xlsx

As dependicas para esta solução são as bibliotecas *numpy* e *pandas*, caso o ambiente em que este script será executado não possua estas dependencias as dependências podem ser adicionadas com o pip
```shell
    $ pip install numpy
    $ pip install pandas
```

Tendo as dependencias instaladas, certifique-se que os arquivos de entrada se encontrem na pasta pasta do script e execute

```shell
    $ python base.py
```

A saída do script será escrita no arquivo *resultado.xlsx*