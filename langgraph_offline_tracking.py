"""
完全离线的 Langfuse + LangGraph 集成方案
不需要 Docker，直接用 Python
"""

import os
import json
from typing import TypedDict
from datetime import datetime

# ==================== 模拟本地 Langfuse 追踪引擎 ====================

class LocalLangfuseTracker:
    """本地追踪系统 - 当 Langfuse 服务不可用时使用"""
    
    def __init__(self, project_name: str = "default"):
        self.project_name = project_name
        self.traces: list = []
        self.trace_log_file = f"langfuse_traces_{project_name}.jsonl"
        
    def log_trace(self, trace_data: dict):
        """记录追踪数据到本地文件"""
        trace_with_time = {
            **trace_data,
            "timestamp": datetime.now().isoformat(),
            "project": self.project_name
        }
        self.traces.append(trace_with_time)
        
        # 追加到文件
        with open(self.trace_log_file, "a") as f:
            f.write(json.dumps(trace_with_time, ensure_ascii=False) + "\n")
        
        print(f"✅ 追踪已记录: {trace_data.get('name', 'unnamed')}")
        return trace_with_time

# ==================== LangGraph 示例 ====================

from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    input: str
    output: str
    trace_id: str

# 创建本地追踪器
tracker = LocalLangfuseTracker(project_name="langgraph_demo")

# 定义节点
def process_node(state: State) -> State:
    """处理节点"""
    tracker.log_trace({
        "name": "process_node",
        "type": "node",
        "input": state["input"],
        "status": "processing"
    })
    state["output"] = f"处理完成: {state['input']}"
    return state

def analyze_node(state: State) -> State:
    """分析节点"""
    tracker.log_trace({
        "name": "analyze_node",
        "type": "node",
        "input": state["output"],
        "status": "analyzing"
    })
    state["output"] = f"{state['output']} → 分析完成"
    return state

# 构建图
graph = StateGraph(State)
graph.add_node("process", process_node)
graph.add_node("analyze", analyze_node)
graph.add_edge(START, "process")
graph.add_edge("process", "analyze")
graph.add_edge("analyze", END)

compiled_graph = graph.compile()

# 运行
print("=" * 50)
print("🚀 启动 LangGraph + 本地 Langfuse 追踪")
print("=" * 50)

result = compiled_graph.invoke({
    "input": "Hello LangGraph",
    "output": "",
    "trace_id": "trace_001"
})

print(f"\n📊 最终结果: {result['output']}")
print(f"\n💾 追踪已保存到: {tracker.trace_log_file}")
print(f"📈 总追踪数: {len(tracker.traces)}")

# 显示追踪日志
print("\n" + "=" * 50)
print("追踪日志内容:")
print("=" * 50)
for trace in tracker.traces:
    print(json.dumps(trace, ensure_ascii=False, indent=2))
