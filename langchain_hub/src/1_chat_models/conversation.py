"""
实现一个简单的对话

HumanMessage: 人类的消息
AIMessage: AI的消息
SystemMessage: 系统的消息(用于指导AI的行为)
"""
from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv


load_dotenv() # 加载环境变量


# 实例化一个大模型
model = ChatDeepSeek(
    model = "deepseek-chat",
    temperature = 0.7
)

messages = [
    SystemMessage(content="你是一个非常友善的助手"),
    HumanMessage(content="你好"),
    AIMessage(content="你好，我是一个非常友善的助手，我可以帮助你解决任何问题"),
]

# invoke是一个很重要的方法，它可以让你和大模型进行对话，接收字符串或者字典。
result = model.invoke(messages)

print(result.content)