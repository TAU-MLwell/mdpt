import concurrent.futures
import os
import csv
import json
import time
import tqdm
import torch
import chromadb
import concurrent.futures
from connect_openAI import connect_to_openAI
import chromadb.utils.embedding_functions as embedding_functions

model = "text-embedding-3-small"
client = connect_to_openAI(model)
vector_client = chromadb.PersistentClient(path="data/micro-concepts/embeddings")

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key=os.environ["AZURE_API_KEY_4o"],
                api_base=os.environ["AZURE_ENDPOINT_EMBEDDING"],
                api_type="azure",
                api_version="2024-05-01-preview",
                model_name=model
            )

#vector_client.delete_collection(name="concept_embeddings") 

collection = vector_client.get_or_create_collection(
        name="concept_embeddings",
        metadata={"hnsw:space": "cosine"},
        embedding_function=openai_ef
    )


print("Loading concepts")
with open("data/micro-concepts/concepts.json", 'r') as json_file:
        data = json.load(json_file)
print("Loading concepts complete")

data_as_list = [str(d) for d in list(data.values())]

def add_batch(idx, batch_size=80):
    collection.add(
        documents=data_as_list[idx:idx + batch_size],
        metadatas=[{'concept': data[str(i)]['concept_name']} for i in range(idx, idx + batch_size)],
        ids=[str(element) for element in range(idx, idx + batch_size)]
    )
    if idx % 8000 == 0:
        end = time.perf_counter()
        print(f"{idx + batch_size} of {len(data_as_list)} ({100 * (idx + batch_size) / len(data_as_list):0.4f}%). {((end - start) / 60):0.4f} minutes passed.")


start = time.perf_counter()

# Use a ThreadPoolExecutor to parallelize the tasks
with concurrent.futures.ThreadPoolExecutor(max_workers=40) as executor:
    # Submit tasks to the thread pool
    futures = [executor.submit(add_batch, idx) for idx in range(0, len(data_as_list), 80)]

# Wait for all the tasks to complete
concurrent.futures.wait(futures)

end = time.perf_counter()
print(f"Total time: {(end - start) / 60} minutes")
