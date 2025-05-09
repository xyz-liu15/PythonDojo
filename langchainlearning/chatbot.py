from typing import ParamSpecArgs
from langchain_core import prompts
from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


model = ChatDeepSeek(
                    model="deepseek-chat",
                    api_key=""
)

prompts = ChatPromptTemplate([
    ("system", "You are a helpful assistant that translates {input_language} to {output_language}."),
    ("human", "{text}"),
])

parser = StrOutputParser()

chain = prompts | model | parser


for chunk in chain.stream({"input_language": "English", "output_language": "Chinese", "text": "I love programming."}):
    print(chunk, end="",flush=True)
    # I adore programmer.
    # I adore programmer.