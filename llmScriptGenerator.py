from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.agents import load_tools, initialize_agent
from langchain.agents import AgentType
from langchain.agents import Tool
from langchain.tools.file_management.write import WriteFileTool
from langchain.tools.file_management.read import ReadFileTool
from langchain_community.tools.human.tool import HumanInputRun

from langchain_community.vectorstores import Chroma

# function to search for the answer in vectordb
def search_in_db(question, vectordb):
    db_q = Chroma(persist_directory="./chroma", embedding_function=embeddings,collection_name="test_all")
    retriever_q = db_q.as_retriever(chunk_size=1)
    return retriever_q

llm = ChatOpenAI(temperature=0.0)
tools = [
    Tool(
        name="searchInDB",
        func=search_in_db,
        description="when you need to answer questions about current events, use this tool firstly. You should ask targeted questions",
    ),  # search vector store tool
    HumanInputRun(),    # human input tool
    WriteFileTool(),    # write file tool
    ReadFileTool(),     # read file tool
]
 
agent_chain = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    
)
 