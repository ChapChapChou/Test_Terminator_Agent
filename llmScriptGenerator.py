from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.agents import load_tools, initialize_agent
from langchain.agents import AgentType
from langchain.agents import Tool
from langchain.tools.file_management.write import WriteFileTool
from langchain.tools.file_management.read import ReadFileTool
from langchain_community.tools.human.tool import HumanInputRun
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

from llm_commons.langchain.btp_llm import BTPOpenAIEmbeddings
from llm_commons.langchain.btp_llm import BTPOpenAI ,ChatBTPOpenAI
 
from multiprocessing import cpu_count
import os

os.environ["OPENAI_API_KEY"] = ""
os.environ["SERPAPI_API_KEY"] = ""
#os.environ["OPENAI_API_KEY"] = ""
from langchain_community.utilities import SerpAPIWrapper
from langchain.agents import Tool
from langchain.tools.file_management.write import WriteFileTool
from langchain.tools.file_management.read import ReadFileTool

# claim the embeddings model
EMBEDDING_MODEL_LOCAL = "text-embedding-ada-002-v2"
embedding = OpenAIEmbeddings()

# fuction to search for the answer in google
search = SerpAPIWrapper()

# function to search for the answer in vectordb
def search_in_db(question, vectordb):
    db_q = Chroma(persist_directory="./chroma", embedding_function=embeddings,collection_name="test_all")
    retriever_q = db_q.as_retriever(chunk_size=1)
    return retriever_q

tools = [
    Tool(
        name="searchInGoogle",
        func=search.run,
        description="useful when you need to answer questions about current events but can not get answer from searchInDB. You should ask targeted questions",
    ),
    Tool(
        name="searchInDB",
        func=search_in_db,
        description="when you need to answer questions about current events, use this tool firstly. You should ask targeted questions",
    ),  # search vector store tool
    HumanInputRun(),    # human input tool
    WriteFileTool(),    # write file tool
    ReadFileTool(),     # read file tool
]

# OpenAI Embedding 模型
embeddings_model = OpenAIEmbeddings()
import chromadb
from langchain_community.vectorstores import Chroma
from langchain_community.docstore import InMemoryDocstore

persist_directory = './chroma'
embedding = OpenAIEmbeddings()

vectordb2 = Chroma(persist_directory=persist_directory, 
                  embedding_function=embedding,
                   )

from langchain_experimental.autonomous_agents import AutoGPT
from langchain_community.chat_models import ChatOpenAI

agent = AutoGPT.from_llm_and_tools(
    ai_name="Jarvis",
    ai_role="Assistant",
    tools=tools,
    llm=ChatOpenAI(model_name="gpt-4", temperature=0, verbose=True),
    memory=vectordb2.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"score_threshold": 0.8}),# 实例化 Chromadb 的 VectorStoreRetriever
)
agent.chain.verbose = True

agent.run(["我现在想要shutdown replication server，需要执行什么指令，请按顺序给出指令，谢谢"])
