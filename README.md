# Issue Sphere - Intelligent Diagnostic Cluster Finder

![Issue Sphere Logo](./issue%20sphere.jpg)

Issue Sphere is an intelligent system that uses vector search and AI to find relevant diagnostic clusters for vehicle-related issues. It combines MongoDB's vector search capabilities with Google's Gemini AI to provide accurate and contextual recommendations.

## 🚀 Features

- **Vector-Based Search**: Utilizes MongoDB's vector search for semantic similarity matching
- **AI-Powered Analysis**: Leverages Google's Gemini AI for intelligent cluster recommendations
- **Interactive UI**: Built with Streamlit for a user-friendly experience
- **Real-time Processing**: Instant results with efficient embedding generation
- **Configurable**: Easy configuration using TOML format

## 🛠️ Technical Stack

- **Frontend**: Streamlit
- **Database**: MongoDB Atlas with Vector Search
- **AI Models**: 
  - Google Gemini 1.5 Flash for analysis
  - Nomic AI Embeddings for vector generation
- **Configuration**: TOML
- **Language**: Python 3.8+

## 📋 Prerequisites

- Python 3.8 or higher
- MongoDB Atlas account with Vector Search enabled
- Google Cloud API key with Gemini API access
- Git (for version control)

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/adm003/Issue__Sphere.git

```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `config.toml` file in the project root:
```toml
[mongodb]
uri = "your_mongodb_uri"
database = "myDatabase"
clusters_collection = "oem_clusters"
claims_collection = "oem_claims"

[api]
google_api_key = "your_google_api_key"

[model]
sentence_transformer = "nomic-ai/nomic-embed-text-v1"
gemini_model = "gemini-1.5-flash"

[app]
title = "Cluster Finder for issues"
image_path = "./issue sphere.jpg"
image_width = 150
```

4. Run the application:
```bash
streamlit run appp.py
```

## 🚀 Usage

1. Start the application using the command above
2. Enter a diagnostic issue in the text input field
3. Click "Find Clusters" to search for relevant clusters
4. View the top matching clusters and AI-generated recommendations
5. Use the recommendations to identify the most relevant diagnostic cluster

## 💡 Example Queries

- "Engine making knocking noise at high RPM"
- "Battery not holding charge after overnight parking"
- "Transmission slipping during gear changes"

## 🔐 Security

- Never commit your `config.toml` with sensitive credentials
- Use environment variables for production deployments
- Regularly update dependencies for security patches
- Implement proper access controls in production

## 🛠️ Development Setup

For local development:

1. Create a development config file:
```bash
cp config.toml config.dev.toml
```

2. Run with development configuration:
```bash
APP_CONFIG=config.dev.toml streamlit run appp.py
```

## 🔄 MongoDB Vector Search Setup

Ensure your MongoDB collection has a vector search index:

```javascript
{
  "mappings": {
    "dynamic": true,
    "fields": {
      "embedding": {
        "dimensions": 384,
        "similarity": "cosine",
        "type": "knnVector"
      }
    }
  }
}
```

## 🚀 Deployment

### Streamlit Cloud

1. Push your code to GitHub
2. Connect your repository to Streamlit Cloud
3. Add your configuration as secrets
4. Deploy


## 📊 Performance Optimization

- Uses Streamlit caching for model initialization
- Implements timeout handling for MongoDB operations
- Optimizes vector search with proper indexing
- Caches configuration loading

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request


## 👥 Authors

- Aditya Makhija (@adm003)

## 🙏 Acknowledgments

- Streamlit for the amazing web framework
- MongoDB Team for Vector Search capabilities
- Google for the Gemini API
- Nomic AI for the embedding model

## 📞 Support

For support, email your-email@example.com or create an issue in the repository.

## 🔮 Future Enhancements

- [ ] Add batch processing capabilities
- [ ] Implement user authentication
- [ ] Add export functionality
- [ ] Create API endpoints
- [ ] Add visualization for cluster relationships
- [ ] Implement feedback mechanism

---
*Note: Replace placeholder values (aditya3makhija@gmail.com, @adm003, etc.) with your actual information before publishing.*