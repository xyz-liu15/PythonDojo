"""
好的，这串代码就像一个高度自动化的“客户反馈处理工厂”，我们一步步来看它是怎么运作的，特别是那些参数是如何像货物一样在流水线上被传递和加工的。

想象一下，你开了一家网店，收到了很多客户的评价，有好有坏，有中性的，还有一些让你摸不着头脑需要升级处理的。这套代码就是你的智能客服总管，能自动分类并初步草拟回复。

**第一站：准备工作与原料加载 (环境与模型初始化)**

1.  `from dotenv import load_dotenv`
    `load_dotenv()`
    *   **生动解释**：这就像工厂开工前的准备。`load_dotenv()` 是个小精灵，它会悄悄溜到你的项目文件夹里，找到一个叫做 `.env` 的秘密小本本。这个本本上可能写着一些重要的密码或许可证，比如你的 OpenAI API 密钥（`OPENAI_API_KEY`）。它把这些秘密信息加载到工厂的环境变量里，这样工厂里的其他机器（代码）就能在需要的时候拿到这些凭证，而不用把秘密直接写在公开的图纸（代码）上。
    *   **参数传递**：这里没有显式的参数传递给 `load_dotenv()` 函数本身（它会自动找 `.env` 文件），但它的 *结果* 是环境变量被设置了，后续的 `ChatOpenAI` 会间接使用到。

2.  `from langchain_openai import ChatOpenAI`
    `model = ChatOpenAI(model="gpt-4o")`
    *   **生动解释**：这是工厂的核心——一台超级智能的“写作机器人” `ChatOpenAI`。我们指定了它的型号是 `"gpt-4o"`，这可是最新最强大的型号！现在，`model` 这个变量就指向了这台随时待命的机器人。
    *   **参数传递**：
        *   `model="gpt-4o"`：这是给 `ChatOpenAI` 构造函数的参数，告诉它我们要用哪个具体的大语言模型。
        *   (隐式) `openai_api_key=os.getenv("OPENAI_API_KEY")`: `ChatOpenAI` 在初始化时，会自动去环境变量里找 `OPENAI_API_KEY`。这就是 `load_dotenv()` 的功劳！它把钥匙放好了，`ChatOpenAI` 自己会去取。

**第二站：设计各种回复的“配方卡” (Prompt Templates)**

我们有四种主要类型的反馈，以及一个用于分类的，所以需要五种不同的“配方卡”（Prompt Templates）。这些配方卡告诉写作机器人针对不同情况应该说什么。

1.  `from langchain.prompts import ChatPromptTemplate`
    `positive_feedback_template = ChatPromptTemplate.from_messages(...)`
    *   **生动解释**：这就像在设计一张“感谢信配方卡”。
        *   `("system", "You are a helpful assistant.")`: 这是给机器人的角色设定，告诉它：“你现在是一位乐于助人的助手。”
        *   `("human", "Generate a thank you note for this positive feedback: {feedback}.")`: 这是具体的指令。注意那个 `{feedback}`，它像一个空盘子，等着我们把客户的实际好评放上去。
    *   **参数传递**：
        *   `from_messages` 方法接收一个消息列表。每个消息是一个元组 `(角色, 内容)`。
        *   `{feedback}`：这是一个占位符。当这张配方卡被使用时，我们需要提供一个字典，其中必须包含一个 `feedback` 键，它的值就是客户的具体反馈内容。

    *类似地，`negative_feedback_template`（差评处理配方）、`neutral_feedback_template`（中性反馈处理配方）、`escalate_feedback_template`（升级处理配方）和 `classification_template`（分类配方）都是用同样的方式创建的。它们都包含一个 `{feedback}` 的空盘子。*

    *   `classification_template`: 这张配方卡比较特殊，它的任务是让机器人判断反馈是“积极的”、“消极的”、“中性的”，还是需要“升级处理”。

**第三站：组装流水线部件**

1.  `from langchain.schema.output_parser import StrOutputParser`
    *   **生动解释**：写作机器人（`model`）完成写作后，它的产出物其实是一个结构化的“消息对象”，里面除了文本内容，可能还有其他元数据。`StrOutputParser()` 就像一个“拆包工”，它的任务很简单：把这个复杂的消息对象拆开，只取出我们最关心的纯文本回复内容（字符串）。

2.  `from langchain.schema.runnable import RunnableBranch`
    `branches = RunnableBranch(...)`
    *   **生动解释**：这是工厂里的“智能分拣调度中心” (`RunnableBranch`)。它负责根据之前分类的结果，将任务导向正确的处理车间。
    *   它由一系列的 `(条件, 处理链)` 对组成，外加一个默认处理链。
    *   **条件**：是一个小型的判断函数（lambda 函数），它会检查输入的分类结果。
        *   `lambda x: "positive" in x`: 如果输入的字符串 `x`（也就是分类结果）中包含 "positive"，这个条件就成立。
    *   **处理链**：如果条件成立，就执行对应的处理链。例如，如果分类是 "positive"，就执行 `positive_feedback_template | model | StrOutputParser()` 这个小流水线。
        *   `positive_feedback_template | model | StrOutputParser()`: 这是一条迷你生产线。客户的原始反馈会先经过“感谢信配方卡”加工，然后送给“写作机器人”撰写，最后由“拆包工”提取纯文本。
    *   **默认处理链**：如果前面的条件都不满足，就走最后一个不带条件的链，这里是 `escalate_feedback_template | model | StrOutputParser()`。
    *   **参数传递（关键点！）**：
        *   `RunnableBranch` 本身会接收一个输入。在我们的主流程中，这个输入将是前面分类链输出的分类结果字符串（比如 "negative"）。
        *   这个输入（分类结果字符串）会传递给每个 `lambda x:` 函数中的 `x`。
        *   **当一个条件满足时，比如 `lambda x: "negative" in x` 为真，`RunnableBranch` 会将它最初收到的那个输入（也就是分类结果字符串 "negative"）传递给被选中的处理链作为其输入。**
        *   **这里有一个潜在的问题点**：被选中的处理链，例如 `negative_feedback_template | model | StrOutputParser()`，它的第一步是 `negative_feedback_template`。这个模板期望的输入是一个包含 `{feedback}` 键的字典，以便填充原始反馈。但如果它从 `RunnableBranch` 那里只收到了分类字符串（如 "negative"），它就无法正确填充 `{feedback}`。
            *   在更复杂的 LangChain 应用中，通常会确保传递给 `RunnableBranch` 的是一个字典，这个字典包含了分类结果 *和* 原始反馈。然后 lambda 条件可以检查字典中的分类结果，而被选中的链则可以从同一个字典中获取原始反馈。
            *   **为了解释代码的原意和通常的用法，我们假设 LangChain 在这里有某种机制（或者开发者期望）原始的 `{"feedback": review}` 数据能够被后续的模板访问到。一个常见的方式是使用 `RunnablePassthrough.assign` 来构建一个包含所有必要信息的字典，然后传递给 `RunnableBranch`。但按照代码的直接写法，这里存在歧义。我们先按“理想情况”解释，即模板能拿到原始反馈。**

3.  `classification_chain = classification_template | model | StrOutputParser()`
    *   **生动解释**：这是工厂的“初步分拣流水线”。
        *   `classification_template`：先用“分类配方卡”把客户反馈包装一下。
        *   `model`：然后让“写作机器人”阅读包装后的内容，并给出分类意见（比如 "positive", "negative"）。
        *   `StrOutputParser()`：“拆包工”提取出这个纯文本的分类意见。
    *   **参数传递**：
        *   当 `classification_chain.invoke({"feedback": "some review text"})` 被调用时：
            1.  `{"feedback": "some review text"}` 这个字典被传给 `classification_template`。
            2.  `classification_template` 使用 "some review text" 填充其 `{feedback}` 占位符，生成一个完整的提示（PromptValue）。
            3.  这个 PromptValue 被传给 `model`。
            4.  `model` 调用 OpenAI API，返回一个 AI 消息对象（比如 `AIMessage(content="negative")`）。
            5.  这个 AI 消息对象被传给 `StrOutputParser()`。
            6.  `StrOutputParser()` 提取出内容，输出字符串 `"negative"`。

4.  `chain = classification_chain | branches`
    *   **生动解释**：这是我们工厂的“总流水线”！它把“初步分拣流水线”和“智能分拣调度中心”串联起来。
    *   **参数传递**：
        1.  当 `chain.invoke({"feedback": review})` 被调用时，`{"feedback": review}` 首先被送入 `classification_chain`。
        2.  `classification_chain` 处理完毕后，输出一个分类字符串（例如 `"negative"`）。
        3.  这个分类字符串 (`"negative"`) 会作为输入，被传递给 `branches`（智能分拣调度中心）。

**第四站：开动工厂，处理订单！**

1.  `review = "The product is terrible. It broke after just one use and the quality is very poor."`
    *   **生动解释**：来了一个客户的差评！这就是我们要处理的“订单”。

2.  `result = chain.invoke({"feedback": review})`
    *   **生动解释**：按下总开关！我们把这个差评打包成一个字典 `{"feedback": review}`，然后扔到总流水线 `chain` 的入口。
    *   **详细运作流程（以差评为例）**：
        1.  **总流水线 (`chain`) 启动**：输入是 `{"feedback": "The product is terrible..."}`。
        2.  **第一段：分拣 (`classification_chain`)**：
            *   `classification_template` 接收 `{"feedback": "The product is terrible..."}`。它将 `review` 填入自己的 `{feedback}`，形成一个请求：“请将这个反馈分类：‘The product is terrible...’”
            *   这个请求被送往 `model` (GPT-4o)。
            *   `model` 分析后，输出类似 `AIMessage(content="negative")`。
            *   `StrOutputParser()` 提取内容，得到字符串 `"negative"`。
            *   `classification_chain` 的输出是：`"negative"`。
        3.  **连接处**：`"negative"` 这个字符串从 `classification_chain` 的出口流向 `branches` 的入口。
        4.  **第二段：调度与处理 (`branches`)**：
            *   `branches` 接收到输入 `"negative"`。
            *   它开始检查条件：
                *   `lambda x: "positive" in x` (即 `"positive" in "negative"`) -> `False`。跳过。
                *   `lambda x: "negative" in x` (即 `"negative" in "negative"`) -> `True`。**命中！**
            *   现在，`branches` 决定执行与 "negative" 条件关联的处理链：`negative_feedback_template | model | StrOutputParser()`。
            *   **关键的参数传递**：此时，`RunnableBranch` 会将它收到的输入（即分类结果 `"negative"`）传递给选中的这条子链。
                *   **理想情况下（或者通过更完善的LCEL结构）**：`negative_feedback_template` 应该能访问到最初的 `review` 内容（"The product is terrible..."）来填充它的 `{feedback}` 占位符。如果它只收到了 `"negative"` 字符串，它将无法正确工作。我们假设它能通过某种方式拿到原始 `review`。
                *   `negative_feedback_template` 接收到原始反馈 (我们假设它能拿到，例如 `{"feedback": "The product is terrible..."}`), 将其填入 `{feedback}`，生成一个针对差评的回复草稿指令，例如：“针对这个差评生成一个回复：‘The product is terrible...’”
                *   这个指令被送往 `model` (GPT-4o)。
                *   `model` 根据这个指令，生成一段安抚客户、解决问题的回复文本，例如 `AIMessage(content="We are so sorry to hear about your experience...")`。
                *   `StrOutputParser()` 提取内容，得到最终的回复字符串，比如 `"We are so sorry to hear about your experience..."`。
            *   `branches` 的输出就是这条子链的输出。
        5.  **总流水线 (`chain`) 的最终输出**：`result` 变量现在就存储了这条由 `model` 生成的、针对差评的回复文本。

3.  `print(result)`
    *   **生动解释**：将工厂加工好的最终回复打印出来，展示给用户看！

**总结一下参数传递的“链条”感觉：**

*   最开始，你像一个客户服务代表，拿着一个原始反馈 `review`。
*   你把它放进一个信封 `{"feedback": review}`，这是我们整个工厂流程的初始“包裹”。
*   这个“包裹”首先进入 `classification_chain`：
    *   `classification_template` 打开包裹，取出 `review`，贴在自己的模板上，形成一个“分类请求单”。
    *   “分类请求单”交给 `model`，`model` 写上分类结果（比如 "negative"），装进一个“模型回复信封”。
    *   `StrOutputParser` 打开“模型回复信封”，只取出分类结果字符串 "negative"。这是 `classification_chain` 的产出物。
*   这个“分类结果字符串” (`"negative"`) 被传递给 `branches`。
*   `branches` 看到是 "negative"，就激活了处理负面反馈的那条迷你生产线。
*   **理想情况下**，这条迷你生产线（`negative_feedback_template | model | StrOutputParser()`）不仅知道分类是 "negative"，还能拿到最初的那个 `review` 内容。
    *   `negative_feedback_template` 再次取出 `review`，贴在自己的“差评回复模板”上，形成一个“回复草稿请求单”。
    *   “回复草稿请求单”交给 `model`，`model` 写出回复初稿，装进“模型回复信封”。
    *   `StrOutputParser` 打开信封，取出纯文本的回复初稿。
*   这个纯文本回复初稿就是整个 `chain` 的最终 `result`。

这个过程就像一个精心设计的接力赛，每一棒选手（组件）完成自己的任务后，把成果（参数/数据）准确无误地交给下一棒，直到终点。而 `RunnableBranch` 就像赛道上的岔路口，根据指示牌（lambda 条件）将选手导向正确的后续赛道。理解每个组件期望接收什么输入，以及它会产生什么输出，是理解整个链条运作的关键！
"""

