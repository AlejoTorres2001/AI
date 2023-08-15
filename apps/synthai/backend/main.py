from fastapi import FastAPI, File, UploadFile,Form
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware


from services.parsers import construct_pdf,parse_json,is_valid_schema,extract_text,get_documents
from services.data import create_embeddings,get_relevant_documents_indexes,get_documents_by_index
from prompts import MAP_PROMPT_EN,COMBINE_PROMPT_EN
from services.inference import create_map_summarization_chain,create_llm,summarize_docs,synthesis
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
    full_text = extract_text(pdf_file)
    
    documents = get_documents(full_text,separators=["\n\n", "\n","\t"],chunk_size=300,chunk_overlap=75)
    
    embeddings = create_embeddings(documents)
    doc_indexes = get_relevant_documents_indexes(embeddings,num_clusters=5)
    relevant_documents = get_documents_by_index(indices=doc_indexes,docs=documents)
    
    llm3 = create_llm(task="summarize")
    summarization_chain= create_map_summarization_chain(llm=llm3,prompt=MAP_PROMPT_EN,input_variables=["text"])
    
    summaries = summarize_docs(map_chain=summarization_chain,documents=relevant_documents)
    
    llm4 = create_llm(task="synthesize")
    result = await synthesis(llm=llm4,prompt=COMBINE_PROMPT_EN,input_variables=["text"],summary_list=summaries)
    print("---this is the full result---",result)
    response_data = {"message": "File uploaded successfully", "json_data": parameters}
    return JSONResponse(content=jsonable_encoder(response_data))