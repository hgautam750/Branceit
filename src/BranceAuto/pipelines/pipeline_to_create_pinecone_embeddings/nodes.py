import logging
import pandas as pd
import openai
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)

openai_key = "xxxxxxx"
openai.api_key = openai_key


@retry(wait=wait_random_exponential(min=1, max=55), stop=stop_after_attempt(610))
def completion_with_backoff(**kwargs):
    return openai.Embedding.create(**kwargs)['data'][0]['embedding']


def read_knowledge_doc(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Creating new embeddings")
    logging.info("Reading Knowledge Document")
    df.reset_index(inplace=True)
    df = df['index']
    df_ = pd.DataFrame(df.values, columns=['text'])
    return df_


def convert_doc_to_embeddings(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Converting doc to embeddings")
    df['embeddings'] = df.text.apply(lambda x: completion_with_backoff(input=x, engine='text-embedding-ada-002'))
    # df.to_csv('./StaticData/embeddings.csv')
    logging.info("Snapshot of Embeddings: ", df.head())
    return df
