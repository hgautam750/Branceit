"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline
from pipelines.pipeline_to_create_pinecone_embeddings.pipeline import create_pipeline_pinecone_embeddings
from pipelines.pipeline_upload_embeddings_to_pinecode_vectordb.pipeline \
    import create_pipeline_upload_pinecone_embeddings
from pipelines.pipeline_qa.pipeline import create_pipeline_qa


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """
    create_new_embeddings_from_doc = create_pipeline_pinecone_embeddings(tags=["create_embeddings"])
    upsert_embeddings = create_pipeline_upload_pinecone_embeddings(tags=["upsert"])
    qa = create_pipeline_qa(tags=["QA"])

    return {"__default__": qa,
            "create_embeddings": create_new_embeddings_from_doc + upsert_embeddings,        # create embeddings (batch)
            "upsert": upsert_embeddings,                    # Upload embeddings to Pinecone DB Pipeline  (batch)
            "qa": qa,                                       # Question&Answer Pipeline ( Will run in realtime )
            }
