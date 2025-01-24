# Mini-RAG-App

Mini-RAG-App is an intelligent question-answering application designed to process and retrieve precise information from user-provided data. When users submit queries, the app identifies the most relevant answers based on similarity and delivers accurate responses. If a question falls outside the scope of the provided data, the app will respond by indicating that the requested information is not available within its knowledge base.

## How It Works

1. **Data Ingestion**: Users upload data files (e.g., `.txt` or `.pdf` formats) to the application.
2. **Validation**: The app checks the format and structure of the uploaded files to ensure they are valid.
3. **Data Chunking**: After validation, the data is split into smaller chunks for more efficient processing and retrieval.
4. **Data Storage**: The processed data chunks are stored in MongoDB (Studio 3T).
5. **Vectorization**: The data chunks are converted into vectors using Qdrant, enabling fast similarity-based searches.
6. **Query Processing**: Upon query submission, the app vectorizes the query and performs a similarity search to find the most relevant data chunks.
7. **Handling Out-of-Scope Queries**: If the query doesn't match the data, the app will not provide a response.

## Technologies Used

- **Backend**: FastAPI, Python
- **AI/ML Tools**: OpenAI API, Cohere API
- **Vector Database**: Qdrant
- **Database**: MongoDB (Studio 3T)
- **Containerization**: Docker
- **Architecture**: MVC (Model-View-Controller)

## How to Install and Run the Application

### Prerequisites

Before you can run the application, you need to install the following tools:

