# mini-rag-app

This is a practical project based on the Retrieval-Augmented Generation (RAG) model for question answering. The project is from Abu Bakr Soliman YouTube channel, and here is the playlist link: [YouTube Playlist](https://www.youtube.com/playlist?list=PLvLvlVqNQGHCUR2p0b8a0QpVjDUg50wQj). You can also find the project repository on GitHub at this link: [GitHub Project](https://github.com/bakrianoo/mini-rag/tree/main).

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

