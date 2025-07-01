import requests
import json
from queue import Queue
import os


NEWS_ARTICLE_URL="https://newsapi.org/v2/everything"
API_KEY="43a1035ead4349feaffa8324ca3f540b"
count=10

# Create the queue
q = Queue()


def download_news_article(api_key,count) ->list[dict]:
    news_api_respones=requests.get(NEWS_ARTICLE_URL,params={
        "apikey": api_key,
        "q" : "bitcoin",
        "pageSize": count
    })
    news_api_respones.raise_for_status()
    news_articles=news_api_respones.json().get("articles",[])
    return news_articles

def save_srticles(articles):
    i=0
    for i,article in enumerate(articles):
        filename=f"article_{i}.json"
        with open(filename,"w",encoding="utf-8") as f:
            json.dump(article,f,indent=4)
        print(f"Saved article {i} to {filename}")




# # List of JSON file paths
# json_dir = r'C:\news_articles'

# json_files = ([ f for f in os.listdir(json_dir) if f.endswith('.json')])
# # Load each file and put the data into the queue
# for filename in json_files:
#     filepath = os.path.join(json_dir, filename)
#     q.put(filepath)

# # Optional: Print all items in the queue
# while not q.empty():
#     print(q.get())

if __name__=="__main__":
    articles=download_news_article(API_KEY,count)
    #save_srticles(articles)
    # for article in articles:
    #     prfolderint (f" the downloded article is : {article}")
    #     print("\n")

    