from langchain import PromptTemplate
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import CTransformers
from langchain.chains import RetrievalQA
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

import chainlit as cl


DB_PATH = "./vectorstores/db_faiss"

custom_qa_prompt_template = """Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
Helpful answer:
"""


def set_custom_qa_prompt():
    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template=custom_qa_prompt_template,
    )
    return prompt_template


def load_llm():
    llm = CTransformers(
        model='llama-2-7b-chat.ggmlv3.q8_0.bin',
        model_type='llama',
        max_new_token=512,
        temperature=0.5
    )
    return llm


def retrieval_qa_chain(llm, prompt, db: FAISS):
    qa_chain = RetrievalQA.from_chain_type(llm=llm,
                                           chain_type='stuff',
                                           retriever=db.as_retriever(
                                               search_kwargs={'k': 3}),
                                           return_source_documents=True,
                                           chain_type_kwargs={"verbose": True, "prompt": prompt,
                                                              }
                                           )
    return qa_chain


def qa_bot():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={'device': 'cpu'})

    db = FAISS.load_local(folder_path=DB_PATH, embeddings=embeddings)

    llm = load_llm()

    qa_prompt = set_custom_qa_prompt()

    qa = retrieval_qa_chain(llm=llm, db=db, prompt=qa_prompt)
    return qa


def parse_output(query):
    qa_result = qa_bot()
    response = qa_result.run({'query': query})
    return response


@cl.on_chat_start
async def start():
    chain = qa_bot()
    msg = cl.Message(content="Starting the bot...")
    await msg.send()
    msg.content = "Hi, Welcome to Medical Bot. What is your query?"
    await msg.update()

    cl.user_session.set("chain", chain)


@cl.on_message
async def main(message):
    chain = cl.user_session.get("chain")
    cb = cl.AsyncLangchainCallbackHandler(
        stream_final_answer=True, answer_prefix_tokens=["FINAL", "ANSWER"]
    )
    cb.answer_reached = True
    res = await chain.acall(message, callbacks=[cb])
    answer = res["result"]
    sources = res["source_documents"]
    print("the response is", res)
    if sources:
        answer += f"\nSources:" + str(sources)
    else:
        answer += "\nNo sources found"

    await cl.Message(content=answer).send()
