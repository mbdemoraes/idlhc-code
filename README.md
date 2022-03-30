# idlhc-code
Implementação em Python do algoritmo _Iteractive Discrete Latin Hypercube_ (IDLHC), com base no artigo: 

von Hohendorff Filho, J.C., Maschio, C. & Schiozer, D.J. Production strategy optimization based on iterative discrete Latin hypercube. J Braz. Soc. Mech. Sci. Eng. 38, 2473–2480 (2016). https://doi.org/10.1007/s40430-016-0511-0
## Depêndencias ##

O arquivo idlhc_env.yml contém as dependências necessárias (e algumas outras) para execução deste projeto.

Em um terminal conda, use o seguinte comando para criar um ambiente virtual com base no arquivo de dependências:

```
conda env create --file idlhc_env.yml
```
## Função de teste ##

O arquivo main.py contém um exemplo de aplicação em um problema combinatório binário chamado "OneMax", cujo objetivo
é a maximização da quantidade de elementos com valor 1 no vetor de decisão.
