import requests
import pandas as pd
import matplotlib.pyplot as plot
import pymongo
from time import sleep

connection_string = f"mongodb+srv://pvfcosta:dsh2023.retorno@ti6-lbtqia-research.bdfqdy0.mongodb.net/test"

client = pymongo.MongoClient(connection_string)

mydb = client['ti-data']

GITHUB_API_ENDPOINT = "https://api.github.com/graphql"

NUMBER_OF_ATTEMPTS = 15

CURSOR_QUERY = """
query($login:String!,$cursor:String!)
{
  user(login: $login) {
    followers(after: $cursor, first: 50) {
      nodes {
        login
      }
      pageInfo {
        endCursor
        hasNextPage
      }
    }
  }
}
"""

INITIAL_QUERY = """
query($login:String!)
{
  user(login: $login) {
    followers(after: null, first: 50) {
      nodes {
        login
      }
      pageInfo {
        endCursor
        hasNextPage
      }
    }
  }
}
"""
token_1 = "Dq5ScIdda8ScfHPEEQI3aOcVc0qLvO3VELU2"

token_2 = "90FbpSheSJlrsWBjy2GorF3fz10fLu2FuYrX"

token_3 = "VSW8eNDQYUBVgxY6L4EQtZSO5Wh6Cn1QK1pm"

user_collection = "users_no_duplicates"

if user_collection in mydb.list_collection_names():
  user_conn_collection = mydb[user_collection]
else:
    print("The collection doesn't exist.")

follow_collection = "follow"

if follow_collection in mydb.list_collection_names():
  print("The collection exists.")
  foll_conn_collection = mydb[follow_collection]
else:
  foll_conn_collection = mydb.create_collection(follow_collection)

def run_query_variables(query, attemp, variables):

        token = "VSW8eNDQYUBVgxY6L4EQtZSO5Wh6Cn1QK1pm"

        headers = {"Authorization": "Bearer ghp_" + token}

        request = requests.post(GITHUB_API_ENDPOINT, headers=headers, json={"query": query, "variables": variables})

        if request.status_code == 200:
            return request.json()
        elif attemp <= NUMBER_OF_ATTEMPTS:
          if token == token_1:
            token = token_2
          else:
            token = token_1
          print("Tentativa de conexão falhou :(. {}/{} Tentando novamente...".format(attemp,
                NUMBER_OF_ATTEMPTS))
          sleep(1)
          return run_query_variables(query, attemp + 1, variables)
        else:
            raise Exception("Tentativa de conexão falhou com o erro: {}. {}".format(
                request.status_code, query))

def save_followers(login, followers):
    foll_cursor = foll_conn_collection.find()
    foll_df = pd.DataFrame(list(foll_cursor))
    if len(foll_df) > 0:
      following_names = foll_df['following']
    else:
      following_names = []

    for follow in followers:
        if follow["login"] in list(following_names):
          print('pula seguidor')
          continue

        follower = {
            "followed": login,
            "following": follow["login"]
        }

        foll_conn_collection.insert_one(follower)


def fetch_followers(login):
    variables = {"login": login}
    has_next = True
    end_cursor = "null"
    follows = []
    query = INITIAL_QUERY

    response = run_query_variables(query, 1, variables)
    print(response)
    if response["data"]["user"] == None:
      has_next = False
    elif len(response["data"]["user"]["followers"]["nodes"]) > 0:
      follows += response["data"]["user"]["followers"]["nodes"]
      has_next = response["data"]["user"]["followers"]["pageInfo"]["hasNextPage"]
    else:
      has_next = response["data"]["user"]["followers"]["pageInfo"]["hasNextPage"]

    if has_next:
        end_cursor = response["data"]["user"]["followers"]["pageInfo"]["endCursor"]

    query = CURSOR_QUERY

    while(has_next):

        variables = {"login": login,"cursor":end_cursor}

        response = run_query_variables(query, 1, variables)

        if len(response["data"]["user"]["followers"]["nodes"]) > 0:

          has_next = response["data"]["user"]["followers"]["pageInfo"]["hasNextPage"]

          if has_next:
              end_cursor = response["data"]["user"]["followers"]["pageInfo"]["endCursor"]

          follows += response["data"]["user"]["followers"]["nodes"]

          print(end_cursor)

    save_followers(login, follows)

cursor = user_conn_collection.find({'followers': {'$gt': 0}})
user_df = pd.DataFrame(list(cursor))
logins = user_df['login']

foll_cursor = foll_conn_collection.find()
foll_df = pd.DataFrame(list(foll_cursor))
if len(foll_df) > 0:
  users = foll_df['followed'].drop_duplicates()
  last = users.iloc[-1]
  users.drop(users.index[-1])
else:
  users = []

for login in logins:
  if login in list(users):
    print('pula usuario')
    continue
  print('usuario' + login)
  fetch_followers(login)

print('Done!')