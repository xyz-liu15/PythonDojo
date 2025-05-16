"""
---

**代码的奇妙旅程：打造你的专属《魔戒》知识库**

想象一下，我们要为一部鸿篇巨著，比如《魔戒》（lord_of_the_rings.txt），打造一个智能问答机器人。为了让机器人能理解并回答关于这本书的问题，我们不能直接把整本书丢给它，那太大了，机器人会“消化不良”。我们需要一个更智能的方法——这就是这段代码所做的事情：建立一个“向量知识库”。

**旅程起点：准备工作与“寻路”**

1.  `import os` 等模块：
    *   **生动解释**：这就像探险开始前，我们要召集各路英雄好汉。
        *   `os`：这位是“路径规划大师”，帮我们找到文件在哪，以及要把新建的知识库（数据库）放在哪。
        *   `TextLoader`：一位“古籍阅读者”，能把文本文件里的内容一字不差地读出来。
        *   `CharacterTextSplitter`：一位“细致的裁书匠”，能把厚厚的书卷（文本）切分成大小合适、略有重叠的小纸条，方便后续处理。
        *   `OpenAIEmbeddings`：一位“语言魔法师”（或者叫“意义编码器”），能把文字转化成一串特殊的数字（向量），这些数字能代表文字的深层含义。
        *   `Chroma`：一位“图书馆管理员”，负责建立和管理一个特殊的“向量图书馆”，在这个图书馆里，书籍（文本片段）不是按字母顺序排，而是按“意义相近度”来组织的。

2.  路径定义：
    `current_dir = os.path.dirname(os.path.abspath(__file__))`
    `file_path = os.path.join(current_dir, "documents", "lord_of_the_rings.txt")`
    `persistent_directory = os.path.join(current_dir, "db", "chroma_db")`
    *   **生动解释**：路径规划大师 `os` 开始工作了。
        *   `current_dir`：首先确定我们现在身处何方（当前脚本所在的文件夹）。
        *   `file_path`：然后告诉我们，《魔戒》这本书（`lord_of_the_rings.txt`）被放在了“身处何方”下的 `documents` 文件夹里。
        *   `persistent_directory`：我们决定把新建的“向量图书馆”建在“身处何方”下的 `db/chroma_db` 这个地方。这个图书馆建好后会“持久化”，下次再来就不用重建了。
    *   **参数传递**：
        *   `os.path.abspath(__file__)`：`__file__` 是一个内置变量，代表当前脚本的路径。`abspath` 把它变成一个绝对路径。这个绝对路径作为参数传给 `os.path.dirname`。
        *   `os.path.dirname(...)`：接收一个路径作为参数，返回这个路径所在的目录。其结果赋值给 `current_dir`。
        *   `os.path.join(...)`：接收多个路径片段作为参数（如 `current_dir`, `"documents"`, `"lord_of_the_rings.txt"`），然后像搭积木一样把它们智能地拼接成一个完整的路径。结果分别赋给 `file_path` 和 `persistent_directory`。

**旅程中途：检查与建设“向量图书馆”**

3.  `if not os.path.exists(persistent_directory):`
    *   **生动解释**：动工之前，我们先派路径规划大师 `os` 去 `persistent_directory`（预定的图书馆地址）看看。如果那个地方空空如也（`os.path.exists` 返回 `False`，加上 `not` 就是 `True`），说明图书馆还没建，那我们就得开始“伟大工程”了！
    *   **参数传递**：`persistent_directory` (字符串，包含路径) 被作为参数传递给 `os.path.exists` 函数。

    **如果图书馆不存在（进入 `if` 代码块）：**

    4.  `if not os.path.exists(file_path): raise FileNotFoundError(...)`
        *   **生动解释**：在开始建图书馆之前，我们得确保有“原材料”——《魔戒》这本书。再次请路径规划大师 `os` 去 `file_path` 看看书在不在。如果书 (`lord_of_the_rings.txt`) 也不在，那就巧妇难为无米之炊了，直接报错（`raise FileNotFoundError`）并停止。
        *   **参数传递**：`file_path` 被传递给 `os.path.exists`。错误信息字符串被传递给 `FileNotFoundError` 的构造函数。

    5.  **第一步：阅读原著 (`TextLoader`)**
        `loader = TextLoader(file_path)`
        `documents = loader.load()`
        *   **生动解释**：书找到了！现在请“古籍阅读者” `TextLoader` 出场。
            *   `loader = TextLoader(file_path)`：我们告诉阅读者，你要读的书在 `file_path` 这个位置。这时，`loader` 就成了一个配置好的阅读工具，它知道了目标。
            *   `documents = loader.load()`：阅读者开始工作，`load()` 一声令下，它把整本书的内容读出来，变成一个或多个“文档对象”（这里通常是一个包含整本书内容的文档对象列表，即使只有一个文件）。这些文档对象被存放在 `documents` 变量里，就像把书的内容抄写到了数字卷轴上。
        *   **参数传递**：
            *   `file_path` (字符串) 作为参数传递给 `TextLoader` 类的构造函数，初始化 `loader` 对象。
            *   `loader.load()` 方法被调用时，它内部会使用之前初始化时传入的 `file_path` 去实际读取文件内容。

    6.  **第二步：裁切书卷 (`CharacterTextSplitter`)**
        `text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)`
        `docs = text_splitter.split_documents(documents)`
        *   **生动解释**：整本数字卷轴太长了，不方便“语言魔法师”施法。现在请“细致的裁书匠” `CharacterTextSplitter` 上场。
            *   `text_splitter = CharacterTextSplitter(...)`：我们告诉裁书匠，每切一小段（chunk），长度大约是 `1000` 个字符 (`chunk_size=1000`)。为了上下文连贯，相邻两段之间最好有 `50` 个字符的重叠部分 (`chunk_overlap=50`)。裁书匠记下了这些要求。
            *   `docs = text_splitter.split_documents(documents)`：裁书匠拿起之前阅读者给的 `documents` (数字卷轴)，按照要求开始“咔嚓咔嚓”地裁剪。裁剪下来的许多小片段（文档块，每个都是一个独立的 `Document` 对象）被收集起来，放在 `docs` 这个篮子里。
        *   **参数传递**：
            *   `chunk_size=1000` 和 `chunk_overlap=50` (整数) 作为关键字参数传递给 `CharacterTextSplitter` 类的构造函数，初始化 `text_splitter` 对象。
            *   `documents` (之前 `loader.load()` 返回的文档对象列表) 作为参数传递给 `text_splitter` 对象的 `split_documents` 方法。

    7.  **信息展示（可选步骤）**
        `print(...)`
        *   **生动解释**：裁书匠干完活，向我们汇报一下成果：总共切了多少块，并给我们看一小块样品。

    8.  **第三步：准备“意义编码器” (`OpenAIEmbeddings`)**
        `embeddings = OpenAIEmbeddings(model="text-embedding-3-small")`
        *   **生动解释**：现在，我们要把这些文字片段转化成机器能更好理解的“意义向量”。请出“语言魔法师” `OpenAIEmbeddings`。
            *   我们告诉魔法师，请使用名为 `"text-embedding-3-small"` 的魔法咒语（模型）。这个咒语能把文本转换成高质量的数字向量。`embeddings` 现在就是这位准备好施法的魔法师。
        *   **参数传递**：
            *   `model="text-embedding-3-small"` (字符串) 作为关键字参数传递给 `OpenAIEmbeddings` 类的构造函数。这个构造函数内部可能还会去环境变量里查找 OpenAI 的 API 密钥等信息（通常由 `load_dotenv()` 提前加载好，虽然本代码段没有显式调用，但在实际项目中常见）。

    9.  **第四步：建造并填充“向量图书馆” (`Chroma.from_documents`)**
        `db = Chroma.from_documents(docs, embeddings, persist_directory=persistent_directory)`
        *   **生动解释**：万事俱备，只欠东风！现在轮到“图书馆管理员” `Chroma` 来建造和填充我们的“向量图书馆”了。
            *   `Chroma.from_documents(...)`：这是一个非常关键的指令。我们告诉管理员：
                *   `docs`：这些是你需要整理入库的“书籍片段”（就是之前裁书匠切好的那些）。
                *   `embeddings`：请用这位“语言魔法师”来为每一片书籍片段生成“意义编码”（向量）。
                *   `persist_directory=persistent_directory`：把建好的图书馆保存在 `persistent_directory` 这个地方，这样下次就不用从头再来了。
            *   **底层运作**：
                1.  `Chroma` 会遍历 `docs` 里的每一个文本片段。
                2.  对于每一个片段，它会调用 `embeddings` 魔法师的“施法”能力（例如，`embeddings.embed_documents([text_fragment])`），将文本片段转换成一个数字向量。
                3.  然后，`Chroma` 会将原始的文本片段和它对应的数字向量一起存储起来，并建立索引，方便以后根据“意义相似度”快速查找。
                4.  所有片段处理完毕后，整个图书馆的结构和数据会被保存到 `persistent_directory` 指定的磁盘位置。
            *   `db`：现在，`db` 就代表了我们这个功能完备、内容丰富的“向量图书馆”！
        *   **参数传递**：
            *   `docs` (文档块列表) 作为第一个位置参数传递。
            *   `embeddings` (OpenAIEmbeddings 对象) 作为第二个位置参数传递。
            *   `persist_directory=persistent_directory` (字符串，路径) 作为关键字参数传递。

    **如果图书馆已存在（进入 `else` 代码块）：**

10. `else: print("Vector store already exists. No need to initialize.")`
    *   **生动解释**：如果我们一开始检查时，发现 `persistent_directory` 那个地方已经有图书馆了，太棒了！说明之前已经建好了，我们就不用重复劳动了，直接告知用户“图书馆已就位”。

**旅程终点：为提问做好准备**

```python
# 要问的问题
# 谁是持戒者？
# 甘道夫在哪里遇见了佛罗多？
```

*   **生动解释**：虽然这段代码本身没有实际去“问问题”，但它留下了线索。这就像我们建好了图书馆，然后在门口贴了张纸条，写着一些我们可能想进去查找的问题。
*   在后续的代码中，我们可以使用 `db` (我们的向量图书馆) 和 `embeddings` (语言魔法师) 来对这些问题进行提问。比如，我们会先把问题“谁是持戒者？”也转换成向量，然后去 `db` 中查找与之意义最相近的文本片段，从而找到答案。

**总结参数传递的“接力棒”：**

1.  **起点**：`file_path` (书的位置) 和 `persistent_directory` (图书馆位置) 是最初的设定。
2.  `file_path` **传递给** `TextLoader`，后者用它 `load()` 出 `documents` (整本书内容)。
3.  `documents` **传递给** `CharacterTextSplitter` 的 `split_documents` 方法，后者根据预设的 `chunk_size` 和 `chunk_overlap` 切割出 `docs` (书的片段)。
4.  `docs` (书的片段)、`embeddings` (配置好的语言魔法师) 和 `persistent_directory` (图书馆存储位置) **一起传递给** `Chroma.from_documents`。
    *   `Chroma` 内部会使用 `embeddings` 对象将 `docs` 里的每个文本片段转换成向量。
    *   然后将文本和向量存储起来，并保存到 `persistent_directory`。
    *   最终返回一个可操作的向量数据库对象 `db`。

整个过程就像一条高效的流水线，每个组件（对象/函数）接收上一步的产出（参数），进行加工，再把成果传递给下一步，最终构建出一个强大的知识检索工具的基础！
"""



