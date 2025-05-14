"""
langchain实现了与几百家公司的大模型进行交互。 
"""
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
import os

load_dotenv()

model_1 = ChatOpenAI(
    model="gpt-4o-mini",
    base_url="https://www.dmxapi.com/v1",
    api_key=os.getenv("DMX_API_KEY"),  # 替换成你的 DMXapi 令牌key
)
text = "周树人和鲁迅是兄弟吗？"
response = model_1.invoke(text)
print(response)


model_2 = ChatAnthropic(
    model="claude-3-5-haiku-20241022",
    base_url="https://www.dmxapi.com",
    api_key=os.getenv("DMX_API_KEY"),   # 替换成你的 DMXapi 令牌key
)
text = "周树人和鲁迅是兄弟吗？"
response = model_2.invoke(text)
print(response)