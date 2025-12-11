from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langfuse.langchain import CallbackHandler
import os
from langchain.chat_models import init_chat_model
from langfuse import get_client
 
# Get keys for your project from the project settings page: https://cloud.langfuse.com
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-d279ccda-a7fd-4dda-9d3b-17c69596eca2" 
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-ae8c1d7b-0b29-4e96-b8a0-1ea13bec2aeb" 
os.environ["LANGFUSE_HOST"] = "https://cloud.langfuse.com" # 🇪🇺 EU region


os.environ["GOOGLE_API_KEY"] = "AIzaSyAI1Gvb8RxKbmBUThElOf0qDqUb_clQQBc"


 
langfuse = get_client()
 
# Verify connection
if langfuse.auth_check():
    print("Langfuse client is authenticated and ready!")
else:
    print("Authentication failed. Please check your credentials and host.")

llm = init_chat_model("google_genai:gemini-2.0-flash")

langfuse_handler = CallbackHandler()

#llm = init_chat_model("google_genai:gemini-2.0-flash")

# Define state
class State(TypedDict):
    input_file_path: str
    file_content: str
    medical_entities: str
    layman_summary: str
    recommendations: str
        

# 🧾 Step 1: Extract raw medical content (text block or structured)
def extract_text(state: State):
    prompt = (
        "You are a skilled medical AI assistant. Extract structured data from this diagnostic report.\n\n"
        "Return ONLY a **valid JSON object** with key medical parameters like vitals, lab values, and diagnoses.\n"
        "Do not include any explanations, markdown, or extra text.\n\n"
        f"Report content:\n{state['input_file_path']}"  # Replace with actual text if preprocessed
    )
    result = llm.invoke(prompt)
    return {"file_content": result.content.strip()}


# 🧠 Step 2: Extract medical entities or summarize the extracted data
def extract_entities(state: State):
    prompt = (
        "Extract important medical entities from this structured report content. "
        "Focus on vitals, lab values, conditions, and abnormalities.\n\n"
        f"{state['file_content']}"
    )
    result = llm.invoke(prompt)
    return {"medical_entities": result.content.strip()}


# 💬 Step 3: Translate  medical data to layman summary
def summarize_layman(state: State):
    prompt = (
        "Explain the following medical findings in simple terms for a non-medical person:\n\n"
        f"{state['medical_entities']}"
    )
    result = llm.invoke(prompt)
    return {"layman_summary": result.content.strip()}


# 🏃‍♀️ Step 4: Suggest lifestyle recommendations
def recommend_lifestyle(state: State):
    prompt = (
        "Based on these simplified findings, suggest appropriate and practical lifestyle changes:\n\n"
        f"{state['layman_summary']}"
    )
    result = llm.invoke(prompt)
    return {"recommendations": result.content.strip()}

# Build workflow
workflow = StateGraph(State)

workflow.add_node("extract_text", extract_text)
workflow.add_node("extract_entities", extract_entities)
workflow.add_node("summarize_layman", summarize_layman)
workflow.add_node("recommend_lifestyle", recommend_lifestyle)

# Define edges
workflow.add_edge(START, "extract_text")
workflow.add_edge("extract_text", "extract_entities")
workflow.add_edge("extract_entities", "summarize_layman")
workflow.add_edge("summarize_layman", "recommend_lifestyle")
workflow.add_edge("recommend_lifestyle", END)

# Compile chain
chain = workflow.compile()

# Show workflow
#display(Image(chain.get_graph().draw_mermaid_png()))

# Simulate run
state = chain.invoke({"input_file_path": './reports_simplification/lft.webp'},
                    config={"callbacks": [langfuse_handler]})
print("Extracted Content:\n", state["file_content"])
print("\nEntities:\n", state["medical_entities"])
print("\nSummary:\n", state["layman_summary"])
print("\nRecommendations:\n", state["recommendations"])

# Initialize Langfuse CallbackHandler for Langchain (tracing)

 #masndjebifewrnfig