import os
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

# 定义包含文本文件的目录和持久化目录
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "documents", "lord_of_the_rings.txt")
persistent_directory = os.path.join(current_dir, "db", "chroma_db")

# 检查 Chroma 向量存储是否已存在
if not os.path.exists(persistent_directory):
    print("持久化目录不存在。正在初始化向量存储...")

    # 确保文本文件存在
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"文件 {file_path} 不存在。请检查路径。"
        )

    # 从文件读取文本内容
    loader = TextLoader(file_path)
    documents = loader.load()

    # 将文档分割成块
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)

    # 显示关于分割后文档块的信息
    print("\n--- 文档块信息 ---")
    print(f"文档块数量: {len(docs)}")
    print(f"示例块:\n{docs[0].page_content}\n")

    # 创建嵌入向量
    print("\n--- 正在创建嵌入向量 ---")
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )  # 如果需要，请更新为有效的嵌入模型
    print("\n--- 完成创建嵌入向量 ---")

    # 创建向量存储并自动持久化
    print("\n--- 正在创建向量存储 ---")
    db = Chroma.from_documents(
        docs, embeddings, persist_directory=persistent_directory)
    print("\n--- 完成创建向量存储 ---")

else:
    print("向量存储已存在。无需初始化。")

# 要问的问题
# 谁是持戒者？
# 甘道夫在哪里遇见了佛罗多？