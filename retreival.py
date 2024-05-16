from langchain_community.embeddings import HuggingFaceInstructEmbeddings


# from langchain_community.vectorstores import ElasticsearchStore
from langchain_community.vectorstores.elasticsearch import ElasticsearchStore
from langchain_community.embeddings import HuggingFaceEmbeddings

# embeddings = HuggingFaceInstructEmbeddings(
#             # model_name="msmarco-distilbert-base-tas-b",
#             model_name="hkunlp/instructor-xl",
#             # model_kwargs = {'device': 'cpu'},
#             encode_kwargs = {'normalize_embeddings': False}
#     )
embeddings = HuggingFaceEmbeddings(
        # model_name="msmarco-distilbert-base-tas-b",
        model_name="hkunlp/instructor-xl",
        encode_kwargs = {'normalize_embeddings': True}
    )

embed = embeddings.embed_documents(["how to add permission to github actions?"])
print(embed)

db = ElasticsearchStore(
    es_url="http://localhost:9200",
    index_name="512_index",
    embedding = embeddings,
    es_user="mike",
    es_password=""
)
 
print(embed[0])

outs = db.similarity_search_by_vector_with_relevance_scores( embed[0], k=20)

for (doc, score) in outs:
    print(doc)
    print(score)
    