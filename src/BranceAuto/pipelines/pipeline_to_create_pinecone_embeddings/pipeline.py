# Initially coded by Harsh Gautam

from kedro.pipeline import Pipeline, node
from .nodes import read_knowledge_doc, convert_doc_to_embeddings


def create_pipeline_pinecone_embeddings(**kwargs):
    tags = ["create_embeddings"]
    return Pipeline(
        [
            node(
                read_knowledge_doc,
                "input_knowledge_txt_document_pan_card",
                "df_input_knowledge_document_pan_card",
                name="read_knowledge_doc_refinement",
                tags=tags
            ),
            node(
                convert_doc_to_embeddings,
                "df_input_knowledge_document_pan_card",
                "output_embeddings_csv",
                name="convert_doc_to_embeddings_csv",
                tags=tags
            )
        ]
    )

