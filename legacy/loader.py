import argparse
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import pathlib
import uuid
from langchain.chains import RetrievalQA,RetrievalQAWithSourcesChain
import os
from langchain.text_splitter import CharacterTextSplitter,RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader,PyPDFLoader
from langchain.vectorstores import Chroma
from llm_commons.langchain.btp_llm import BTPOpenAIEmbeddings
from llm_commons.langchain.btp_llm import BTPOpenAI ,ChatBTPOpenAI
from langchain.document_loaders import WebBaseLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import LanguageParser
import chromadb
from numpy import argsort
from langchain.document_loaders import WebBaseLoader
from langchain.schema import Document
from tqdm.auto import tqdm

#loader = PyPDFLoader('./raw_docs/resume.pdf')
#loader = WebBaseLoader("https://edition.cnn.com/us/live-news/maui-wildfires-08-10-23/index.html")
#documents = loader.load()



import os

def doc_to_document(api):
    metadata=api.metadata
    metadata['id'] = str(uuid.uuid1())
    return Document(page_content=api.page_content,
                    metadata=metadata
                    )

def embed_doc(doc, embeddings_func):
    document = doc_to_document(doc)
    return document, embeddings_func(document.page_content)

def persist_embeddings(docs,embeddings,collection,n_parallel_embeddings=5):
    get_result = collection.get(include=[])
    present_docs = set(get_result.get('ids', []))
    new_docs = docs

    if len(new_docs) > 0:
        documents = []
        embeddings_doc = []
        with ThreadPoolExecutor(max_workers=n_parallel_embeddings) as executor:
            f_add = partial(embed_doc, embeddings_func=embeddings.embed_query)
            for document, emb in tqdm(executor.map(f_add, new_docs), total=len(new_docs)):
                documents.append(document)
                embeddings_doc.append(emb)
        metadatas=[doc.metadata for doc in docs]
        collection.upsert(
            metadatas=metadatas,
            embeddings=embeddings_doc, 
            documents=[doc.page_content for doc in documents],  
            ids=[doc.metadata['id'] for doc in documents])
        
def get_all_docs(root,embeddings,collection):
    filename ="already_loaded"
    file_created=os.path.join(root,filename)
    if len(file_created) > 256:
        return
    
    for paths,dirnames,filenames in os.walk(root):
        if filename in filenames:
            break
        for dir in dirnames:
            print(os.path.join(paths,dir))
            get_all_docs(os.path.join(paths,dir),embeddings,collection)

        for file in filenames:
            documents = [] 
            if file.endswith(".pdf"):
                pdf_path = os.path.join(paths,file)
                print([pdf_path])
                loader = PyPDFLoader(pdf_path)
                documents.extend(loader.load())
            elif file.endswith('.docx') or file.endswith('.doc'):
                doc_path = os.path.join(paths,file)
                print(doc_path)
                try:
                    loader = Docx2txtLoader(doc_path)
                    documents.extend(loader.load())
                    #solution 1:
                    #loader =UnstructuredWordDocumentLoader(doc_path)
                    #solution 2:
                    #try:
                    #    loader = Docx2txtLoader("path/to/file.docx")
                    #    docs = loader.load()
                    #except Exception as e:
                    #    print(f"Error loading docx: {e}")
                except:
                    try:
                        loader = TextLoader(doc_path, autodetect_encoding=True)
                        documents.extend(loader.load())
                    except:
                        print("Unable to load file:"+doc_path)

            elif file.endswith('.tcf') or file.endswith(".tcl")  or file.endswith('.html') or file.endswith('.txt'):
                text_path = os.path.join(paths,file)
                print(text_path)
                try:
                    loader = TextLoader(text_path, autodetect_encoding=True)
                    documents.extend(loader.load())
                except:
                    print("Unable to load file:"+text_path)	
            elif file.endswith('.java'):
                text_path = os.path.join(paths,file)
                print(text_path)
                try:
                    loader = TextLoader(text_path, autodetect_encoding=True)
                    documents.extend(loader.load())
                except:
                    print("Unable to load file:"+text_path)

            elif file.endswith('.c') or file.endswith('.cc'):    
                text_path = os.path.join(paths,file)
                print(text_path)
                try:
                    loader = TextLoader(text_path, autodetect_encoding=True)
                    documents.extend(loader.load())
                except:
                    print("Unable to load file:"+text_path)
            elif file.endswith('.cpp'):
                text_path = os.path.join(paths,file)
                print(text_path)
                try:
                    loader = TextLoader(text_path, autodetect_encoding=True)
                    documents.extend(loader.load())
                except:
                    print("Unable to load file:"+text_path) 
            elif file.endswith('_h') or file.endswith('.h'):
                text_path = os.path.join(paths,file)
                print(text_path)
                try:
                    loader = TextLoader(text_path, autodetect_encoding=True)
                    documents.extend(loader.load())
                except:
                    print("Unable to load file:"+text_path)

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=128)
            texts = text_splitter.split_documents(documents)
            persist_embeddings(texts,embeddings,collection)
            
        pathlib.Path(file_created).touch()

model = "gpt-4-32k"
#llm = BTPOpenAI(deployment_id=deployment_id)  # can be used as usual with langchain
llm = ChatBTPOpenAI(deployment_id=model, temperature=0, token=32768)

#llm = ChatBTPOpenAI(deployment_id=model, temperature=0, token=32768, stream=true)
#text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
#texts = text_splitter.split_documents(documents)

EMBEDDING_MODEL_LOCAL = "text-embedding-ada-002-v2"
embeddings = BTPOpenAIEmbeddings(deployment_id=EMBEDDING_MODEL_LOCAL, chunk_size=10)


#db = Chroma.from_documents(texts, embedding=embeddings, persist_directory="./data_test_src")

persistent_client = chromadb.PersistentClient()

db = Chroma(
    client=persistent_client,
    collection_name="test_all",
    embedding_function=embeddings,
    persist_directory="./chroma"
)

collection = persistent_client.get_or_create_collection("test_all")

dir_to_search ="./docs"
get_all_docs(dir_to_search,embeddings,collection)

#db = Chroma(persist_directory="./data_test_src", embedding_function=embeddings)
retriever = db.as_retriever()

chain = RetrievalQAWithSourcesChain.from_chain_type(llm, chain_type="stuff", retriever=retriever, reduce_k_below_max_tokens=True,)
parser = argparse.ArgumentParser(description='Ask a question to the notion DB.')
parser.add_argument('question', type=str, help='The question to ask the notion DB')
args = parser.parse_args()
result = chain({"question": args.question})
print(f"Answer: {result['answer']}")
print(f"Sources: {result['sources']}")
'''
qa = RetrievalQA.from_llm(llm=llm, retriever=retriever)  # pass the BTP OpenAI model


query = args.question
print("Ask:"+query+"\n")
print("Reply:"+qa.run(query))
'''