from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableBranch
from langchain_openai import ChatOpenAI

# Load environment variables from .env
load_dotenv()

# Create a ChatOpenAI model
model = ChatOpenAI(
    model = "Pro/deepseek-ai/DeepSeek-V3",
    base_url = "https://www.dmxapi.com/v1",
    api_key = os.getenv("DMX_API_KEY"),
    temperature = 0.7
)

# Define prompt templates for different feedback types
positive_feedback_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        ("human",
         "Generate a thank you note for this positive feedback: {feedback}."),
    ]
)

negative_feedback_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        ("human",
         "Generate a response addressing this negative feedback: {feedback}."),
    ]
)

neutral_feedback_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        (
            "human",
            "Generate a request for more details for this neutral feedback: {feedback}.",
        ),
    ]
)

escalate_feedback_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        (
            "human",
            "Generate a message to escalate this feedback to a human agent: {feedback}.",
        ),
    ]
)

# Define the feedback classification template
classification_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        ("human",
         "Classify the sentiment of this feedback as positive, negative, neutral, or escalate: {feedback}."),
    ]
)

# Define the runnable branches for handling feedback
branches = RunnableBranch(
    (
        lambda x: "positive" in x,
        positive_feedback_template | model | StrOutputParser()  # Positive feedback chain
    ),
    (
        lambda x: "negative" in x,
        negative_feedback_template | model | StrOutputParser()  # Negative feedback chain
    ),
    (
        lambda x: "neutral" in x,
        neutral_feedback_template | model | StrOutputParser()  # Neutral feedback chain
    ),
    escalate_feedback_template | model | StrOutputParser()
)

# Create the classification chain
classification_chain = classification_template | model | StrOutputParser()

# Combine classification and response generation into one chain
chain = classification_chain | branches

# Run the chain with an example review
# Good review - "The product is excellent. I really enjoyed using it and found it very helpful."
# Bad review - "The product is terrible. It broke after just one use and the quality is very poor."
# Neutral review - "The product is okay. It works as expected but nothing exceptional."
# Default - "I'm not sure about the product yet. Can you tell me more about its features and benefits?"

review = "The product is terrible. It broke after just one use and the quality is very poor."
result = chain.invoke({"feedback": review})

# Output the result
print(result)