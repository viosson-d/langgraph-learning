"""
完全本地的 LangGraph + Langfuse 追踪方案
不依赖 Docker，直接用 Langfuse SDK
"""

from langfuse import Langfuse
from langgraph.graph import StateGraph, START, END
from typing import TypedDict
import os

# ==================== 方案 1: 本地文件存储追踪 ====================

class OfflineTracker:
    """本地文件系统追踪器"""
    def __init__(self):
        self.traces = []
        
    def track(self, name: str, input_data: str, output_data: str):
        """记录追踪"""
        self.traces.append({
            "name": name,
            "input": input_data,
            "output": output_data
        })
        print(f"✅ 追踪: {name}")

offline_tracker = OfflineTracker()

# ==================== 定义状态 ====================

class State(TypedDict):
    input: str
    output: str

# ==================== 定义节点 ====================

def node_1(state: State) -> State:
    """第一个处理节点"""
    state["output"] = f"Step 1: 处理 '{state['input']}'"
    offline_tracker.track("node_1", state["input"], state["output"])
    return state

def node_2(state: State) -> State:
    """第二个处理节点"""
    state["output"] = f"{state['output']} → Step 2: 分析完成"
    offline_tracker.track("node_2", state["output"].split(" → ")[0], state["output"])
    return state

def node_3(state: State) -> State:
    """第三个处理节点"""
    state["output"] = f"{state['output']} → Step 3: 最终输出"
    offline_tracker.track("node_3", state["output"].split(" → ")[-2], state["output"])
    return state

# ==================== 构建图 ====================

graph = StateGraph(State)
graph.add_node("step1", node_1)
graph.add_node("step2", node_2)
graph.add_node("step3", node_3)

graph.add_edge(START, "step1")
graph.add_edge("step1", "step2")
graph.add_edge("step2", "step3")
graph.add_edge("step3", END)

compiled_graph = graph.compile()

# ==================== 可视化图结构 ====================

print("=" * 60)
print("🚀 LangGraph 图结构")
print("=" * 60)
print(compiled_graph.get_graph().draw_ascii())

# ==================== 执行图 ====================

print("\n" + "=" * 60)
print("⚙️  执行流程")
print("=" * 60)

result = compiled_graph.invoke({
    "input": "Hello LangGraph",
    "output": ""
})

print(f"\n✨ 最终结果: {result['output']}")

# ==================== 显示追踪日志 ====================

print("\n" + "=" * 60)
print("📊 追踪日志")
print("=" * 60)
for i, trace in enumerate(offline_tracker.traces, 1):
    print(f"{i}. {trace['name']}: {trace['input']} → {trace['output']}")

# ==================== 方案 2: 连接到 Langfuse 云端（可选） ====================

print("\n" + "=" * 60)
print("💡 如何连接到 Langfuse 云端")
print("=" * 60)
print("""
步骤:
1. 访问 https://cloud.langfuse.com
2. 注册免费账户
3. 获取 API Keys (Public Key 和 Secret Key)
4. 运行以下代码启用云端追踪:

    from langfuse import Langfuse
    
    langfuse = Langfuse(
        public_key="pk_xxx...",
        secret_key="sk_xxx...",
        host="https://cloud.langfuse.com"  # 或使用本地部署
    )
    
    # 使用 langfuse_callback 来追踪
    from langfuse.callback import CallbackHandler
    callback = CallbackHandler(public_key="...", secret_key="...")
    
    # 在 invoke 中传递 callback
    result = compiled_graph.invoke(
        {"input": "...", "output": ""},
        config={"callbacks": [callback]}
    )
""")

# ==================== 导出追踪为 JSON ====================

import json

trace_output_file = "/Users/viosson/langgraph_traces.json"
with open(trace_output_file, "w") as f:
    json.dump(offline_tracker.traces, f, ensure_ascii=False, indent=2)

print(f"\n💾 追踪已导出到: {trace_output_file}")
