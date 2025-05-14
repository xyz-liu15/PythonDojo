"""
使用LCEL语法，实现链式调用。
"""
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


parser = StrOutputParser()

model = ChatOpenAI(
    model = "Pro/deepseek-ai/DeepSeek-V3",
    base_url = "https://www.dmxapi.com/v1",
    api_key = os.getenv("DMX_API_KEY"),
    temperature = 0.7
)


messages = [
    ("system" , "你是一个喜剧大师，可以给我讲关于{topic}的笑话。"),
    ("user" , "给我讲{number}个笑话。")
]

prompt_template = ChatPromptTemplate.from_messages(messages)

chain = prompt_template | model | parser

response = chain.invoke({
    "topic" : "胖猫",
    "number" : 2
})
print(response)