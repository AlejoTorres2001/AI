from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

from prompts import MAP_PROMPT_EN, COMBINE_PROMPT_EN

from services.parsers import construct_pdf, parse_json, validate_schema, extract_text, get_documents
from services.data import create_embeddings, get_relevant_documents_indexes, get_documents_by_index
from services.inference import create_llm, summarize_docs, synthesis

from models.responseModels import SuccessResponse
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


@app.post("/summarize", description="Summarize a pdf file", summary="Summarize the text content of a document in PDF format using LLMs and clustering", tags=["Summarize"], response_model=SuccessResponse, response_description="returns a JSON object containing the summary of the document and a message indicating information about the status of the request")
async def upload_file(file: UploadFile = File(..., description="a document in PDF format containing the text to be summarized"), parameters: str = Form(..., description="a JSON object containing the parameters for the summarization process, must be serialized into a string")):
    ###! ---- Schema validations ---- ###
    try:
        parsed_json = parse_json(parameters)
        model_parameters = validate_schema(parsed_json)
        print(model_parameters)
        ###! ---- Data Parsing ---- ###
        pdf_file = await construct_pdf(file)
        full_text = extract_text(pdf_file,start=model_parameters.from_page, finish =model_parameters.to_page)

        documents = get_documents(full_text, separators=[
            "\n\n", "\n", "\t"], chunk_size=model_parameters.chunk_size, chunk_overlap=model_parameters.chunk_overlap)

        embeddings = create_embeddings(documents)
        doc_indexes = get_relevant_documents_indexes(
            embeddings, num_clusters=model_parameters.clusters_number)
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
