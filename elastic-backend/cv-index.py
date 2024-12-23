import requests
import pandas as pd

csv_path = "/app/shared-data/cv-valid-dev.csv"
es_url = "http://elastic-backend-1:9200"
kibana_url = "http://search-ui:5601"
index = "cv-transcriptions"

def create_es_index(es_url, index_name):
    response = requests.head(f"{es_url}/{index_name}")

    if response.status_code == 404:
        requests.put(f"{es_url}/{index_name}", json={
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 1
            }
        })

def ingest_csv(csv_path, es_url, index):
    create_es_index(es_url, index)
    df = pd.read_csv(csv_path).replace({float('nan'): ""})
    for i, row in df.iterrows():
        doc = row.to_dict()
        requests.post(f"{es_url}/{index}/_doc", json=doc)


if __name__ == "__main__":
    ingest_csv(csv_path, es_url, index)
