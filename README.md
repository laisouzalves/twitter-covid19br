# twitter-covid19br
Arquivos relacionados ao projeto de análise de sentimentos dos tweets da quarentena

O arquivo _twitter-scrapper.py_ foi criado por mim e pelo Andrei (aluno no IFT-SP). Ele é o código do scrapper de dados do twitter, que utilia como base a API do twitter. Infelizmente essa API possui algumas limitações, como um número limite de requisições num período de tempo, o que acaba por limitar a análise do numero real de tweets.

O arquivo _tweets-cleaner.py_ eu escrevi para automatizar o processo de limpeza dos tweets e obtenção de algumas informações chaves, como a distribuição dos tweets por estado e a contagem de palavras.

Os arquivos Jupter Notebooks (com final .ipynb), possuem alguns dos workflows realizados para treino das redes neurais.

O dataset que fizemos para o treino dessa rede neural é o arquivo _twitter_data.py_. Nele selecionamos tweets dos dias entre 18 e 23 de Março e qualificamos em 1 (negativo), 2 (neutro) ou 3 (positivo), de acordo com a tabela:

|1. Negativo |2. Neutro |3. Positivo |
|:---|:---|:---|
| Sarcasmo ou ironias negativas | Conselhos ou "dicas" | Preocupações positivas (_e.g._, desejar o bem) |
| Reclamações | Propagandas | Otimismo |
| Ameaças | Questionamentos | Paz |
| Tristeza | Reflexões | Excitação |
| Indignação | Curiosidades | Esperança |
| Raiva | Comentários pensativos | Piadas de "bom humor" |
| Críticas negativas | Rotina | Felicidade |
| Tédio | | Sarcasmo ou Ironias positivas |
| Pessimismo | | Gratidão |
| Preocupações negativas | | Sonhos |
| | | Campanhas à favor da quarentena |

Esses arquivos não possuem a intenção de serem utilizados para deploy e o projeto ainda está em andamento.

Espero que os arquivos aque possam ser úteis para você.


Laís Alves | Universidade de Brasília | Brasil
