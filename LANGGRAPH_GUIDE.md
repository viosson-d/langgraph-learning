# LangGraph 快速参考指南

## 核心四步：定义 → 构建 → 编译 → 运行

### 第1步：定义状态结构
```python
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class MyState(TypedDict):
    input: str      # 输入数据
    output: str     # 输出数据
    history: list   # 历史记录
```

### 第2步：定义处理节点
```python
def node_function(state: MyState) -> MyState:
    # 处理数据
    state["output"] = f"处理: {state['input']}"
    return state
```

### 第3步：构建图结构
```python
graph = StateGraph(MyState)

# 添加节点
graph.add_node("node1", node_function)
graph.add_node("node2", another_function)

# 连接节点
graph.add_edge(START, "node1")
graph.add_edge("node1", "node2")
graph.add_edge("node2", END)

# 或者使用条件分支
def route_decision(state: MyState) -> str:
    if condition:
        return "path_a"
    return "path_b"

graph.add_conditional_edges(
    "node1",
    route_decision,
    {"path_a": "node2", "path_b": "node3"}
)
```

### 第4步：编译和运行
```python
app = graph.compile()

# 运行
result = app.invoke({
    "input": "Hello",
    "output": "",
    "history": []
})

print(result)  # 查看结果
```

---

## 常见用法示例

### 1. 简单的顺序流程
```python
# 数据流：START → 预处理 → 处理 → 后处理 → END
graph.add_edge(START, "preprocess")
graph.add_edge("preprocess", "process")
graph.add_edge("process", "postprocess")
graph.add_edge("postprocess", END)
```

### 2. 条件判断（if-else）
```python
def should_retry(state):
    if state["error"]:
        return "retry"
    return "success"

graph.add_conditional_edges(
    "process",
    should_retry,
    {
        "retry": "process",      # 重新执行 process
        "success": END
    }
)
```

### 3. 循环（直到条件满足）
```python
graph.add_edge("try_operation", "check_condition")
graph.add_conditional_edges(
    "check_condition",
    lambda state: "retry" if not state["success"] else "done",
    {
        "retry": "try_operation",  # 循环回 try_operation
        "done": END
    }
)
```

### 4. 多分支流程
```python
# 并行开始处理
graph.add_edge(START, "analyze")
graph.add_edge(START, "fetch")
graph.add_edge(START, "validate")

# 等待都完成
graph.add_edge("analyze", "combine")
graph.add_edge("fetch", "combine")
graph.add_edge("validate", "combine")
graph.add_edge("combine", END)
```

---

## 实际应用场景

### 场景 1：数据处理管道
```
用户输入 → 验证 → 清洗 → 分析 → 生成报告 → 输出
```

### 场景 2：决策树
```
           → 是否满足条件1? → 路径A
         /
用户输入 →  
         \
           → 是否满足条件2? → 路径B
```

### 场景 3：重试机制
```
尝试操作 → 成功? → 是 → 输出结果
                 → 否 → 重新尝试 (循环)
```

### 场景 4：AI 助手
```
用户消息 → 理解意图 → 检索信息 → 生成回复 → 输出
```

---

## 关键方法速查

| 方法 | 用途 | 示例 |
|------|------|------|
| `add_node(name, func)` | 添加节点 | `graph.add_node("step1", func)` |
| `add_edge(from, to)` | 连接两个节点 | `graph.add_edge("step1", "step2")` |
| `add_conditional_edges(from, func, map)` | 条件分支 | `graph.add_conditional_edges("check", decide, {})` |
| `compile()` | 生成可执行应用 | `app = graph.compile()` |
| `invoke(input_data)` | 同步运行图 | `result = app.invoke({})` |
| `stream(input_data)` | 流式运行（分步输出）| `for step in app.stream({})` |

---

## 状态管理最佳实践

### ✅ 好的做法
```python
def process_node(state: MyState) -> MyState:
    # 直接修改 state
    state["result"] = compute(state["input"])
    return state  # 必须返回更新后的 state
```

### ❌ 避免
```python
def bad_node(state: MyState) -> None:
    # ❌ 不返回值
    state["result"] = "something"

def bad_node2(state: MyState):
    # ❌ 直接修改全局变量
    global_var.append(state["input"])
```

---

## 调试技巧

### 查看图的结构
```python
# ASCII 图形化
print(app.get_graph().draw_ascii())

# Mermaid 图表
print(app.get_graph().draw_mermaid())
```

### 流式执行（观察每一步）
```python
for step_output in app.stream(input_data):
    print("Step:", step_output)
```

### 添加日志
```python
def logged_node(state: MyState) -> MyState:
    print(f"Node input: {state}")
    result = process(state)
    print(f"Node output: {result}")
    return result
```

---

## 常见错误及解决方案

### 错误 1：State 字段未初始化
```python
# ❌ 错误：字段不存在
state["new_field"] = value  # 会导致错误

# ✅ 正确：在定义时初始化
class MyState(TypedDict):
    new_field: str

# 或在 invoke 时提供初值
result = app.invoke({"new_field": "default"})
```

### 错误 2：节点没有返回值
```python
# ❌ 错误
def bad_node(state):
    state["value"] = 123  # 忘记返回

# ✅ 正确
def good_node(state):
    state["value"] = 123
    return state  # 必须返回
```

### 错误 3：条件分支的返回值不匹配
```python
# ❌ 错误：返回值 "path_a" 不在映射中
def router(state):
    return "path_a"  # 但条件映射中没有这个键

# ✅ 正确
graph.add_conditional_edges(
    "node",
    router,
    {"path_a": "next_node"}  # 确保返回值在这个字典中
)
```

---

## 完整最小示例

```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class State(TypedDict):
    input: str

def process(state: State) -> State:
    state["input"] = f"处理: {state['input']}"
    return state

graph = StateGraph(State)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)

app = graph.compile()
result = app.invoke({"input": "Hello"})
print(result)  # {'input': '处理: Hello'}
```

---

## 进阶功能

### 子图：复用图结构
```python
# 定义子图
sub_graph = StateGraph(State)
# ... 构建子图

# 在主图中引用
graph.add_node("sub_process", sub_graph.compile())
```

### 内存/持久化
```python
# Langfuse 集成（见 langgraph_langfuse.py）
from langfuse.callback import CallbackHandler

callback = CallbackHandler(...)
result = app.invoke(input_data, config={"callbacks": [callback]})
```

---

更多学习资源：
- 官方文档：https://langchain-ai.github.io/langgraph/
- 本教程脚本：`langgraph_tutorial.py`
- 追踪集成：`langgraph_langfuse.py`
