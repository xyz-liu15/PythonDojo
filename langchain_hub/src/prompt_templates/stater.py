"""
使用提示词模板
"""
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


model = ChatOpenAI(
    model = "Pro/deepseek-ai/DeepSeek-V3",
    base_url = "https://www.dmxapi.com/v1",
    api_key = os.getenv("DMX_API_KEY"),
    temperature = 0.7
)


# # 例子一
# # 创建一个模板
# template = "请你帮我写一份辞职申请，内容包括{reason}，{date}。"

# # 创建一个提示词模板
# prompt_template = ChatPromptTemplate.from_template(template)

# # 构建提示词
# prompt = prompt_template.invoke({
#     "reason" : "世界这么大，我想去看看。",
#     "date" : "2025年5月14日"
# })


# response = model.invoke(prompt)

# print(response.content)

# 例子二
# 在元组中使用system消息和human消息
messages = [
    ("system" , "你是一个喜剧大师，可以给我讲关于{topic}的笑话。"),
    ("user" , "给我讲{number}个笑话。")
]

prompt_template = ChatPromptTemplate.from_messages(messages)

prompt = prompt_template.invoke({
    "topic" : "猫",
    "number" : "3"
})

response = model.invoke(prompt)
print(response.content)