from langchain_core.messages import HumanMessage
from langgraph.graph import END, StateGraph, START
from langgraph.graph.message import add_messages
from langchain_ollama import ChatOllama
from typing import TypedDict

# 定义状态
class State(TypedDict):
    messages: list

# 初始化 LLM（使用本地 Ollama 模型）
llm = ChatOllama(model="llama3.2")  # 假设你有 llama3.2 模型

# 定义节点函数
def chatbot(state: State):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# 构建图
workflow = StateGraph(State)

# 添加节点
workflow.add_node("chatbot", chatbot)

# 添加边
workflow.add_edge(START, "chatbot")
workflow.add_edge("chatbot", END)

# 编译图
app = workflow.compile()

# 运行示例
if __name__ == "__main__":
    initial_message = HumanMessage(content="Hello! How can I help you today?")
    result = app.invoke({"messages": [initial_message]})
    print(result["messages"][-1].content)