# twitter-covid19br
Arquivos relacionados ao projeto de análise de sentimentos dos tweets da quarentena

O arquivo _twitter-scrapper.py_ foi criado por mim e pelo Andrei (aluno no IFT-SP). Ele é o código do scrapper de dados do twitter, que utiliza como base a API do twitter. Infelizmente essa API possui algumas limitações, como um número limite de requisições num certo período de tempo, o que acaba por limitar a análise do numero real de tweets.

O arquivo _tweets-cleaner.py_ eu escrevi com o intuito de automatizar o processo de limpeza dos tweets e obtenção de algumas informações chaves, como a distribuição dos tweets por estado e a contagem de palavras.

Os arquivos Jupyter Notebooks (com final .ipynb), possuem alguns dos workflows realizados para treino das redes neurais.

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

Ao total foram 10.953 tweets classificados manualmente, para serem utilizados como dados de treino e testes.

Quanto à rede neural, ainda não consegui obter uma rede satisfatória, capaz de classificar ao menos 50% dos sentimentos negativos e positivos, apesar da acurácia total ser acima de 50% (note que os dados de tweets tendem a possuir um número muito maior de sentimentos neutros, em comparação aos outros sentimentos separadamente -- ver o arquivo _Twitter-LSTM-sentiment-analysis.ipynb_).

Esses arquivos não possuem a intenção de serem utilizados para deploy e o projeto ainda está em andamento. Os próximos passos seriam: analisar como a diminuição dos dados de treinamento afeta na acurácia, para então se ter uma ideia de quantos dados a mais de treinamento são necessários, e implementar um grid search nos parâmetros da rede. 

Espero que os arquivos deste repositório possam ser úteis para você.


Laís Alves | Universidade de Brasília | Brasil
