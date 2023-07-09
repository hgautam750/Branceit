"""
responsible for creating index at cloud managed Pinecone Vector DB

"""
import logging
import os
import pinecone
import pandas as pd
import numpy as np
from tqdm.auto import tqdm

# pinecone_key = os.getenv("PINECONE_KEY","767b3586-ab00-42f6-b2c8-27269a8b442a")
# pinecone_env = os.getenv("PINECONE_ENV","us-central1-gcp")
# openai_key = os.getenv("OPENAI_KEY","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")
# embedding_path = "./StaticData/embeddings.csv"


def connection_to_pinecone(pinecone_key: str, pinecone_env: str):
    logging.info("Initiating connection to pinecone")
    index = None
    pinecone.init(
        api_key=pinecone_key,
        environment=pinecone_env  # go to https://app.pinecone.io/organizations
    )
    if "embeddings" in pinecone.list_indexes():
        index = pinecone.Index('embeddings')
    else:
        logging.info("Index not found on Pinecone, hence creating")
        pinecone.create_index('embeddings', dimension=1536, metric='cosine')
        index = pinecone.Index('embeddings')

    return index


def upsert_embeddings_to_pinecone(df: pd.DataFrame, pinecone_key: str, pinecone_env: str):
    index = connection_to_pinecone(pinecone_key, pinecone_env)
    logging.info("Upsert embeddings to pinecone in progress")
    # df = pd.read_csv(embedding_path, index_col=0)
    df['embeddings'] = df['embeddings'].apply(eval).apply(np.array)

    batch_size = 16  # process everything in batches of 16
    for i in tqdm(range(0, len(df), batch_size)):
        # set end position of batch
        i_end = min(i + batch_size, len(df))
        # get batch of lines and IDs
        lines_batch = df['text'][i: i + batch_size]
        embeddings_batch = df['embeddings'][i: i + batch_size]
        ids_batch = [str(n) for n in range(i, i_end)]
        embeddings = [e.tolist() for e in embeddings_batch]
        metadata = [{'text': text} for text in zip(lines_batch)]
        # upsert batch
        to_upsert = zip(ids_batch, embeddings, metadata)
        index.upsert(list(to_upsert))

    logging.info("Upsert embeddings to pinecone complete")