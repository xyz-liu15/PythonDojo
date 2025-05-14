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


prompt_template = ChatPromptTemplate.from_messages(
     [
        ("system", "你钟爱于事实，并且你会告诉我关于{animal}的事实。"),
        ("human", "告诉我{count}事实。"),
    ]
)
format_prompt  = RunnableLambda(lambda x : prompt_template.format_prompt(**x)) # 将animal和count解包填入提示词模板，生成最终的提示词传递出去
invoke_model = RunnableLambda(lambda x : model.invoke(x.to_messages())) # 将格式化后的内容输入给大模型，然后将大模型输出的内容传递出去
parse_output = RunnableLambda(lambda x : x.content)


chain = format_prompt | invoke_model | parse_output


for chunk in chain.stream({
    "animal" : "cat",
    "count" : 3
}):
    print(chunk,end="",flush = True)