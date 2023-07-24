
import requests
import pandas as pd
import matplotlib.pyplot as plot
import pymongo

connection_string = f"mongodb+srv://pvfcosta:dsh2023.retorno@ti6-lbtqia-research.bdfqdy0.mongodb.net/test"

client = pymongo.MongoClient(connection_string)

mydb = client['ti-data']

GITHUB_API_ENDPOINT = "https://api.github.com/graphql"

NUMBER_OF_ATTEMPTS = 15

# colocar token aqui
token = "VSW8eNDQYUBVgxY6L4EQtZSO5Wh6Cn1QK1pm"

CURSOR_QUERY = """
query($login:String!,$cursor:String!)
{
  user(login: $login) {
    following(after: $cursor, first: 50) {
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
    following(after: null, first: 50) {
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

        token_1 = "zZx07Qs7B4nzWLvH0waExtyRrOzsNW2Lmp7J"

        token_2 = "GjRyws4PZUKZJJRPvag3lB4I2Wd2hQ2aWvbe"

        if attemp > 5 and attemp <= 10:
          headers = {"Authorization": "Bearer ghp_" + token_2} 
        else:
          headers = {"Authorization": "Bearer ghp_" + token_1}

        request = requests.post(GITHUB_API_ENDPOINT, headers=headers, json={"query": query, "variables": variables})

        if request.status_code == 200:
            return request.json()
        elif attemp <= NUMBER_OF_ATTEMPTS:
            print("Tentativa de conexão falhou :(. {}/{} Tentando novamente...".format(attemp,
                  NUMBER_OF_ATTEMPTS))
            sleep(1)
            return run_query_variables(query, attemp + 1, variables)
        else:
            raise Exception("Tentativa de conexão falhou com o erro: {}. {}".format(
                request.status_code, query))

def save_following(login, following):
    data = []
    for follow in following:
        follower = {
            "followed": follow["login"],
            "following": login
        }
        data.append(follower)

    if len(data) > 0:
        foll_conn_collection.insert_many(data)
    else:
        print("No data to be inserted")


def fetch_following(login):
    variables = {"login": login}
    has_next = True
    i = 0
    end_cursor = "null"
    follows = []
    query = INITIAL_QUERY

    response = run_query_variables(query, 1, variables)

    if response["data"]["user"] == None:
      has_next = False
    elif len(response["data"]["user"]["following"]["nodes"]) > 0:
      follows += response["data"]["user"]["following"]["nodes"]
      has_next = response["data"]["user"]["following"]["pageInfo"]["hasNextPage"]
    else:
      has_next = response["data"]["user"]["following"]["pageInfo"]["hasNextPage"]

    if has_next:
        end_cursor = response["data"]["user"]["following"]["pageInfo"]["endCursor"]

    i += 1

    query = CURSOR_QUERY

    while(has_next):

        variables = {"login": login,"cursor":end_cursor}

        response = run_query_variables(query, 1, variables)

        if len(response["data"]["user"]["following"]["nodes"]) > 0:

          has_next = response["data"]["user"]["following"]["pageInfo"]["hasNextPage"]

          if has_next:
              end_cursor = response["data"]["user"]["following"]["pageInfo"]["endCursor"]

          follows += response["data"]["user"]["following"]["nodes"]

        print(end_cursor)

        i += 1

    save_following(login, follows)

cursor = user_conn_collection.find({'following': {'$gt': 0}})
user_df = pd.DataFrame(list(cursor))
logins = user_df['login'] 

for login in logins:
    print('usuario: ' + login)
    fetch_following(login)

print('Done!')