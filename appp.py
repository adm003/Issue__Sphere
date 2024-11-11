import os
from dotenv import load_dotenv
import streamlit as st
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
import toml
from config import MONGODB_URI, GOOGLE_API_KEY
mongo_uri = MONGODB_URI
google_api_key = GOOGLE_API_KEY

# Load configuration
@st.cache_resource
def load_config():
    try:
        return toml.load("config.toml")
    except Exception as e:
        st.error(f"Failed to load configuration: {str(e)}")
        return None

# Initialize the embedding model and Google Gemini API
@st.cache_resource
def initialize_models(config):
    model = SentenceTransformer(config["model"]["sentence_transformer"], trust_remote_code=True)
    genai.configure(api_key=google_api_key)
    return model, genai.GenerativeModel(config["model"]["gemini_model"])

# MongoDB connection with error handling
@st.cache_resource
def initialize_mongodb(config):
    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        # Verify connection
        client.server_info()
        db = client[config["mongodb"]["database"]]
        return db
    except Exception as e:
        st.error(f"Failed to connect to MongoDB: {str(e)}")
        return None

# Function to generate embeddings
def get_embedding(model, data):
    return model.encode(data).tolist()

def main():
    # Load configuration
    config = load_config()
    if config is None:
        st.error("Cannot proceed without configuration. Please check config.toml file.")
        return

    # Setup page
    st.image(config["app"]["image_path"], width=config["app"]["image_width"])
    st.title(config["app"]["title"])

    # Initialize models
    model, gemini_model = initialize_models(config)

    # Initialize MongoDB
    db = initialize_mongodb(config)
    
    if db is None:
        st.error("Cannot proceed without MongoDB connection. Please check your connection string.")
        return

    collection_clusters = db[config["mongodb"]["clusters_collection"]]
    collection_claims = db[config["mongodb"]["claims_collection"]]

    prompt = st.text_input("Enter a diagnostic issue to find relevant clusters:")

    if st.button("Find Clusters"):
        if prompt:
            try:
                # Generate embedding for the input prompt
                query_embedding = get_embedding(model, prompt)

                # Vector search pipeline
                pipeline = [
                    {
                        "$vectorSearch": {
                            "index": "vector_index",
                            "queryVector": query_embedding,
                            "path": "embedding",
                            "exact": True,
                            "limit": 3
                        }
                    },
                    {
                        "$project": {
                            "_id": 0,
                            "Cluster #": 1,
                            "Cluster Name": 1,
                            "Description": 1,
                            "score": {
                                "$meta": "vectorSearchScore"
                            }
                        }
                    }
                ]

                # Execute the search with timeout handling
                results = list(collection_clusters.aggregate(pipeline, maxTimeMS=30000))

                if not results:
                    st.warning("No clusters found matching your query.")
                    return

                # Display the top 3 results
                top_clusters = []
                for i, cluster in enumerate(results):
                    cluster_info = f"Cluster #{cluster['Cluster #']}: {cluster['Cluster Name']}\n" \
                                f"Description: {cluster['Description']}\nScore: {cluster['score']}\n"
                    st.write(f"**Cluster {i + 1}:**\n{cluster_info}")
                    top_clusters.append(cluster_info)

                if len(top_clusters) == 3:
                    # Prepare prompt for Gemini
                    gemini_prompt = f"""
                    You are an expert vehicle diagnostics assistant. Based on the following cluster information,
                    suggest which cluster best addresses the issue of "{prompt}", and explain your reasoning:

                    {top_clusters[0]}

                    {top_clusters[1]}

                    {top_clusters[2]}

                    Which cluster would you recommend, and why?
                    """
                    # Generate response from Google Gemini
                    response = gemini_model.generate_content(gemini_prompt)
                    st.subheader("Gemini Recommendation")
                    st.write(response.text)
                else:
                    st.write("Not enough clusters returned from the search.")

            except Exception as e:
                st.error(f"An error occurred while processing your request: {str(e)}")
        else:
            st.write("Please enter a prompt.")

if __name__ == "__main__":
    main()