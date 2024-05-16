from elasticsearch import Elasticsearch



from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.embeddings import HuggingFaceInstructEmbeddings


# from langchain_community.vectorstores import ElasticsearchStore
from langchain_community.vectorstores.elasticsearch import ElasticsearchStore

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
import time



# Configuration
es_host = 'http://localhost:9200'  # Replace with your Elasticsearch host
index_name = 'my_index'            # Replace with your index name


# Connect to Elasticsearch
es = Elasticsearch(
    es_host,
    http_auth=("mike", "")
)




def embed_and_load(title=None):
    file_save = "section.txt"  
    # Embed the text
    loader = TextLoader("section.txt", encoding="utf-8")
    documents = loader.load()
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=300, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)


    embeddings = HuggingFaceEmbeddings(
        model_name="msmarco-distilbert-base-tas-b",
        encode_kwargs = {'normalize_embeddings': True}
    )
    
    
    
def create_index_with_mapping(es, index_name):
    # Define your mapping
    mapping = {
    "mappings": {
        "properties": {
        "text": {
            "type": "text",
            "fields": {
            "keyword": {
                "type": "keyword",
                "ignore_above": 256
            }
            }
        },
            "title": {
            "type": "text",
            "fields": {
            "keyword": {
                "type": "keyword",
                "ignore_above": 256
            }
            }
        },
        "vector": {
            "type": "dense_vector",
            "dims": 4096,
            "index": "true",
            "similarity": "dot_product"
        }
        }
    }
    }
    try:
        # Check if the index already exists
        if not es.indices.exists(index=index_name):
            # Create the index with the specified mapping
            es.indices.create(index=index_name, body=mapping)
            print(f"Index '{index_name}' created.")
        else:
            print(f"Index '{index_name}' already exists.")
    except Exception as e:
        print(f"Error creating index: {e}")
        



# Create the index with the mapping
create_index_with_mapping(es, index_name)