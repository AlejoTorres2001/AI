from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

from prompts import MAP_PROMPT_EN, COMBINE_PROMPT_EN

from services.parsers import construct_pdf, parse_json, is_valid_schema, extract_text, get_documents
from services.data import create_embeddings, get_relevant_documents_indexes, get_documents_by_index
from services.inference import create_llm, summarize_docs, synthesis

app = FastAPI()

origins = [
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET,OPTIONS,POST"],
    allow_headers=["*"]
)

#! configurar cors antes de abiente pre-productivo y apikey
#! validar a mano los parametros del json serializado -> files + json models no no se quieren juntos
#! Arquitectura hexagonal para los servicios


@app.post("/summarize")
async def upload_file(file: UploadFile = File(...), parameters: str = Form(...)):
    ###! ---- Schema validations ---- ###
    try:
        parameters = parse_json(parameters)

        if not is_valid_schema(parameters):
            raise Exception("Invalid parameters")
        ###! ---- Data Parsing ---- ###

        pdf_file = await construct_pdf(file)
        full_text = extract_text(pdf_file)

        documents = get_documents(full_text, separators=[
            "\n\n", "\n", "\t"], chunk_size=300, chunk_overlap=75)

        embeddings = create_embeddings(documents)
        doc_indexes = get_relevant_documents_indexes(
            embeddings, num_clusters=5)
        relevant_documents = get_documents_by_index(
            indexes=doc_indexes, docs=documents)

        ###! ---- Inference ---- ###

        llm3 = create_llm(task="summarize")
        summaries = await summarize_docs(llm=llm3, prompt=MAP_PROMPT_EN, input_variables=["text"], documents=relevant_documents)

        llm4 = create_llm(task="synthesize")
        result = await synthesis(llm=llm4, prompt=COMBINE_PROMPT_EN, input_variables=["text"], summary_list=summaries)

        ###! ---- Response ---- ###
        response_data = {"message": "File uploaded successfully",
                         "summary": result}
        return JSONResponse(content=jsonable_encoder(response_data))
    except Exception as e:
        return JSONResponse(content=jsonable_encoder({"message": f"{e}", "summary": "{}"}), status_code=500)
