# LangGraph 快速查找表

## 📖 我想要... 看这个文件

| 我想要... | 文件 | 时间 |
|---------|------|------|
| 快速了解 LangGraph | README.md | 5分钟 |
| 学习推荐路径 | LEARNING_PATH.md | 10分钟 |
| API 参考和快速代码 | LANGGRAPH_GUIDE.md | 15分钟 |
| 配置追踪功能 | LANGFUSE_CONFIG.md | 10分钟 |
| 看 5 个教学例子 | langgraph_tutorial.py | 30分钟 |
| 看完整项目示例 | langgraph_survey_project.py | 30分钟 |
| 看追踪演示 | langgraph_complete_demo.py | 15分钟 |

## 🚀 快速命令

```bash
# 查看文件
cat /Users/viosson/README.md
cat /Users/viosson/LEARNING_PATH.md
cat /Users/viosson/LANGGRAPH_GUIDE.md

# 运行示例
python3 /Users/viosson/langgraph_tutorial.py
python3 /Users/viosson/langgraph_survey_project.py
python3 /Users/viosson/langgraph_complete_demo.py

# 查看输出
cat /Users/viosson/langgraph_traces.json
cat /Users/viosson/survey_results.json

# 编辑代码
code /Users/viosson/langgraph_tutorial.py
nano /Users/viosson/langgraph_tutorial.py
vim /Users/viosson/langgraph_tutorial.py
```

## 💡 最常用的代码片段

### 1. 创建简单的图
```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class State(TypedDict):
    input: str

def process(state):
    state["input"] = state["input"].upper()
    return state

graph = StateGraph(State)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)

app = graph.compile()
result = app.invoke({"input": "hello"})
```

### 2. 条件分支
```python
def route(state):
    return "a" if condition else "b"

graph.add_conditional_edges(
    "check",
    route,
    {"a": "node_a", "b": "node_b"}
)
```

### 3. 循环
```python
graph.add_conditional_edges(
    "process",
    lambda s: "retry" if not s["done"] else "exit",
    {"retry": "process", "exit": END}
)
```

### 4. 可视化图
```python
print(app.get_graph().draw_ascii())
```

### 5. 流式执行
```python
for output in app.stream({"input": "test"}):
    print(output)
```

## 🔑 核心 API

| API | 用途 | 示例 |
|-----|------|------|
| `StateGraph(State)` | 创建图 | `graph = StateGraph(MyState)` |
| `add_node(name, func)` | 添加节点 | `graph.add_node("step", func)` |
| `add_edge(a, b)` | 连接节点 | `graph.add_edge("a", "b")` |
| `add_conditional_edges()` | 条件分支 | `graph.add_conditional_edges("n", router, {})` |
| `compile()` | 编译 | `app = graph.compile()` |
| `invoke(input)` | 同步执行 | `result = app.invoke({})` |
| `stream(input)` | 流式执行 | `for o in app.stream({})` |

## 🎯 常见问题速查

### Q: 如何定义状态？
```python
from typing import TypedDict

class MyState(TypedDict):
    field1: str
    field2: int
    field3: list
```

### Q: 如何添加节点？
```python
def my_node(state: MyState) -> MyState:
    # 修改 state
    state["field1"] = "new value"
    return state

graph.add_node("node_name", my_node)
```

### Q: 如何连接节点？
```python
# 简单连接
graph.add_edge(START, "node1")
graph.add_edge("node1", "node2")
graph.add_edge("node2", END)

# 条件连接
def should_retry(state):
    return "retry" if state["error"] else "success"

graph.add_conditional_edges(
    "process",
    should_retry,
    {"retry": "process", "success": END}
)
```

### Q: 如何可视化图？
```python
# ASCII 图
print(app.get_graph().draw_ascii())

# Mermaid 图表
print(app.get_graph().draw_mermaid())
```

### Q: 如何调试？
```python
# 流式执行，看每一步
for step_output in app.stream(input_data):
    print("Step output:", step_output)

# 添加日志
def logged_node(state):
    print(f"Input: {state}")
    result = process(state)
    print(f"Output: {result}")
    return result
```

### Q: 如何追踪执行？
```python
from langfuse.callback import CallbackHandler

callback = CallbackHandler()
result = app.invoke(
    input_data,
    config={"callbacks": [callback]}
)
```

## 📊 项目模板

### 最小项目
```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class State(TypedDict):
    data: str

def step1(state):
    state["data"] = f"Step1: {state['data']}"
    return state

def step2(state):
    state["data"] = f"Step2: {state['data']}"
    return state

graph = StateGraph(State)
graph.add_node("step1", step1)
graph.add_node("step2", step2)
graph.add_edge(START, "step1")
graph.add_edge("step1", "step2")
graph.add_edge("step2", END)

app = graph.compile()
print(app.invoke({"data": "hello"}))
```

### 带条件的项目
```python
def route_logic(state):
    if state["value"] > 10:
        return "high"
    else:
        return "low"

graph.add_conditional_edges(
    "check",
    route_logic,
    {"high": "process_high", "low": "process_low"}
)
```

### 带循环的项目
```python
def should_continue(state):
    if state["attempt"] < 3:
        return "retry"
    return "done"

graph.add_conditional_edges(
    "try",
    should_continue,
    {"retry": "try", "done": END}
)
```

## 🐛 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| `KeyError: 'field'` | State 字段不存在 | 在 TypedDict 中定义或在 invoke 时提供初值 |
| `Function must return state` | 节点没有返回值 | 确保每个节点函数都 return state |
| `Invalid edge` | 边连接到不存在的节点 | 检查节点名称拼写 |
| `No path found` | 没有连接到 END | 确保所有节点都能到达 END |

## 📚 学习顺序

1. **第1步（5分钟）**: 阅读 README.md
2. **第2步（15分钟）**: 阅读 LANGGRAPH_GUIDE.md
3. **第3步（30分钟）**: 运行 langgraph_tutorial.py
4. **第4步（30分钟）**: 修改代码实验
5. **第5步（1小时）**: 学习 langgraph_survey_project.py
6. **第6步（2小时+）**: 创建自己的项目

## 💬 需要帮助？

- 📖 查看 LANGGRAPH_GUIDE.md
- 🐍 运行对应的 Python 文件查看例子
- 🧪 修改代码进行实验
- 🔍 使用 `draw_ascii()` 可视化图

## ✨ 最后提示

- ✅ 从简单的例子开始
- ✅ 逐步增加复杂度
- ✅ 频繁测试和调试
- ✅ 查看导出的追踪数据
- ✅ 与他人分享你的项目

---

**准备好了吗？**

```bash
python3 /Users/viosson/langgraph_tutorial.py
```

祝你学习愉快！🚀
