from fastapi import FastAPI

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pandas as pd
from os import getenv

from .qdrant import q_create_collection, q_upload_records, q_search
from .classes import CreateCollection, QueryPayload, TypeSearch, Response, Error, Status
from .spotify import sp_search
from .init_logger import logger


embedding_model = SentenceTransformer(getenv('MODEL'))
qdrant = QdrantClient(getenv('QDRANT_HOST'),
                      port=getenv('QDRANT_PORT'))

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=getenv('SPOTIFY_CLIENT_ID'),
                                                           client_secret=getenv('SPOTIFY_CLIENT_SECRET')))

dataset = pd.read_csv(getenv('DATAPATH'))
documents = dataset.to_dict('records')

semantic_app = FastAPI()


@semantic_app.post("/create_collection")
def create_collection(req: CreateCollection) -> Response:
    """
    Create a collection and upload records into the collection if documents are loaded.
    """

    # Create a qdrant collection
    q_create_collection(qdrant=qdrant,
                        collection_name=req.collection_name,
                        embedding_model=embedding_model)

    logger.success("Collection created with success.")

    # Upload recods with vectors
    q_upload_records(qdrant=qdrant,
                        collection_name=req.collection_name,
                        embedding_model=embedding_model,
                        documents=documents,
                        key_to_encode = 'lyrics')

    logger.success("Collection filled with success.")

    return Response(
        status=Status.OK,
        status_message="Collection created with success.",
    )


@semantic_app.post("/search")
def search(req: QueryPayload) -> Response:
    """
    Search a query string into a certain collection.

    The query json body follow the shema:

    {
        "query": "your query",
        "collection_name": "my_collection",
        "limit": 15,
        "type": "playlist"
    }

    :param req:QueryPayload - Parameters for the endpoint. Collection_name: str and query: str are required.
    """

    try:
        track = dataset[dataset['track_name'] == req.query].head(1).to_dict('records')[0]
        track_image = sp_search(client = sp, query = track, type="track")

    except Error as e:
        logger.error(f"{e}")
        return Response(
            status=Status.NOT_FOUND,
            status_message=e.status_message,
        )

    results = q_search(qdrant=qdrant,
                       collection_name=req.collection_name,
                       embedding_model=embedding_model,
                       limit=req.limit,
                       query=track["lyrics"])
    
    tracks = [r["payload"]["track_name"] for r in results[1:req.limit+1]]

    logger.info(f"Tracks to suggest: {tracks}")
    
    suggestion_tacks = [{"track": track, "playlists": sp_search(client = sp, query = track, type=req.type, p_limit=req.limit)} for track in tracks]
    
    for t, st in zip(tracks, suggestion_tacks):
        logger.info(f"Playlists to suggest for {t}: {st}")

    response = {
        "track_search": track,
        "track_image": track_image,
        "suggestion_tacks": suggestion_tacks
    }

    return Response(
        status=Status.OK,
        status_message="Query send with success.",
        metadata={"response": response}
    )


@semantic_app.get("/get_collections")
def get_collections() -> Response:
    try:
        collections = qdrant.get_collections()
        logger.success("Collections listed with success.")

        return Response(
            status=Status.OK,
            status_message="Collections listed with success.",
            metadata={"collections": collections}
        )

    except Error as e:
        logger.error(f"{e}")

        return Response(
            status=Status.NOT_FOUND,
            status_message=e.status_message,
        )


@semantic_app.delete("/delete_collections")
def delete_collections(collection_name: str) -> Response:
    try:
        resp = qdrant.delete_collection(collection_name=collection_name)
        if resp:
            logger.success("Collection deleted with success.")

            return Response(
                status=Status.OK,
                status_message="Collection deleted with success.",
            )

        else:
            logger.info(f"Collection {collection_name} not found.")

            return Response(
                status=Status.NOT_FOUND,
                status_message=f"Collection {collection_name} not found.",
            )

    except Error as e:
        logger.error(f"{e}")

        return Response(
            status=Status.INTERNAL_SERVER_ERROR,
            status_message=e.status_message,
        )
