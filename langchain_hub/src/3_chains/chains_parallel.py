"""
实现并行调用
构建一个链 (chain)，该链首先为指定电影生成一个摘要，
然后基于这个摘要并行地分析电影的情节 (plot) 和角色 (characters)，
最后将这两个分析结果合并成一个最终的评论。
"""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda,RunnableParallel


load_dotenv(override=True) # 加载环境变量，覆盖系统环境变量

# 创建大模型实例
model = ChatOpenAI(
    model = "Pro/deepseek-ai/DeepSeek-V3",
    base_url = "https://www.dmxapi.com/v1",
    api_key = os.getenv("DMX_API_KEY"),
    temperature = 0.7 # 数值范围在0-1，数值越大，模型输出越有想象力。
)

summary_template_prompt = ChatPromptTemplate.from_messages({
    ("system","你是一个顶级电影评论家，善于使用多种角度对电影进行评论。"),
    ("user","请你使用刁钻的语言对{movie_name}进行评价。")
})


def plot_analyze(plot):
    """对电影情节进行评论分析"""
    plot_prompt = ChatPromptTemplate.from_messages({
        ("system","你是一个顶级电影评论家，善于透过内核来对电影的情节进行评论。"),
        ("user","请你使用刁钻的语言对{plot}进行评价。")
    })
    return plot_prompt.format_prompt(plot=plot)

def analyze_characters(characters):
    character_template = ChatPromptTemplate.from_messages(
        [
            ("system", "你是一个顶级电影评论家，善于透过内核来对电影中的角色进行评论。"),
            ("human", "请你使用刁钻的语言对{characters}进行评价。"),
        ]
    )
    return character_template.format_prompt(characters=characters)


def combine_verdicts(plot_analyze, analyze_characters):
    return f"情节分析：\n{plot_analyze}\n\n人物分析：\n{analyze_characters}"


plot_analyze_chain = (
                      RunnableLambda(lambda x : plot_analyze(x)) | 
                      model | 
                      StrOutputParser()
                      )


analyze_characters_chain = (
    RunnableLambda(lambda x: analyze_characters(x)) |
    model |
    StrOutputParser()
)

chain = (summary_template_prompt | 
         model | 
         StrOutputParser() | 
         RunnableParallel(branches = {"plot" : plot_analyze_chain,"characters" : analyze_characters_chain}) | 
        RunnableLambda(lambda x: combine_verdicts(x["branches"]["plot"], x["branches"]["characters"]))
         )


response = chain.invoke({"movie_name" : "哪吒之魔童闹海"})
print(response)