1. **Install Miniconda (if Conda is not installed)**:
   - If you don’t have Conda installed, download and install **Miniconda** from [here](https://docs.conda.io/en/latest/miniconda.html). Miniconda is a lightweight version of Conda.
   - Once Miniconda is installed, verify the installation by running:
     ```bash
     conda --version
     ```

2. **[Visual Studio Code (VSCode)](https://code.visualstudio.com/)**
   - Install Visual Studio Code for a powerful and lightweight code editor.

3. **[Docker](https://www.docker.com/get-started)**
   - Docker is optional for containerizing the application.
   - Docker allows you to run the app in an isolated environment.
   Once Docker is installed:
   - Start Docker Desktop and make sure it's running.

4. **[Rustup](https://rustup.rs/)**
   - Rustup is the Rust programming language installer. It's necessary for any development involving Rust-based dependencies.

5. **[Studio 3T MongoDB](https://studio3t.com/)**
   - **Studio 3T** is a MongoDB GUI tool used to manage and query your MongoDB instance.
   
6. **[Postman](https://www.postman.com/downloads/)**
   - Postman is used for testing APIs and sending HTTP requests.

---

### Installation Steps

1. **Clone the Repository**:
   - Open **VSCode** and open the terminal in VSCode (`Ctrl + ~`).
   - Clone the repository by running:
     ```bash
     git clone https://github.com/neny-1/Mini-QA-App.git
     cd Mini-QA-App
     ```

2. **Create a Conda Environment**:
   - In the terminal, create a Conda environment for the project:
     ```bash
     conda create -n mini-qa-app-env python=3.9
     ```
   - Activate the environment:
     ```bash
     conda activate mini-qa-app-env
     ```

3. **Install Dependencies**:
   - Install all the required dependencies from the `requirements.txt` file:
     ```bash
     pip install -r requirements.txt
     ```

4. **Navigate to the `src` Folder**:
   - Before setting environment variables, navigate to the `src` folder:
     ```bash
     cd src
     ```

5. **.env Configuration **:
   - Copy the example environment file:
     ```bash
     cp .env.example .env
     ```
   - **Set API Keys**:  
     Open `.env` and set the required variables, such as `COHERE_API_KEY` or `OPENAI_API_KEY`, for the app to function properly.
   
   - **Set Language**:  
     You can also set the primary language for data processing and generation by configuring the `PRIMARY_LANG` variable in `.env`. The available languages are:
     - `ar` for Arabic
     - `en` for English
   ---
### Run the Application

1. **Run Docker Using Docker Compose**:
  - Navigate to `docker-compose.yml` file is located in docker folder.
  - Right-click and select **Compose Up** (if using Docker Desktop).

   This will start all the services defined in the `docker-compose.yml` file, including MongoDB.

2. **Navigate to the `src` Folder**:
   - In the terminal, navigate to the `src` directory where the main app code is located:
     ```bash
     cd src
     ```

3. **Run the App Using Uvicorn**:
   - Once inside the `src` directory, start the app using Uvicorn:
     ```bash
     uvicorn main:app --reload --host 0.0.0.0 --port 8080
     ```
   - This command will start the FastAPI app and make it accessible at [http://127.0.0.1:8080](http://127.0.0.1:8080).

4. **Verify the Application**:
   - Open your browser and navigate to [http://127.0.0.1:8080](http://127.0.0.1:8080). You should see the FastAPI interactive documentation for the app.

---


### Next Steps

Once the app is running, you can proceed with setting up the database and testing the app using Postman.

---

### Database Setup

1. **Connecting to MongoDB Using Studio 3T**:
   - Open **Studio 3T** and click on **Connect** to create a new connection and select Manually configure my connection settings.
   - Set the connection details as:
     - **Host**: `localhost` 
     - **Port**: `27017`
   - Select **Test Connection** to ensure it's working.
---

### Using Postman to Test the Application

Once the app is running, and the database is set up, you can use Postman to send queries to your app.
# Postman API Requests for Mini-QA-App

You can use Postman to test the endpoints of the Mini-QA-App by making HTTP requests to the routes. Below is a list of available API routes and the expected methods, URLs, and request bodies.

### 1. **Welcome Route** - `GET /`
   - **URL**: `http://127.0.0.1:8080/`
   - **Method**: `GET`
   - **Description**: This is the welcome route to check if the server is running.
   - **Response**: A basic message indicating the status of the application.
   ![image](https://github.com/user-attachments/assets/ff553e26-adf8-4504-a8da-bb8f8dbfc656)


---

### 2. **Upload Data File** - `POST /upload/{project_id}`
   - **URL**: `http://127.0.0.1:8080/upload/1`  
     *(Replace `1` with your project ID, where the same topic or field will share the same project ID.)*
   - **Method**: `POST`
   - **Request Body**: 
     - This request uploads the data file into assets folder.
     - The file should be uploaded in the `file` parameter.
   ![image](https://github.com/user-attachments/assets/c32edd55-b2b5-46c0-99ff-19a75ba23507)
---

### 3. **Process Data File** - `POST /process/{project_id}`
   - **URL**: `http://127.0.0.1:8080/process/1`  
     *(Replace `1` with your project ID)*
   - **Method**: `POST`
   - **Request Body**:
     ```json
     {
       "chunk_size": 300,
       "overlap_size": 5,
       "do_reset": 1
     }
     ```
   - **Description**: This route processes the uploaded data file with chunk size, overlap size, and a flag for resetting.
     ![image](https://github.com/user-attachments/assets/788816c7-eee9-40a3-a083-aa029edfffad)

---

### 4. **Store Chunks into vector DB** - `POST /store/{project_id}`
   - **URL**: `http://127.0.0.1:8080/store/1`  
     *(Replace `1` with your project ID)*
   - **Method**: `POST`
   - **Description**: This route stores the processed data chunks into the database.
     ![image](https://github.com/user-attachments/assets/545a34a9-a41f-4d07-aa67-8f0760ff7cf4)


---

### 5. **Vector DB Info** - `GET /info/{project_id}`
   - **URL**: `http://127.0.0.1:8080/info/1`  
     *(Replace `1` with your project ID)*
   - **Method**: `GET`
   - **Description**: This route provides information about the vector database for the given project.
     ![image](https://github.com/user-attachments/assets/a8d1e191-ba13-4801-bfbc-28e058cc05d9)


---

### 6. **Similarity Search** - `POST /search/{project_id}`
   - **URL**: `http://127.0.0.1:8080/search/1`  
     *(Replace `1` with your project ID)*
   - **Method**: `POST`
   - **Request Body**:
     ```json
     {
       "query": "Your search query",
       "limit": 5
     }
     ```
   - **Description**: This route performs a similarity search based on the provided query. You can specify the number of results with the `limit` field.
     ![image](https://github.com/user-attachments/assets/65d7ac92-f029-49bf-aa2e-a24262435724)

---

### 7. **Generate Response** - `POST /generate/{project_id}`
   - **URL**: `http://127.0.0.1:8080/generate/1`  
     *(Replace `1` with your project ID)*
   - **Method**: `POST`
   - **Request Body**:
     ```json
     {
       "query": "Your query here",
       "limit": 1
     }
     ```
   - **Description**: This route generates a response based on the provided query. The `limit` specifies how many results to return.
     ![image](https://github.com/user-attachments/assets/0606342b-56ac-48ea-963e-72c9e99eb882)
---

### How to Test the API Endpoints

1. Open **Postman**.
2. Choose the **HTTP method** (`GET` or `POST`) for your request.
3. Enter the **URL** (replace the `project_id` or query parameters as needed).
4. If it’s a **POST** request, set the request body accordingly.
5. Click **Send** to test the route.
6. Review the response from the API to ensure it’s working correctly.

To test any of the routes, use the following API links:

- **Welcome**: `http://127.0.0.1:8080/` (GET)
- **Upload Data File**: `http://127.0.0.1:8080/upload/{project_id}` (POST, where `{project_id}` is the ID for the project/topic)
- **Process Data File**: `http://127.0.0.1:8080/process/{project_id}` (POST, takes JSON body with `"chunk_size"`, `"overlap_size"`, and `"do_reset"`)
- **Store Chunks into DB**: `http://127.0.0.1:8080/store/{project_id}` (POST)
- **Vector DB Info**: `http://127.0.0.1:8080/info/{project_id}` (GET)
- **Similarity Search**: `http://127.0.0.1:8080/search/{project_id}` (POST, requires `"query"` and `"limit"`)
- **Generate**: `http://127.0.0.1:8080/generate/{project_id}` (POST, requires `"query"` and `"limit"`)
---
### Testing
  
#### Sample Data Source
The sample data used as source from the following website:  
[https://www.nasaaem.com/ar/medical-information](https://www.nasaaem.com/ar/medical-information)

#### Data Folder Link
After converting the data to PDF files, the data files can be accessed from the following Google Drive folder:  
[https://drive.google.com/drive/folders/1fqhXkQPBtndhrN15-KMXGaI3JTFL_wy6?usp=drive_link](https://drive.google.com/drive/folders/1fqhXkQPBtndhrN15-KMXGaI3JTFL_wy6?usp=drive_link)

Include test cases for the following scenarios:

- **Queries with Answers in the Data**: Ensure the app retrieves and generates accurate responses based on the uploaded data.
  ![image](https://github.com/user-attachments/assets/3ddcc076-2fde-455c-8c68-19586430a813)

  ![image](https://github.com/user-attachments/assets/bfa7c14c-34e6-4b39-bea7-bd62a1ef9150)
- **Out-of-Scope Queries**: Validate that the app does not provide answers when the query is unrelated to the uploaded data.
  ![image](https://github.com/user-attachments/assets/f3395084-01d5-45d3-a245-1d3a5c710bb8)
  ![image](https://github.com/user-attachments/assets/60ca2ce2-fcce-421a-8454-2fae61cfa333)

- **Edge Cases**:
  - Empty queries
    ![image](https://github.com/user-attachments/assets/821fb1bd-c45e-483b-bdf7-70f0f904eb80)
    ![image](https://github.com/user-attachments/assets/25332ef3-8cc3-4784-9d83-2db16d964c1b)

  - Extremely long queries
    ![image](https://github.com/user-attachments/assets/997c8d44-ce90-4fb0-8e7d-68e13c6316dc)

  - Invalid file uploads
    ![image](https://github.com/user-attachments/assets/d2cd9c0a-8bd0-442d-a5fe-9df9e485cdcf)


### Project Architecture and code structure 

This project follows a **Model-View-Controller (MVC)** architecture to ensure a clean separation of concerns and enhance scalability. Below is the breakdown of the directory structure and its components:

#### Project Structure

This project is designed to ensure modularity and maintainability. Below is an overview of the main folders and their purposes.

###### 1. **`assets/`**
   - Purpose: To store data files and vector database files.
   - Contains:
     - Files necessary for data storage 
     - Vector database-related resources.

###### 2. **`controllers/`**
   - Purpose: Contains the core logic of the application.

###### 3. **`models/`**
   - Purpose: Manages all database-related operations.
   - Contains:
     - **`db_schemes/`**: Defines database schemas.
     - **`enums/`**: Enumerations for handling constants and response types.

###### 4. **`routes/`**
   - Purpose: Manages API routes and their corresponding request/response schemas.
   - Contains:
     - Logic to define and handle application routes.

###### 5. **`stores/`**
   - Purpose: Manages LLM configurations, vector database logic, and state management.
   - Contains:
     - **`llm/`**: Manages large language models (LLMs).
       - **`providers/`**: Configurations and integrations for providers like OpenAI and Cohere.
       - **`templates/`**:
         - **`locales/`**: Localization templates for different languages.
           - **`ar/`**: Arabic templates.
           - **`en/`**: English templates.
     - **`vectordb/`**: Handles vector database logic and integrations.
       - Includes the `QdrantProvider.py` file for managing Qdrant, the vector database provider.

##### Environment Files

- **`.env`**: Stores sensitive environment variables (e.g., API keys, database credentials).
- **`.env.example`**: Example environment file to guide setup for new developers.

#### Supporting Files

- **`main.py`**: The main entry point of the application.
- **`requirements.txt`**: Lists all the Python dependencies required to run the application.

This structure promotes modularity, ease of maintenance, and scalability, making it suitable for a variety of use cases.


### Future Development

This application requires further enhancements, especially in the **LLM (Large Language Models)** part, to achieve satisfactory results in the **medical field**.

### Resources

I used this [Mini RAG Playlist](https://www.youtube.com/playlist?list=PLvLvlVqNQGHCUR2p0b8a0QpVjDUg50wQj) as a resource and followed its project architecture. It provided valuable inspiration and guidance in building this application.


    


