import os
from google.cloud import firestore
from langchain_google_firestore import FirestoreChatMessageHistory
from langchain_openai import ChatOpenAI

# 设置代理
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"  # 替换为 Mihomo Party 代理端口
os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"

"""
重现这个示例的步骤：
1. 创建一个 Firebase 账户
2. 创建一个新的 Firebase 项目和 FireStore 数据库
3. 获取项目 ID
4. 在你的电脑上安装 Google Cloud CLI
    - https://cloud.google.com/sdk/docs/install
    - 使用你的 Google 账户认证 Google Cloud CLI
        - https://cloud.google.com/docs/authentication/provide-credentials-adc#local-dev
    - 设置默认项目为你创建的 Firebase 项目
5. 使用命令 `pip install langchain-google-firestore` 安装 langchain-google-firestore
6. 在 Google Cloud 控制台中启用 Firestore API：
    - https://console.cloud.google.com/apis/enableflow?apiid=firestore.googleapis.com&project=crewai-automation
"""

# 设置 Firebase Firestore 配置
PROJECT_ID = "pythondojo-7e453"  # Firebase 项目的 ID
SESSION_ID = "user_session_new"  # 这可以是用户名或一个唯一的 ID
COLLECTION_NAME = "chat_history"  # 存储聊天历史记录的 Firestore 集合名称

# 初始化 Firestore 客户端
print("正在初始化 Firestore 客户端...")  # 输出日志，表示正在初始化 Firestore 客户端
client = firestore.Client(project=PROJECT_ID)  # 使用项目 ID 初始化 Firestore 客户端

# 初始化 Firestore 聊天记录
print("正在初始化 Firestore 聊天记录...")  # 输出日志，表示正在初始化聊天记录
chat_history = FirestoreChatMessageHistory(
    session_id=SESSION_ID,  # 使用会话 ID
    collection=COLLECTION_NAME,  # 指定集合名称
    client=client,  # 使用 Firestore 客户端
)
print("聊天记录初始化完成。")  # 输出日志，表示聊天记录初始化完成
print("当前聊天记录:", chat_history.messages)  # 输出当前的聊天记录

# 初始化聊天模型
model = ChatOpenAI(model="Pro/deepseek-ai/DeepSeek-V3", base_url="https://www.dmxapi.com/v1", api_key=os.getenv("DMX_API_KEY"))  # 使用指定的模型和 API 密钥初始化聊天模型

print("开始与 AI 聊天。输入 'exit' 退出。")  # 提示用户输入聊天内容，输入 'exit' 退出聊天

# 聊天循环
while True:
    human_input = input("用户: ")  # 获取用户输入
    if human_input.lower() == "exit":  # 如果用户输入 'exit'，则退出循环
        break
    chat_history.add_user_message(human_input)  # 将用户消息添加到聊天记录中

    ai_response = model.invoke(chat_history.messages)  # 传递当前的聊天记录给模型，获取 AI 的响应
    chat_history.add_ai_message(ai_response.content)  # 将 AI 的回应添加到聊天记录中

    print(f"AI: {ai_response.content}")  # 输出 AI 的回应
