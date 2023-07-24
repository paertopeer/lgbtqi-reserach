import pymongo
import pandas as pd
import plotnine as p9
import numpy as np
# import ggplot, aes, geom_boxplot, coord_flip, labs, scale_y_log10

connection_string = f"mongodb+srv://pvfcosta:dsh2023.retorno@ti6-lbtqia-research.bdfqdy0.mongodb.net/test"

client = pymongo.MongoClient(connection_string)

mydb = client['ti-data']

user_collection = "users_no_duplicates"
user_conn_collection = mydb[user_collection]

df = pd.DataFrame(list(user_conn_collection.find()))

df['commitsPerWeek_noZero'] = df['commitsPerWeek'] + 1

df['commitsPerDay'] = df['commitsPerWeek'] / 7
df['commitsPerDay_noZero'] = df['commitsPerDay'] + 1

df['accountAge_inYears'] = df['accountAge'] / 365

# rq1m2g1
rq1m2g1 = (p9.ggplot(df)
           + p9.aes(y='commitsPerDay_noZero', x=0)
           + p9.geom_boxplot()
           + p9.scale_y_log10()
           + p9.ylab("Commits Por Dia")
           + p9.xlab("Usuários")
           + p9.ggtitle("Commits por Dia por Usuário")
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
rq1m2g1.save("Instrumentos/Codigos/outputs/plots/rq1m2g1.pdf", dpi=600)

# rq1m2g2
rq1m2g2 = (p9.ggplot(df)
           + p9.aes(y='commitsPerWeek_noZero', x=0)
           + p9.geom_boxplot()
           #  + p9.coord_flip()        # flipping the x- and y-axes
           #  + labs(title='Média de commits por semana por usuário', x='Média de commits por semana', y='') # customizing labels
           + p9.scale_y_log10()
           + p9.ylab("Commits Por Semana")
           + p9.xlab("Usuários")
           + p9.ggtitle("Commits por Semana por Usuário")
           + p9.theme(
              axis_text=p9.element_text(size=15),
               panel_grid_major=p9.element_blank(),
               panel_grid_minor=p9.element_blank(),
               panel_border=p9.element_blank(),
               panel_background=p9.element_blank(),
               plot_title=p9.element_text(size=24),
            #    text=p9.element_text(size=30),
               axis_title_x=p9.element_text(size=20),
               axis_title_y=p9.element_text(size=20),
            )
)
rq1m2g2.save("Instrumentos/Codigos/outputs/plots/rq1m2g2.pdf", dpi=600)

# rq1m3
rq1m3 = (p9.ggplot(df)
           + p9.aes(y='accountAge_inYears', x=0)
           + p9.geom_boxplot()
           #  + p9.coord_flip()        # flipping the x- and y-axes
           #  + labs(title='Média de commits por semana por usuário', x='Média de commits por semana', y='') # customizing labels
           + p9.scale_y_log10()
           + p9.ylab("Idade (Anos)")
           + p9.xlab("Usuários")
           + p9.ggtitle("Idade do Perfil por Usuário")
           + p9.theme(
              axis_text=p9.element_text(size=15),
               panel_grid_major=p9.element_blank(),
               panel_grid_minor=p9.element_blank(),
               panel_border=p9.element_blank(),
               panel_background=p9.element_blank(),
               plot_title=p9.element_text(size=24),
            #    text=p9.element_text(size=30),
               axis_title_x=p9.element_text(size=20),
               axis_title_y=p9.element_text(size=20),
            )
)
rq1m3.save("Instrumentos/Codigos/outputs/plots/rq1m3.pdf", dpi=600)

# rq1m4g1
rq1m4g1 = (p9.ggplot(df)
           + p9.aes(y='pullRequests', x=0)
           + p9.geom_boxplot()
           #  + p9.coord_flip()        # flipping the x- and y-axes
           #  + labs(title='Média de commits por semana por usuário', x='Média de commits por semana', y='') # customizing labels
           + p9.scale_y_log10()
           + p9.ylab("Quantidade de Pull Requests")
           + p9.xlab("Usuários")
           + p9.ggtitle("Pull Requests por Usuário")
           + p9.theme(
              axis_text=p9.element_text(size=15),
               panel_grid_major=p9.element_blank(),
               panel_grid_minor=p9.element_blank(),
               panel_border=p9.element_blank(),
               panel_background=p9.element_blank(),
               plot_title=p9.element_text(size=24),
            #    text=p9.element_text(size=30),
               axis_title_x=p9.element_text(size=20),
               axis_title_y=p9.element_text(size=20),
            )
)
rq1m4g1.save("Instrumentos/Codigos/outputs/plots/rq1m4g1.pdf", dpi=600)


# rq1m4g2
rq1m4g2 = (p9.ggplot(df)
           + p9.aes(y='issues', x=0)
           + p9.geom_boxplot()
           #  + p9.coord_flip()        # flipping the x- and y-axes
           #  + labs(title='Média de commits por semana por usuário', x='Média de commits por semana', y='') # customizing labels
           + p9.scale_y_log10()
           + p9.ylab("Quantidade de Issues")
           + p9.xlab("Usuários")
           + p9.ggtitle("Issues por Usuário")
           + p9.theme(
              axis_text=p9.element_text(size=15),
               panel_grid_major=p9.element_blank(),
               panel_grid_minor=p9.element_blank(),
               panel_border=p9.element_blank(),
               panel_background=p9.element_blank(),
               plot_title=p9.element_text(size=24),
            #    text=p9.element_text(size=30),
               axis_title_x=p9.element_text(size=20),
               axis_title_y=p9.element_text(size=20),
            )
)
rq1m4g2.save("Instrumentos/Codigos/outputs/plots/rq1m4g2.pdf", dpi=600)

repo_collection = "repositories"
repo_conn_collection = mydb[repo_collection]

df2 = pd.DataFrame(list(repo_conn_collection.find()))

df2['commitsPerWeek'] = df2['total_commits'] / (df2['age_years'] * 52)
df2['commitsPerWeek_no_zero'] = np.where(df2['commitsPerWeek'] == 0, df2['commitsPerWeek'] + 1, df2['commitsPerWeek'])

# rq2m2
rq2m2 = (p9.ggplot(df2)
           + p9.aes(y='age_years', x=0)
           + p9.geom_boxplot()
           #  + p9.coord_flip()        # flipping the x- and y-axes
           #  + labs(title='Média de commits por semana por usuário', x='Média de commits por semana', y='') # customizing labels
           + p9.scale_y_log10()
           + p9.ylab("Idade (Anos)")
           + p9.xlab("Repositórios")
           + p9.ggtitle( "Idade em anos por repositório")
           + p9.theme(
              axis_text=p9.element_text(size=15),
               panel_grid_major=p9.element_blank(),
               panel_grid_minor=p9.element_blank(),
               panel_border=p9.element_blank(),
               panel_background=p9.element_blank(),
               plot_title=p9.element_text(size=24),
            #    text=p9.element_text(size=30),
               axis_title_x=p9.element_text(size=20),
               axis_title_y=p9.element_text(size=20),
            )
)
rq2m2.save("Instrumentos/Codigos/outputs/plots/rq2m2.pdf", dpi=1200)

# rq1m5
rq1m5 = (p9.ggplot(df2)
           + p9.aes(y='commitsPerWeek_no_zero', x = 0)
           + p9.geom_boxplot()
           + p9.scale_y_log10()
           + p9.ylab("Commits Por Semana")
           + p9.xlab("Commits")
           + p9.ggtitle("Commits em Repositórios")
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
rq1m5.save("Instrumentos/Codigos/outputs/plots/rq2m5.pdf", dpi=1200)