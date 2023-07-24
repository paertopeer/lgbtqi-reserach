import pymongo
import matplotlib.pyplot as plt
import re

connection_string = f"mongodb+srv://pvfcosta:dsh2023.retorno@ti6-lbtqia-research.bdfqdy0.mongodb.net/test"

client = pymongo.MongoClient(connection_string)

mydb = client['ti-data']

user_collection = "users"
user_conn_collection = mydb[user_collection]

pipeline = [
    { "$group": { "_id": "$search", "count": { "$sum": 1 } } },
    { "$sort": { "count": -1 } }
]

result = list(user_conn_collection.aggregate(pipeline))


for item in result:
    print(item)


x1 = int(re.findall(r'\d+', str(result[0]))[0])
x2 = int(re.findall(r'\d+', str(result[1]))[0])
x3 = int(re.findall(r'\d+', str(result[2]))[0])
x4 = int(re.findall(r'\d+', str(result[3]))[0])
x5 = int(re.findall(r'\d+', str(result[4]))[0])

columns = (result[0]['_id'], result[1]['_id'], result[2]['_id'], result[3]['_id'], result[4]['_id'])
values = [x1, x2, x3, x4, x5]

query = {"search": {"$nin": [columns]}}

x6 = user_conn_collection.count_documents(query)

print(x6)

plt.bar(columns, values, color ='purple')

plt.xlabel('String de identificação')
plt.ylabel('Número de usuários')
plt.title('Usuários')

plt.show()
