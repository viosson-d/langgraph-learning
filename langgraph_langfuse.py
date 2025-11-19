import os
from langfuse.callback import CallbackHandler
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# 配置 Langfuse（本地或云端）
# 选项1: 使用 Langfuse Cloud
# os.environ["LANGFUSE_PUBLIC_KEY"] = "your-public-key"
# os.environ["LANGFUSE_SECRET_KEY"] = "your-secret-key"
# os.environ["LANGFUSE_HOST"] = "https://cloud.langfuse.com"  # 默认值

# 选项2: 使用本地 Langfuse
os.environ["LANGFUSE_HOST"] = "http://localhost:3000"  # 本地部署
# os.environ["LANGFUSE_PUBLIC_KEY"] = "your-public-key"
# os.environ["LANGFUSE_SECRET_KEY"] = "your-secret-key"

# 初始化 Langfuse callback
langfuse_callback = CallbackHandler(
    public_key="default-public-key",
    secret_key="default-secret-key",
    host="http://localhost:3000"  # 使用本地部署
)

# 定义状态
class State(TypedDict):
    input: str
    output: str

# 创建图
graph = StateGraph(State)

# 定义节点
def process_node(state: State) -> State:
    """处理输入"""
    state["output"] = f"处理完成: {state['input']}"
    return state

def analyze_node(state: State) -> State:
    """分析输出"""
    state["output"] = f"{state['output']} -> 分析完成"
    return state

# 添加节点
graph.add_node("process", process_node)
graph.add_node("analyze", analyze_node)

# 添加边
graph.add_edge(START, "process")
graph.add_edge("process", "analyze")
graph.add_edge("analyze", END)

# 编译图
compiled_graph = graph.compile()

# 运行图（集成 Langfuse 追踪）
try:
    result = compiled_graph.invoke(
        {"input": "Hello LangGraph with Langfuse", "output": ""},
        config={"callbacks": [langfuse_callback]}
    )
    print(f"✅ 结果: {result}")
    print("\n📊 追踪已发送到 Langfuse！请访问你的 Langfuse 仪表板查看。")
except Exception as e:
    print(f"⚠️ 如果看到连接错误，请确保已配置 Langfuse 凭证或启动了本地服务器")
    print(f"错误: {e}")
