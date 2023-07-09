import json
import yaml
from src.BranceAuto.pipelines.pipeline_qa.nodes import answer_my_question
path = './conf/base/parameters.yml'
with open(path) as file:
    data = yaml.load(file)

key = data["pinecone_key"]
env = data["pinecone_env"]


def lambda_handler(event, context):
    body = json.loads(event["body"])
    prompt = body['query']["prompt"]
    idx = body['query']["id"]
    res = answer_my_question(query=body['query'], pinecone_key=key, pinecone_env=env)

    if res is None:
        res = 42

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "id": idx,
            "response": res
        })
    }


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sample_event = {
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            'query': data['query']
        })
    }
    sample_context = None
    out = lambda_handler(sample_event, sample_context)
    if out["statusCode"] == 200:
        response = json.loads(out["body"])["response"]
        print("Q: " + json.loads(sample_event["body"])['query']["prompt"])
        print("A: " + str(response))
    else:
        raise Exception("Invalid Response")