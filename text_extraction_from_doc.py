import os
from langchain.document_loaders import PyPDFLoader, UnstructuredPowerPointLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

class DocumentReader:
    def read_pdf(self, pdf_path):
        """
        Reads and extracts text from a PDF file using LangChain's PyPDFLoader.
        :param pdf_path: Path to the PDF file.
        :return: Extracted text as a string.
        """
        try:
            with open(pdf_path, 'rb') as f:
                header = f.read(4)
            # Check if it's a valid PDF by signature
            if header != b'%PDF':
                raise ValueError("File does not appear to be a valid PDF.")
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()
            return "\n".join([doc.page_content for doc in documents])
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return ""

    def read_pptx(self, pptx_path):
        """
        Reads and extracts text from a PowerPoint file using LangChain's UnstructuredPowerPointLoader.
        :param pptx_path: Path to the PPTX file.
        :return: Extracted text as a string.
        """
        try:
            loader = UnstructuredPowerPointLoader(pptx_path)
            documents = loader.load()
            return "\n".join([doc.page_content for doc in documents])
        except Exception as e:
            print(f"Error reading PPTX: {e}")
            return ""

class DocumentStore:
    def __init__(self):
        self.embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    def store_documents(self, documents, faiss_index_path="faiss_index"):
        """
        Stores document embeddings into FAISS and saves the index to a file.
        :param documents: List of text documents.
        :param faiss_index_path: Path to save the FAISS index.
        """
        try:
            vector_store = FAISS.from_texts(documents, self.embeddings_model)
            vector_store.save_local(faiss_index_path)
            print("Documents successfully stored in FAISS.")
        except Exception as e:
            print(f"Error storing documents in FAISS: {e}")

def process_presentation(file_extension,file_path):
    reader = DocumentReader()
    store = DocumentStore()
    documents_content = []
    # Example file paths (replace with your files)
    if file_extension in {".ppt", ".pptx"}:
        # call embedding function for ppt
        pptx_content = reader.read_pptx(file_path)
        documents_content.append(pptx_content)
        print("PPTX Content Extracted.")
    elif file_extension == ".pdf":
        # call embedding function for pdf
        pdf_content = reader.read_pdf(file_path)
        documents_content.append(pdf_content)
    else:
        return "Unknown error. Could not determine file type."
    # Store extracted content in FAISS
    store.store_documents(documents_content)
    return "Success"


