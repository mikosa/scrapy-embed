from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.embeddings import HuggingFaceInstructEmbeddings


# from langchain_community.vectorstores import ElasticsearchStore
from langchain_community.vectorstores.elasticsearch import ElasticsearchStore

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
import time

def embed_and_load(title=None):
    file_save = "section.txt"  
    # Embed the text
    loader = TextLoader(file_save, encoding="utf-8")
    documents = loader.load()
    documents[0].metadata['title'] = title
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=512, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)


    embeddings = HuggingFaceEmbeddings(
        # model_name="msmarco-distilbert-base-tas-b",
        model_name="hkunlp/instructor-xl",
        encode_kwargs = {'normalize_embeddings': True}
    )
    
    # embeddings = HuggingFaceInstructEmbeddings(
    #             model_name="sentence-transformers/all-mpnet-base-v2",
    #             # model_name="BAAI/bge-large-en-v1.5",
    #             # model_kwargs = {'device': 'cpu'},
    #             encode_kwargs = {'normalize_embeddings': True}
    #     )

    print(title)
    db = ElasticsearchStore.from_documents(
        docs,
        embeddings,
        es_url="http://localhost:9200",
        index_name="512_index",
        es_user="mike",
        es_password=""
    )
    db.client.indices.refresh(index="toto_index")

file_save = "section.txt"    
file_path = "output.txt" 
current_section = ''
n = 0
title = ''
# Open the file and process it line by line
with open(file_path, 'r',  encoding="utf-8") as file:
    for line in file:
        # Check if the line is a separator
        if line.strip() == '------':
            if current_section:
                n += 1
                print(n)
                # print(current_section)
                with open(file_save, 'w',  encoding="utf-8") as file:
                    file.write(current_section)
                # sleep fpr 3 secons
                embed_and_load(title)
                title = ''
                current_section = ''
        elif not line.startswith('Link') and not line.startswith('URL: '): 
            current_section += line
        if line.startswith("Title: "):
            title = line.replace("Title: ", "")
            title = title.strip()
            # print(title)
                

db = ElasticsearchStore(
    es_url="http://localhost:9200",
    index_name="test_index2",
    es_user="mike",
    es_password=""
)

db.similarity_search_by_vector
print(db.similarity_search("What is github action?"))


# query = "What is github action?"
# results = db.similarity_search(query)
# print(results)