"""
将大模型输出的英文内容翻译为中文，以顺序链接。
需要两个提示词，一个英文版的提示词。一个翻译英文输出内容的提示词。
"""
import os
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser


model = ChatOpenAI(
    model = "Pro/deepseek-ai/DeepSeek-V3",
    base_url = "https://www.dmxapi.com/v1",
    api_key = os.getenv("DMX_API_KEY"),
    temperature = 0.7
)

human_template_prompt = ChatPromptTemplate.from_messages({
    ("system","你是一个顶级科幻小说创作大师，非常擅长使用生动形象的文字来组织语言。尤其是关于{topic}。"),
    ("user","请帮我创作一个关于{topic}的不超过200字的科幻短篇故事。")
})

novel_analyze_prompt = ChatPromptTemplate.from_template("采用人格分裂讨论模式（文学评论家，读者，创作者等人格）对{text}进行解构。")


prepared_for_analyze = RunnableLambda(lambda x : {"text" : x})


chain = (
        human_template_prompt | model | StrOutputParser() | 
         prepared_for_analyze | novel_analyze_prompt | 
         model | StrOutputParser()
)


response = chain.invoke({"topic" : "当地球上只剩下了一个人，这时，他的房门却被敲响了。"})
print(response)