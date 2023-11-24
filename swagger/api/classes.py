from pydantic import BaseModel, validator, Field
from fastapi import UploadFile
from typing import Optional, Dict, List

class CreateCollection(BaseModel):
    collection_name: str


class QueryPayload(BaseModel):
    collection_name: str
    query: str
    limit: int = 4
    type: str


class TypeSearch(BaseModel):
    playlist: str = 'playlists'
    track: str = 'tracks'

    def filter_type(self, type: str):
        if type == "playlist":
            return self.playlist
        elif type == 'track':
            return self.track


class Status:
    OK: int = 200
    BAD_REQUEST: int = 400
    NOT_FOUND: int = 404
    INTERNAL_SERVER_ERROR: int = 500


class Response(BaseModel):
    status: int
    status_message: str
    metadata: str | Dict | None = None


class Error(Exception):
    def __init__(self, message: str, status_message: str | None = None, detail: str | None = None):
        super().__init__(message)
        self.status_message = status_message
        self.detail = detail
