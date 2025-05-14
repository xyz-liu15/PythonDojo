"""
将大模型输出的英文内容翻译为中文，以顺序链接。
需要两个提示词，一个英文版的提示词。一个翻译英文输出内容的提示词。
"""
import os
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda,RunnableSequence


model = ChatOpenAI(
    model = "Pro/deepseek-ai/DeepSeek-V3",
    base_url = "https://www.dmxapi.com/v1",
    api_key = os.getenv("DMX_API_KEY"),
    temperature = 0.7
)

template = "请你使用{language}为我讲一个简短的科幻故事，不超过200字。"

English_prompt = ChatPromptTemplate.from_template(template)


translate_prompt = ChatPromptTemplate.from_messages({
    ("system","你是一个顶级科幻故事翻译大师，可以生动形象的将英文翻译为中文。")
    ("user","请翻译以下内容：{text}")
})


text_input = RunnableLambda(lambda x : English_prompt.format_messages(**x))
invoke_model = RunnableLambda(lambda x : model.invoke(x))
parser_output = RunnableLambda(lambda x : x.content)

translate_text = RunnableLambda(lambda x : translate_prompt.format_messages(**x))
translate_invoke_model = RunnableLambda(lambda x : model.invoke(x))
translate_parser_output = RunnableLambda(lambda x : x.content)

chain = text_input | invoke_model | parser_output | translate_invoke_model | translate_text | translate_invoke_model | translate_parser_output

response = chain.invoke({
    "language" : "English"
})