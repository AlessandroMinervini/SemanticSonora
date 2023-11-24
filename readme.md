SemanticSonora

## Description
This platform utilizes a machine learning algorithm based on semantic search to provide users with details and lyrics of the searched songs, along with recommended playlists based on the selected song.

## Technologies Used

Machine Learning Algorithm: Developed using the Python library named Qdrant and a transformer to create embedding vectors, based on semantic search.

API Interface: The platform is implemented using FastAPI, providing a robust and fast RESTful interface.

Communication with Spotify: To interact with Spotify and obtain information about songs, the Spotipy library is employed.

## Endpoints

### 1. Collection Creation

Method: POST
Endpoint: /create-collection
Description: This endpoint allows the creation of a collection of songs within the system. Users can provide details of the songs they want to include in the collection.

### 2. Song Search and Recommended Playlists

Method: GET
Endpoint: /search
Description: This endpoint enables users to search for a song in the system. In response, details of the searched song along with lyrics will be returned, along with a list of recommended playlists based on the selected song.
Example Request:

Enjoy exploring and discovering new fantastic songs on SemanticSonora! 🎵✨
