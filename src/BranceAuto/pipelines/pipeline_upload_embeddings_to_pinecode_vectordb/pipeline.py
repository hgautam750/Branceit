# Initially coded by Harsh Gautam

from kedro.pipeline import Pipeline, node
from .nodes import connection_to_pinecone, upsert_embeddings_to_pinecone


def create_pipeline_upload_pinecone_embeddings(**kwargs):
    tags = ["pinecone_connect"]
    return Pipeline(
        [
            # node(
            #     connection_to_pinecone,
            #     ["params:pinecone_key", "params:pinecone_env"],
            #     dict(
            #         index="index",
            #     ),
            #     name="initiate_connection_with_pinecone_vector_db",
            #     tags=tags + ["pinecone_connect_only"]
            # ),
            node(
                upsert_embeddings_to_pinecone,
                ["output_embeddings_csv", "params:pinecone_key", "params:pinecone_env"],
                ["dummy"],
                name="upsert_embeddings_to_pinecone",
                tags=tags + ["upsert"]
            )
        ]
    )

