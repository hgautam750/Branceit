import logging
import openai
from ..pipeline_upload_embeddings_to_pinecode_vectordb.nodes import connection_to_pinecone

openai_key = "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"
openai.api_key = openai_key


def answer_my_question(query: dict, pinecone_key: str, pinecone_env: str):
    index = connection_to_pinecone(pinecone_key, pinecone_env)
    prompt = query['prompt']
    idx = query['id']
    logging.info("Embedding Query asked: " + prompt)
    xq = openai.Embedding.create(input=prompt, engine='text-embedding-ada-002')['data'][0]['embedding']
    logging.info("Fetching Query match from PineCone")
    try:
        res = index.query([xq], top_k=1, include_metadata=True)
    except Exception as e:
        raise Exception("Index doesnt exist in Pinecone, please run pipeline->create_&_upload_embeddings:  "
                        + str(e))
    if len(res['matches']) > 0:
        for match in res['matches']:
            logging.log(f"{match['score']:.2f}: {match['metadata']['text']}")

        out = match['metadata']['text']
    else:
        out = str(42)

    if type(out) == list:
        response = "".join(out)
    elif type(out) == str:
        response = out
    else:
        raise Exception("Invalid Response")

    logging.info("Q: " + prompt)
    logging.info("A: " + str(response))

    return response
