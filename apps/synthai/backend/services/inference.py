from typing import Literal
from services.configuration import get_settings
import concurrent.futures

from langchain.chat_models import ChatOpenAI
from langchain.llms import HuggingFaceHub
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from langchain.schema.language_model import BaseLanguageModel
from langchain.chains.combine_documents.base import BaseCombineDocumentsChain


def create_llm(task: Literal["summarize"] | Literal["synthesis"]):
    settings = get_settings()
    if settings.OPENAI_API_KEY != None:

        llm = ChatOpenAI(temperature=0,
                         openai_api_key=settings.OPENAI_API_KEY,
                         max_tokens=1000,
                         model='gpt-3.5-turbo'
                         ) if task == "summarize" else ChatOpenAI(temperature=0,
                                                                  openai_api_key=settings.OPENAI_API_KEY,
                                                                  max_tokens=3000,
                                                                  model='gpt-4',
                                                                  request_timeout=120
                                                                  )
    else:
        llm = HuggingFaceHub(repo_id="tiiuae/falcon-7b-instruct")
    return llm


def create_map_summarization_chain(llm: BaseLanguageModel, prompt: str, input_variables: list[str]):
    prompt_template = PromptTemplate(
        template=prompt, input_variables=input_variables)
    map_chain = load_summarize_chain(llm=llm,
                                     chain_type="stuff",
                                     prompt=prompt_template)
    return map_chain


async def summarize_docs(llm: BaseLanguageModel, prompt: str, input_variables: list[str], documents: list[Document]):
    summary_list = []

    map_chain = create_map_summarization_chain(
        llm=llm, prompt=prompt, input_variables=input_variables)

    with concurrent.futures.ProcessPoolExecutor() as executor:
        future_to_doc = {executor.submit(
            run_summarization, map_chain, doc): doc for doc in documents}

        for future in concurrent.futures.as_completed(future_to_doc):
            doc = future_to_doc[future]
            try:
                chunk_summary = future.result()
                summary_list.append(chunk_summary)
            except Exception as e:
                print(f"Error processing document: {doc.content}, error: {e}")

    return summary_list


def run_summarization(map_chain: BaseCombineDocumentsChain, doc: Document):
    return map_chain.run([doc])


async def synthesis(llm: BaseLanguageModel, prompt: str, input_variables: list[str], summary_list: list[str]):
    summaries = "\n".join(summary_list)
    summaries_doc = Document(page_content=summaries)
    reduce_chain = create_map_summarization_chain(llm=llm,
                                                  prompt=prompt,
                                                  input_variables=input_variables)

    output = await reduce_chain.arun([summaries_doc])
    return output
