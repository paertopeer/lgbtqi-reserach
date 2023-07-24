import requests
import pandas as pd
import matplotlib.pyplot as plot
import pymongo
import pandas as pd
import seaborn as sns
import plotnine as p9

connection_string = f"mongodb+srv://pvfcosta:dsh2023.retorno@ti6-lbtqia-research.bdfqdy0.mongodb.net/test"

client = pymongo.MongoClient(connection_string)

mydb = client['ti-data']

user_collection = "users_no_duplicates"

follow_metrics_collection = "follow_metrics"

if user_collection in mydb.list_collection_names():
  user_conn_collection = mydb[user_collection]
else:
    print("The collection doesn't exist.")

if follow_metrics_collection in mydb.list_collection_names():
  follow_metrics_conn_collection = mydb[follow_metrics_collection]
else:
    print("The collection doesn't exist.")

cursor = user_conn_collection.find()

follow_cursor = follow_metrics_conn_collection.find()

df = pd.DataFrame(list(cursor))

df_follow = pd.DataFrame(list(follow_cursor))

follow =  df[['followers', 'following']]

df['user']= 'Usuários'

df.loc[df['followers'] == 0, 'followers'] += 1
df.loc[df['following'] == 0, 'following'] += 1

#rq3m1g1

rq3m1g1 = (p9.ggplot(df)
           + p9.aes(y='followers', x='user')
           + p9.geom_boxplot()
           + p9.scale_y_log10()
           + p9.ylab("Seguidores Por Usuário")
           + p9.xlab("")
           + p9.ggtitle("Seguidores por Usuário")
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

rq3m1g1.save("Instrumentos/Codigos/outputs/plots/rq3m1g1.pdf", dpi=600)

#rq3m1g2

rq3m2g2 = (p9.ggplot(df)
           + p9.aes(y='following', x='user')
           + p9.geom_boxplot()
           + p9.scale_y_log10()
           + p9.ylab("Perfis seguidos Por Usuário")
           + p9.xlab("")
           + p9.ggtitle("Perfis seguidos por Usuário")
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

rq3m2g2.save("Instrumentos/Codigos/outputs/plots/rq3m1g2.pdf", dpi=600)


""" sns.boxplot(x=df['followers'])
plot.title("Número de followers")
plot.savefig("followers.png")

plot.clf()

sns.boxplot(x=df['following'])
plot.title("Número de following")
plot.savefig("following.png")

plot.clf()

sns.boxplot(data=df_follow[['comm_followed','comm_following']], orient='v')
plot.title("Número de Seguidores e Seguides em Comum")
plot.savefig("common_following.png") """