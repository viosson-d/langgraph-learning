import os
from dotenv import load_dotenv
from langfuse import Langfuse
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# 加载环境变量
load_dotenv()

# 获取配置
langfuse_host = os.getenv("LANGFUSE_HOST", "http://localhost:3000")
langfuse_public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
langfuse_secret_key = os.getenv("LANGFUSE_SECRET_KEY")

if not langfuse_public_key or "..." in langfuse_public_key:
    print("⚠️  请先配置 .env 文件中的 Langfuse 密钥！")
    exit(1)

from langfuse import Langfuse

# 加载环境变量
load_dotenv()

# 获取配置
langfuse_host = os.getenv("LANGFUSE_HOST", "http://localhost:3000")
langfuse_public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
langfuse_secret_key = os.getenv("LANGFUSE_SECRET_KEY")

if not langfuse_public_key or "..." in langfuse_public_key:
    print("⚠️  请先配置 .env 文件中的 Langfuse 密钥！")
    exit(1)

# 初始化 Langfuse 客户端
# langfuse = Langfuse(
#     public_key=langfuse_public_key,
#     secret_key=langfuse_secret_key,
#     host=langfuse_host
# )

# 初始化 Langfuse 客户端
langfuse = Langfuse(
    public_key=langfuse_public_key,
    secret_key=langfuse_secret_key,
    host=langfuse_host
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
    # 使用 Langfuse v3 装饰器
    from langfuse.decorators import observe
    
    @observe(name="process_node")
    def _run(inp):
        return f"处理完成: {inp}"
        
    result = _run(state["input"])
    return {"output": result}

def analyze_node(state: State) -> State:
    """分析输出"""
    # 使用 Langfuse v3 装饰器
    from langfuse.decorators import observe
    
    @observe(name="analyze_node")
    def _run(inp):
        return f"{inp} -> 分析完成"
        
    result = _run(state["output"])
    return {"output": result}


# 添加节点
graph.add_node("process", process_node)
graph.add_node("analyze", analyze_node)

# 构建边
graph.add_edge(START, "process")
graph.add_edge("process", "analyze")
graph.add_edge("analyze", END)

# 编译图
app = graph.compile()

# 运行测试
print("🚀 开始运行 LangGraph + Langfuse 测试...")
inputs = {"input": "Hello Langfuse"}

# 不使用 callbacks，因为我们手动 instrument 了节点
for output in app.stream(inputs):
    for key, value in output.items():
        print(f"Node '{key}': {value}")

# 确保数据发送完成
langfuse.flush()
print("✅ 测试完成！请查看 Langfuse 控制台: http://localhost:3000")

