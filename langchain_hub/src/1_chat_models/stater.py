"""
实现一个与大模型的简单交互
需要执行命令：uv add langchain_deepseek langchain python-dotenv
"""


from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv


load_dotenv() # 加载环境变量

model = ChatDeepSeek(
    model = "deepseek-chat",
    temperature = 0.7
)

# invoke是一个很重要的方法，它可以让你和大模型进行对话，接收字符串或者字典。
result = model.invoke("你好")

print(result)