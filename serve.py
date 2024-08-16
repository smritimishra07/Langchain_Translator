from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from langserve import add_routes
from dotenv import load_dotenv
load_dotenv()

groq_api_key=os.getenv("GROQ_API_KEY")
model=ChatGroq(model="Gemma2-9b-It",groq_api_key=groq_api_key)

# 1.Create prompt template
system_template = "Translate the following into {language}: {text}"
prompt_template = ChatPromptTemplate.from_template(system_template)

parser=StrOutputParser()

# Define chain function
def run_chain(text, language):
    prompt = prompt_template.format(text=text, language=language)
    response = model(prompt)
    return parser.parse(response)

# FastAPI app definition
from fastapi import FastAPI, Request

## Create chain
chain=prompt_template|model|parser

## App definition
app=FastAPI(title="Langchain Server",
            version="1.0",
            description="A simpleAPI server using Langchain runnable interfaces")

## Adding chain routes
add_routes(
    app,
    chain,
    path="/chain"
)

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8000)