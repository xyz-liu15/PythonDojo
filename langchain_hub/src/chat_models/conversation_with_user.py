"""为聊天机器人添加历史记录"""
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage
import os

from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model = "Pro/deepseek-ai/DeepSeek-V3",
    base_url = "https://www.dmxapi.com/v1",
    api_key = os.getenv("DMX_API_KEY"),
    temperature = 0.7 # 值取0-1，数值越大，大模型输出内容越发散。
)

chat_history = [] # 创建一个空列表用来储存历史聊天记录

system_message = SystemMessage(content = "你是一个顶级AI助手。")

chat_history.append(system_message) # 将系统消息添加进历史聊天记录中

while True:
    query = input("人类：")
    if query.lower() == "exit":
        print("聊天结束！")
        break
    else:
        human_message = HumanMessage(content = query) # 创建一个人类消息
        chat_history.append(human_message)
        response = model.invoke(chat_history).content
        chat_history.append(AIMessage(content = response)) # 将AI消息添加进历史聊天记录中  
        print(f"{response}",end="",flush=True) # 打印输出
        
        
        

