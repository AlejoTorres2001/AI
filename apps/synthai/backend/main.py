from fastapi import FastAPI, File, UploadFile,Form
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

from langchain.text_splitter import RecursiveCharacterTextSplitter

from services.parsers import construct_pdf,parse_json,is_valid_schema

app = FastAPI()

origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#! configurar cors antes de abiente pre-productivo y apikey
#! validar a mano los parametros del json serializado -> files + json models no no se quieren juntos
#! Arquitectura hexagonal para los servicios 

@app.post("/upload")
async def upload_file(file: UploadFile = File(...),data: str = Form(...)):
    parameters = parse_json(data)
    
    if not is_valid_schema(parameters):
        return JSONResponse(content={"message": "Invalid data"})
    
    pdf_file = await construct_pdf(file)
    
    text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n"], chunk_size=2000, chunk_overlap=250)
    
    full_text = "\n\n".join([page.extract_text() for page in pdf_file.pages])
    text_chunks = text_splitter.split_text(full_text)
    
    
    
    
    response_data = {"message": "File uploaded successfully", "json_data": parameters}
    return JSONResponse(content=jsonable_encoder(response_data))
