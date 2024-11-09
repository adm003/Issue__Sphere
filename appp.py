import streamlit as st
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the embedding model and Google Gemini API
@st.cache_resource
def initialize_models():
    model = SentenceTransformer("nomic-ai/nomic-embed-text-v1", trust_remote_code=True)
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    return model, genai.GenerativeModel("gemini-1.5-flash")

# MongoDB connection with error handling
@st.cache_resource
def initialize_mongodb():
    try:
        # Use the connection string from environment variable or default to your direct string
        mongo_uri = os.getenv("MONGODB_URI")
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        # Verify connection
        client.server_info()
        db = client["myDatabase"]
        return db
    except Exception as e:
        st.error(f"Failed to connect to MongoDB: {str(e)}")
        return None

# Helper function to generate embeddings
def get_embedding(model, data):
    return model.encode(data).tolist()

def main():
    st.image("./issue sphere.jpg", width=150)
    st.title("Cluster Finder for issues")

    # Initialize models
    model, gemini_model = initialize_models()

    # Initialize MongoDB
    db = initialize_mongodb()
    
    if db is None:
        st.error("Cannot proceed without MongoDB connection. Please check your connection string.")
        return

    collection_clusters = db["oem_clusters"]
    collection_claims = db["oem_claims"]

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
                            "limit": 5
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