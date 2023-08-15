from typing import Literal
from services.configuration import get_settings

from langchain.chat_models import ChatOpenAI
from langchain.llms import HuggingFaceHub
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from langchain.schema.language_model import BaseLanguageModel

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


def create_map_summarization_chain(llm:BaseLanguageModel, prompt: str, input_variables: list[str]):
    prompt_template = PromptTemplate(
        template=prompt, input_variables=input_variables)
    map_chain = load_summarize_chain(llm=llm,
                                     chain_type="stuff",
                                     prompt=prompt_template)
    return map_chain


def summarize_docs(map_chain, documents: list[Document]):
    summary_list = []
# Loop through a range of the lenght of your selected docs
    for i, doc in enumerate(documents):

        # Go get a summary of the chunk
        chunk_summary = map_chain.run([doc])

        # Append that summary to your list
        summary_list.append(chunk_summary)

    return summary_list


async def synthesis(llm:BaseLanguageModel, prompt: str, input_variables: list[str], summary_list: list[str]):
    summaries = "\n".join(summary_list)
    print("---this are all the summaries---", summaries)
    summaries_doc = Document(page_content=summaries)

    reduce_chain = create_map_summarization_chain(llm=llm,
                                                  prompt=prompt,
                                                  input_variables=input_variables)

    output = await reduce_chain.arun([summaries_doc])
    return output
