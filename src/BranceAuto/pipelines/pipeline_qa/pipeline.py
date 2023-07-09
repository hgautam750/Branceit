# Initially coded by Harsh Gautam

from kedro.pipeline import Pipeline, node
from .nodes import answer_my_question


def create_pipeline_qa(**kwargs):
    tags = ["QA"]
    return Pipeline(
        [
            node(
                answer_my_question,
                ["params:query", "params:pinecone_key", "params:pinecone_env"],
                "dummy_qa",
                name="Q_and_A",
                tags=tags
            )
        ]
    )

