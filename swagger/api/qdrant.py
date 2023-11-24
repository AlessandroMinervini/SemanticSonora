from fastapi import HTTPException

from qdrant_client import models
from .init_logger import logger


def q_create_collection(qdrant, collection_name, embedding_model):
    logger.info("Creating collection...")
    try:
        qdrant.recreate_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=embedding_model.get_sentence_embedding_dimension(),
                distance=models.Distance.COSINE
            )
        )
        logger.info("Created collection.")
    except Exception as e:
        logger.error(f"{e}")
        raise HTTPException(status_code=500, detail=str(e))


def q_upload_records(qdrant, collection_name, embedding_model, documents, key_to_encode):
    logger.info("Updating collection...")
    try:
        qdrant.upload_records(
            collection_name=collection_name,
            records=[
                models.Record(
                    id=idx,
                    vector=embedding_model.encode(doc[key_to_encode]).tolist(),
                    payload=doc
                ) for idx, doc in enumerate(documents)
            ]
        )
        logger.info("Updated collection...")
    except Exception as e:
        logger.error(f"{e}")
        raise HTTPException(status_code=500, detail=str(e))


def q_search(qdrant, collection_name, embedding_model, limit, query):
    logger.info("Searching...")
    try:
        hits = qdrant.search(
            collection_name=collection_name,
            query_vector=embedding_model.encode(query).tolist(),
            limit=limit
        )

        results = [{"payload": hit.payload, "score": hit.score}
                   for hit in hits]

        # for hit in hits:
        #     print(hit.payload, "score:", hit.score)

        logger.info("Qdrant search end.")
        return results

    except Exception as e:
        logger.error(f"{e}")
        raise HTTPException(status_code=500, detail=str(e))
