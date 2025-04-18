<div align="center">
<img width=40% src="https://github.com/moyrsd/Axiom/blob/e47d34e28b6ff849b3f047344783ca6e3425e39f/root/client/assets/logo_text.png" alt="rocket-chat">
</div>



<!-- ABOUT THE PROJECT -->

##  About The Project:
The General-Purpose Document Q&A System is an AI-powered tool designed to extract and answer questions from diverse document formats. It supports PDFs, DOCX, PPTX, XLSX, CSV, JSON, TXT, and images (PNG/JPG) via OCR, and integrates semantic search, structured data handling, and external link crawling for comprehensive knowledge retrieval.


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
3. Setup Backend

    ```sh
    cd root/server
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    # Add Google Api key in .env file (See .env.example for reference)
    uvicorn main:app --reload
    ```
4. Use the application
   now go to `http://localhost:3000/` to use the application. Upload any pdf file and ask question 
    





