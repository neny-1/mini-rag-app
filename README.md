# Retrieval-Augmented Generation (RAG) App

An AI-powered application that leverages Retrieval-Augmented Generation (RAG) to provide accurate and context-aware responses. The app ingests data files, processes them into a knowledge base, and delivers user-specific answers through an interactive API.

## Features
- Upload data files in `.txt` and `.pdf` formats to create a searchable knowledge base.
- Retrieve precise and contextually relevant responses based on user queries.
- Scalable and modular design using the **MVC architecture**.
- Powered by **Qdrant** for high-performance vector-based search.
- Integrated with **Ollama** for enhanced AI capabilities.
- Future Plans: Extend support for more file formats.

## Technologies Used
- **Backend:** FastAPI, Python
- **AI/ML Tools:** OpenAI API, Cohere API, Ollama
- **Vector Database:** Qdrant
- **Database:** MongoDB
- **Containerization:** Docker
- **Architecture:** MVC (Model-View-Controller)

## How It Works
1. **Data Ingestion:** Upload a `.txt` or `.pdf` file containing data to the app.
2. **Knowledge Base Creation:** The app processes the file and converts it into a vectorized format using Qdrant and AI models.
3. **Query Processing:** Users can query the app via API endpoints, and the app retrieves the most relevant answers from the knowledge base.

## Requirements

- Python 3.8 or later

### Install Python using MiniConda

1) Download and install MiniConda from [here](https://docs.anaconda.com/free/miniconda/#quick-command-line-install)
2) Create a new environment using the following command:
   ```bash
   $ conda create -n mini-rag python=3.8

### (Optional) Setup you command line interface for better readability

```bash
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "
```

## Installation

### Install the required packages

```bash
$ pip install -r requirements.txt
```

### Setup the environment variables

```bash
$ cp .env.example .env
```

Set your environment variables in the `.env` file. Like `OPENAI_API_KEY` value.


This is a practical project based on the Retrieval-Augmented Generation (RAG) model for question answering. The project is from Abu Bakr Soliman YouTube channel, and here is the playlist link: [YouTube Playlist](https://www.youtube.com/playlist?list=PLvLvlVqNQGHCUR2p0b8a0QpVjDUg50wQj). You can also find the project repository on GitHub at this link: [GitHub Project](https://github.com/bakrianoo/mini-rag/tree/main).
