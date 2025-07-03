import os
import json
import chromadb
from connect_openAI import connect_to_openAI
import chromadb.utils.embedding_functions as embedding_functions

def get_concepts(query, n_results):
    chroma_client = chromadb.PersistentClient(path="/home/irena/data/micro-concepts/embeddings")

    model = "text-embedding-3-small"
    client = connect_to_openAI(model)

    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                    api_key=os.environ["AZURE_API_KEY_4o"],
                    api_base=os.environ["AZURE_ENDPIONT_EMBEDDING"],
                    api_type="azure",
                    api_version="2024-05-01-preview",
                    model_name=model
                )

    collection = chroma_client.get_or_create_collection(name="concept_embeddings", embedding_function=openai_ef)

    response = client.embeddings.create(
        input=query, 
        model=model
    )
    query_embedding = response.data[0].embedding

    results = collection.query(
        query_embeddings =[query_embedding], 
        n_results=n_results,
        include=["documents","distances"], 

    )

    return results

