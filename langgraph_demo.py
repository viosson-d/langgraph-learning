from langgraph.graph import StateGraph, START, END
from typing import TypedDict

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

# 添加节点
graph.add_node("process", process_node)

# 添加边
graph.add_edge(START, "process")
graph.add_edge("process", END)

# 编译图
compiled_graph = graph.compile()

# 运行图
result = compiled_graph.invoke({"input": "Hello LangGraph", "output": ""})
print(f"结果: {result}")

# 获取图的可视化信息
print("\n图结构:")
print(compiled_graph.get_graph().draw_ascii())
