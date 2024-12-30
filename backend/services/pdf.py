import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma


async def process_pdf(file_content: bytes) -> str:
    """Process PDF content and extract text"""
    pdf_document = fitz.open(stream=file_content, filetype="pdf")
    text = ""
    for page in pdf_document:
        text += page.get_text()
    return text

async def create_vector_store(text: str, doc_id: str) -> None:
    """Create a vector store from text"""
    # Placeholder for actual vector store creation
    text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
    texts = text_splitter.split_text(text)
        
    # Create and persist vector store
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_texts(
            texts,
            embeddings,
            persist_directory=f"vectorstore/{doc_id}"
        )
    vectorstore.persist()