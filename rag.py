from langchain_community.document_loaders import WebBaseLoader
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
os.environ["USER_AGENT"] = "MyLangChainAgent/1.0 (contact: you@example.com)"


urls = [
    "https://lilianweng.github.io/posts/2024-11-28-reward-hacking/"
]

docs = [WebBaseLoader(url).load() for url in urls]
#print(docs)



docs_list = [item for sublist in docs for item in sublist]

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=100, chunk_overlap=50
)
doc_splits = text_splitter.split_documents(docs_list)

#doc_splits[0].page_content.strip()

# for doc in doc_splits:
#     print(doc.page_content.strip())      these used to print the chunked doc 



from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
import os
os.environ["GOOGLE_API_KEY"] = "AIzaSyAwUpXzOlV2nJZWT7Pq0OGExbnRZmMr1q4"


embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

vectorstore = InMemoryVectorStore.from_documents(
    documents=doc_splits, 
    embedding=embedding_model
)

retriever = vectorstore.as_retriever()

from langchain.tools.retriever import create_retriever_tool

retriever_tool = create_retriever_tool(
    retriever,
    "retrieve_blog_posts",
    "Search and return information about Lilian Weng blog posts.",
)
input_query = input("Please enter the query: ")  # taking the input quary form the user dynamicaly

respone=retriever_tool.invoke({"query": f"{input_query}"})
print(respone)
