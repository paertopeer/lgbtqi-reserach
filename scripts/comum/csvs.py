import pandas as pd
import pymongo

connection_string = f"mongodb+srv://pvfcosta:dsh2023.retorno@ti6-lbtqia-research.bdfqdy0.mongodb.net/test"

client = pymongo.MongoClient(connection_string)

mydb = client['ti-data']

for name in mydb.list_collection_names():
    connection = mydb[name]
    cursor = connection.find()
    df = pd.DataFrame(list(cursor))
    csv_file_name = 'C:/Projetos/plf-es-2023-1-ti6-3150100-analise-populacao-lgbt-github/Instrumentos/Codigos/outputs/csv/' + name +'.csv'
    df.to_csv(csv_file_name, index=False, sep=';')
    print(name)