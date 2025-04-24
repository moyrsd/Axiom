<div align="center" >
  <img width="40%" src="https://github.com/moyrsd/Axiom/blob/e47d34e28b6ff849b3f047344783ca6e3425e39f/root/client/assets/logo_text.png" alt="Axiom logo">
</div>

<div align="center" >
  <p align="center">
    <a href="https://www.youtube.com/playlist?list=PL8wn-1UB8mCD-hUiz2di77vs93YEzZcd8">View Demo</a>
    ·
    <a href="https://github.com/moyrsd/Axiom/issues">Report Bug</a>
    ·
    <a href="https://github.com/moyrsd/Axiom/issues">Request Feature</a>
  </p>
</div>
<div align="center" >
  <img width="100%" src="https://github.com/moyrsd/Axiom/blob/f3940b4d91773ae1cbef2cdd62a0c8fcba6cb314/Assets/Screenshot%20from%202025-04-25%2003-36-20.png" alt="rocket-chat">
</div>

<!-- ABOUT THE PROJECT -->

##  About The Project:
The General-Purpose Document Q&A System is an AI-powered tool designed to extract and answer questions from diverse document formats. It supports PDFs, DOCX, PPTX, XLSX, CSV, JSON, TXT, and images (PNG/JPG) via OCR, and integrates semantic search, structured data handling, and external link crawling for comprehensive knowledge retrieval.


## ✨  Features

- **📄 Multi-format Document Processing**: Handles PDFs, PowerPoint presentations, Word documents, Images, csv and many more ...
- **🤖 Data Analytics** : Answer SQL queries like finding mean, median, mode , then finding the projections
- **🔍 Advanced OCR**: Extract text from images embedded within documents
- **🔎 Semantic Search:** Find information based on meaning, not just keywords
- **📊 Table & Image** Recognition: Process structured data and visual element
- **📝 Source Attribution**: Responses include references to source materials


## 📜 Getting Started

### ⚙️ Installation

1. Clone the repo
    ```sh
    git clone https://github.com/moyrsd/Axiom.git
    ```
2. Setup Frontend
    ```sh
    cd root/client
    npm install
    npm run dev
    ```
    Add your backend url in the .env for eg see the [.env.example file](https://github.com/moyrsd/Axiom/blob/main/root/client/.env.example)
3. Setup Backend

    ```sh
    sudo apt install sqlite3
    sudo apt install poppler-utils
    cd root/server
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
    Add Google Api key in .env file (See [.env.example](https://github.com/moyrsd/Axiom/blob/main/root/server/.env.example) for reference)
   ```sh
    uvicorn main:app --reload
    ```
5. Use the application
   now go to `http://localhost:3000/` to use the application. Upload any pdf file and ask question 
    

## Code Architecture
```sh
root/
├── client/
│   ├── src/
│   │   ├── app/
│   │   │   ├── actions/
│   │   │   │   └── delete_tempfile.ts      # Deletes temporary files (server-side)
│   │   │   └── page.tsx                    # Main page component
│   │   ├── components/
│   │   │   ├── Filesidebar.tsx             # Sidebar for uploaded files
│   │   │   ├── MessageList.tsx             # Displays message responses
│   │   │   └── PromptBox.tsx               # User input box
│   │   ├── interface/
│   │   │   └── Interface.ts                # TypeScript interfaces
│   │   └── pages/api/
│   │       ├── ask.ts                      # API for querying
│   │       └── upload.ts                   # API for uploads
└── server/
    ├── main.py                             # Server entry point
    ├── requirements.txt                    # Python dependencies
    └── src/
        ├── config/
        │   └── constant.py                 # Server constants
        ├── document_processing/
        │   ├── image_parser.py             # Image file processing
        │   ├── pdf_parser.py               # PDF file processing
        │   ├── ppt_parser.py               # PPT file processing
        │   ├── structured_data_parser.py   # Structured data processing
        │   ├── text_parser.py              # Text file processing
        │   └── web_crawl.py                # Web crawling
        ├── prompts/
        │   ├── beautify_prompt.py          # Beautifies user prompts
        │   ├── dataprocessing_prompt.py    # Prepares data processing prompts 
        │   └── ocr_prompt.py               # OCR-related prompts
        ├── routers/
        │   ├── ask.py                      # Routes for querying
        │   ├── delete_tempfiles.py         # Routes for temp file deletion
        │   └── upload.py                   # Routes for file uploads
        └── services/
            ├── convert_to_json.py          # Converts to JSON
            ├── file_processor.py           # File processing workflows
            ├── llm_calls.py                # Interacts with LLMs
            ├── qa_chain.py                 # QA pipeline implementation
            └── vector_store.py             # Vector storage


```

## 🛠️ Technologies Used
#### Backend

- **FastAPI**: High-performance Python framework optimized for building APIs with automatic documentation
- **LangChain**: Framework for developing applications powered by language models
- **ChromaDB**: Vector database for efficient similarity search and metadata storage

#### AI & ML Components

- **Gemini-2.0-Flash**: Multimodal LLM for text generation and image understanding
- **Vector Embeddings**: Semantic representation of document content for intelligent retrieval

#### Document Processing

- **PyMuPDF**: Versatile library for parsing PDFs and extracting complex elements
- **python-pptx**: Advanced toolkit for PowerPoint presentation analysis
- **BeautifulSoup & Requests**: Web content extraction and formatting tools

#### Frontend

- **Next.js**: React framework for building a responsive and dynamic user interface

## 🚀 Processing Pipeline

### 1. Document Upload & Processing

When a user uploads a document, the following process occurs:

1. The client sends the document to the `/upload` API endpoint.Document references are added to the user's sidebar via `Filesidebar.tsx`.
2. The server's `upload.py` router receives the file and initiates processing.
3. Based on the file type, the appropriate parser is selected:
   - `pdf_parser.py` for PDF documents
   - `ppt_parser.py` for PowerPoint presentations
   - `text_parser.py` for plain text files
   - `image_parser.py` for images requiring OCR
   - `structured_data_parser.py` for data files (CSV, Excel, etc.)
   - `web_crawl.py` for processing web content

The `file_processor.py` orchestrates the document processing workflow:
- Text extraction
- Chunking content appropriately with source metadata

### 2. Knowledge Indexing

After processing:
1. The extracted content `vector_store.py` generates embeddings and stores them in ChromaDB along with metadata.

### 3. Query & Response Generation

When a user submits a question:
1. The query is sent from `PromptBox.tsx` to the `/ask` API endpoint.
2. `ask.py` router processes the request and directs it to the appropriate service.
3. 4. `qa_chain.py` implements the RAG pipeline:
   - Converts the query to a vector representation.
   - Retrieves relevant document chunks from ChromaDB.
   - Formats context and query for the LLM.
   - Processes the response to include source attribution.
4. `beautify_prompt.py` refines the user's query for optimal retrieval.


The response is returned to the client, where `MessageList.tsx` displays it to the user in proper markdown format 

### 4. Cleanup & Maintenance

- Temporary files are managed through `delete_tempfiles.py` on the server.
- Client-side cleanup is handled by `delete_tempfile.ts` server action.



## 🧑‍💻 Contributing
Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue.
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feat/AmazingFeature`)
3. Commit your Changes (`git commit -m 'feat: adds some amazing feature'`)
4. Push to the Branch (`git push origin feat/AmazingFeature`)
5. Open a Pull Request








