# SemanticSonora

## Overview

This repository contains the source code for a music recommendation platform that leverages a state-of-the-art machine learning algorithm for semantic search. The platform allows users to search for a specific song and provides detailed information about the song, including its lyrics. Additionally, it offers curated playlists based on the searched song using advanced recommendation algorithms.

## Features

- Semantic Search: The core of the platform is powered by a machine learning algorithm developed using the Qdrant library for semantic search. This allows users to search for songs not just by keywords but also by capturing the semantic meaning of the query.

- Sentence Transformers: The semantic search algorithm utilizes Sentence Transformers, a cutting-edge Python library, for embedding text and generating vectors that capture the semantic similarity between songs.

- FastApi Interface: The platform is built using FastApi, a modern, fast web framework for building APIs with Python. The FastApi interface ensures efficient communication between the user interface and the backend, providing a seamless experience.

- Spotify Integration: To fetch and display detailed information about songs, as well as to generate playlists, the platform communicates with Spotify using the Spotipy library. This integration enhances the user experience by offering a wide range of songs and rich metadata.

## Prerequisites

Before running the platform, make sure you have the following installed:

- Qdrant library
- Sentence Transformers library
- FastApi
- Spotipy

## How it Works

Search for a Song: Users can enter the name of a song they are interested in.

- Semantic Search: The platform processes the query using the semantic search algorithm, providing detailed information about the searched song, including lyrics.

- Playlist Recommendations: Based on the searched song, the platform generates playlists using advanced recommendation algorithms, offering users a curated list of songs related to their preferences.

## Contributing

Feel free to contribute to the development of this platform by creating issues, submitting pull requests, or suggesting improvements.
