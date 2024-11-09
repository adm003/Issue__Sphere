import streamlit as st
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
import pymongo

# Initialize the embedding model and Google Gemini API
model = SentenceTransformer("nomic-ai/nomic-embed-text-v1", trust_remote_code=True)
genai.configure(api_key="GEMINI_API_KEY")
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

# MongoDB setup
client = MongoClient("MONGO_URI")
db = client["myDatabase"]
collection_clusters = db["oem_clusters"]
collection_claims = db["oem_claims"]

# Helper function to generate embeddings
def get_embedding(data):
    return model.encode(data).tolist()

st.image("/content/issue sphere.jpg",width = 150)
# Streamlit UI setup
st.title("Cluster Finder for issues")
prompt = st.text_input("Enter a diagnostic issue to find relevant clusters:")

if st.button("Find Clusters"):
    if prompt:
        # Generate embedding for the input prompt
        query_embedding = get_embedding(prompt)

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

        # Execute the search
        results = list(collection_clusters.aggregate(pipeline))

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
    else:
        st.write("Please enter a prompt.")
