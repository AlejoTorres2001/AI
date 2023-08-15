from fastapi import  UploadFile
from PyPDF2 import PdfReader
import io
from fastapi.encoders import jsonable_encoder
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

async def construct_pdf(file:UploadFile,strict:bool=False, password:str=None) -> PdfReader:
  raw_file_content = await file.read()
  bytes_stream = io.BytesIO(raw_file_content)
  
  pdf_file = PdfReader(bytes_stream, strict=strict, password=password)
  
  return pdf_file

def parse_json(string:str) -> dict:
  return jsonable_encoder(string)

def is_valid_schema(json_data:dict) -> bool:
  #TODO: define parameters and validation rules
  return True

def extract_text(pdf_file:PdfReader) -> str:
    full_text = "\n\n".join([page.extract_text() for page in pdf_file.pages])
    full_text = full_text.replace('\t', ' ')
    return full_text
  
def get_documents(text:str,separators:list[str],chunk_size:int,chunk_overlap:int) -> list[Document]:
    text_splitter = RecursiveCharacterTextSplitter(separators=separators, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    documents = text_splitter.create_documents([text])
    return documents
    
  