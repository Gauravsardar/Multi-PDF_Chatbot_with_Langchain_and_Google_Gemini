# Chat with PDF using Gemini 💁

![image](https://github.com/user-attachments/assets/9b0b4043-80e5-47db-8968-6fa0186da503)

This project is a Streamlit application that allows users to upload multiple PDF files, ask questions based on their content, and generate summaries for selected PDFs. The app leverages Google's Generative AI models, FAISS for vector search, and Sumy for text summarization.

## Features

- **Upload Multiple PDFs**: Users can upload one or more PDF files.
- **Interactive Q&A**: Ask questions about the content of the uploaded PDFs.
- **PDF Summarization**: Generate summaries for selected PDFs.
- **PDF Selection**: Choose specific PDFs to generate or view summaries.

## Installation

To run this application locally, follow these steps:

1. **Clone the repository:**

```bash
   git clone https://github.com/Gauravsardar/Multi-PDF_Chatbot_with_Langchain_and_Google_Gemini.git
   cd Multi-PDF_Chatbot_with_Langchain_and_Google_Gemini
```

2. **Create a virtual environment (optional but recommended):**

- **On Windows**:
     
```bash
   python -m venv env
  .\env\Scripts\activate
  ```

- **On macOS**:

```bash
  python3 -m venv env
  source env/bin/activate
   ```

3. **Install the dependencies**:
   
```bash
  pip install -r requirements.txt
   ```
4. **Set up environment variables**:
Create a .env file in the project root directory and add your Google API key
```bash
  GOOGLE_API_KEY=your_google_api_key
   ```

5. **Run the Streamlit app**:
```bash
  streamlit run app.py
   ```   
