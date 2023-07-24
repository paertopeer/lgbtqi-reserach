import requests
import pandas as pd
import matplotlib.pyplot as plot
import pymongo
import plotnine as p9

connection_string = f"mongodb+srv://pvfcosta:dsh2023.retorno@ti6-lbtqia-research.bdfqdy0.mongodb.net/test"

client = pymongo.MongoClient(connection_string)

mydb = client['ti-data']

user_collection = "users_no_duplicates"

if user_collection in mydb.list_collection_names():
    user_conn_collection = mydb[user_collection]
else:
    print("The collection doesn't exist.")

sponsor_collection = "sponsor"

if sponsor_collection in mydb.list_collection_names():
    spon_conn_collection = mydb[sponsor_collection]
else:
    print("The collection doesn't exist.")

metrics_collection = "sponsor_metrics"

if metrics_collection in mydb.list_collection_names():
    print("The collection exists.")
    metrics_conn_collection = mydb[metrics_collection]
else:
    metrics_conn_collection = mydb.create_collection(metrics_collection)

user_docs = user_conn_collection.find()
spon_docs = spon_conn_collection.find({})

df_spon = pd.DataFrame(list(spon_docs))

users = pd.DataFrame(list(user_docs))
metrics = []
logins = users['login'].tolist()

for login in logins:
    data = []
    mask_sponsored = ((df_spon['sponsor'] == login) & df_spon['sponsored'].isin(logins))
    mask_sponsor = ((df_spon['sponsored'] == login) & df_spon['sponsor'].isin(logins))

    comm_sponsors = df_spon[mask_sponsor]
    comm_sponsoring = df_spon[mask_sponsored]
    metric = {
        "login": login,
        "comm_sponsors": len(comm_sponsors),
        "comm_sponsoring": len(comm_sponsoring)
    }

    metrics.append(metric)

metrics_conn_collection.insert_many(metrics)

users['user']= 'Usuários'

#rq3m2g1

rq3m2g1 = (p9.ggplot(users)
           + p9.aes(y='sponsors', x='user')
           + p9.geom_boxplot()
           + p9.ylab("Patrocinadores por Usuário")
           + p9.xlab("")
           + p9.ggtitle("Patrocinadores por Usuário")
           + p9.theme(
               axis_text=p9.element_text(size=15),
               panel_grid_major=p9.element_blank(),
               panel_grid_minor=p9.element_blank(),
               panel_border=p9.element_blank(),
               panel_background=p9.element_blank(),
               plot_title=p9.element_text(size=24),
               axis_title_x=p9.element_text(size=20),
               axis_title_y=p9.element_text(size=20),
            )
)

rq3m2g1.save("Instrumentos/Codigos/outputs/plots/rq3m2g1.pdf", dpi=600)

#rq3m1g2

rq3m2g2 = (p9.ggplot(users)
           + p9.aes(y='sponsoring', x='user')
           + p9.geom_boxplot()
           + p9.ylab("Perfis patrocinados por Usuário")
           + p9.xlab("")
           + p9.ggtitle("Perfis patrocinados por Usuário")
           + p9.theme(
               axis_text=p9.element_text(size=15),
               panel_grid_major=p9.element_blank(),
               panel_grid_minor=p9.element_blank(),
               panel_border=p9.element_blank(),
               panel_background=p9.element_blank(),
               plot_title=p9.element_text(size=24),
               axis_title_x=p9.element_text(size=30, color='black'),
               axis_title_y=p9.element_text(size=20),
            )
)

rq3m2g2.save("Instrumentos/Codigos/outputs/plots/rq3m2g2.pdf", dpi=600)


