# Issue Sphere - Cluster Matching App

## Overview

Issue Sphere is a web app that connects user prompts to the most relevant information clusters by leveraging NLP embeddings, clustering, and similarity scoring. Built for efficient information retrieval, the app is ideal for cases where users need highly relevant information quickly from large datasets.

## How It Works

1. **User Input**: The app interface, built with **Streamlit**, allows users to enter prompts. This interface makes it easy for users to interact with the backend.

2. **Issue Sphere Processing**: Once a prompt is submitted, it's handled by **Issue Sphere** and sent to the backend for deeper processing.

3. **Embeddings Creation with Sentence Transformers**: In the backend, **Sentence Transformers** are used to create embeddings for both the user’s prompt and the stored documents. These embeddings are dense vectors representing the semantic meaning of the text, making it easier to match similar content.

4. **Data Management with MongoDB Atlas**:
   - **Storage**: All documents, claims, and clusters are stored in **MongoDB Atlas** for scalability and flexibility.
   - **Aggregation Pipeline**: An aggregation pipeline identifies the **top 5 clusters** based on similarity to the user’s prompt.

5. **Gemini API 1.5 Flash**: The top 5 clusters identified in MongoDB are refined further by **Gemini API 1.5 Flash**. This API performs advanced similarity ranking to select the single best-matching cluster.

6. **Result Display**: The app returns the most relevant cluster to the user in the Streamlit interface, providing a targeted response to their prompt.

## Tech Stack

- **Streamlit**: Provides an interactive user interface.
- **MongoDB Atlas**: A cloud-based NoSQL database for document storage and data aggregation.
- **Sentence Transformers**: NLP models used to generate embeddings for semantic similarity.
- **Gemini API 1.5 Flash**: API for ranking and refining results based on similarity scoring.

## Features

- **Fast Information Retrieval**: The app efficiently narrows down relevant clusters, providing the most relevant result to the user.
- **Advanced NLP Matching**: Using embeddings for semantic similarity ensures a more accurate match compared to simple keyword searches.
- **Scalable Data Management**: MongoDB Atlas supports large datasets and allows for complex data processing with its aggregation pipeline.

## Ideal Use Cases

This app is well-suited for:
- Research projects requiring access to clustered, topic-specific information.
- Customer support solutions that need quick access to relevant information.
- Knowledge exploration tools that connect users to highly relevant content clusters.
- Hackathons or prototype environments where rapid, accurate data retrieval is essential.

## Setup

1. Clone the repository:
```bash
git clone https://github.com/adm003/Issue__Sphere.git
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
   - Create a `.env` file with your API keys and MongoDB URI
   - Never commit this file to GitHub

4. Run the application:
```bash
streamlit run appp.py
```

## Features

- Vector search using MongoDB
- Semantic similarity using SentenceTransformer
- AI-powered recommendations using Google Gemini
- Interactive UI with Streamlit

## Security Note

Make sure to:
- Never commit API keys or sensitive credentials
- Use environment variables for all sensitive information
- Keep your dependencies updated

