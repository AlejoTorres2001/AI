from fastapi import  UploadFile
from PyPDF2 import PdfReader
import io
from fastapi.encoders import jsonable_encoder

async def construct_pdf(file:UploadFile,strict:bool=False, password:str=None) -> PdfReader:
  raw_file_content = await file.read()
  bytes_stream = io.BytesIO(raw_file_content)
  
  pdf_file = PdfReader(bytes_stream, strict=strict, password=password)
  
  return pdf_file

def parse_json(string:str) -> dict:
  return jsonable_encoder(string)

def is_valid_schema(json_data:dict) -> bool:
  #TODO: define parameters and validation rules
  return False