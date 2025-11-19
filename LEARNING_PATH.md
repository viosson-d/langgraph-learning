# 🚀 LangGraph 完整学习路径

## 📚 学习资源汇总

你已经有了完整的 LangGraph 学习资源！下面是推荐的学习顺序：

### 第 1 阶段：基础概念（15分钟）
**文件：** `LANGGRAPH_GUIDE.md`
- 快速了解 LangGraph 的核心四步
- 学习 State、Node、Edge 的概念
- 查看常见用法示例

**阅读指令：**
```bash
cat /Users/viosson/LANGGRAPH_GUIDE.md | less
```

---

### 第 2 阶段：动手实验（30分钟）
**文件：** `langgraph_tutorial.py`
- 5个从易到难的实例
- 每个示例都可以直接运行
- 涵盖：顺序执行、条件分支、循环、对话系统

**运行指令：**
```bash
python3 /Users/viosson/langgraph_tutorial.py
```

**学习内容：**
1. ✅ 简单顺序流：字符串处理
2. ✅ 条件分支：根据输入选择路径
3. ✅ 任务序列：多步骤处理
4. ✅ 循环重试：直到条件满足
5. ✅ AI 对话系统：综合应用

---

### 第 3 阶段：进阶示例（20分钟）
**文件：** `langgraph_complete_demo.py`
- 展示本地追踪功能
- 生成 ASCII 图形化结构
- 导出 JSON 追踪日志

**运行指令：**
```bash
python3 /Users/viosson/langgraph_complete_demo.py
```

**输出包括：**
- 📊 图结构可视化
- ✅ 处理步骤日志
- 💾 JSON 追踪文件

---

### 第 4 阶段：实战项目（30分钟）
**文件：** `langgraph_survey_project.py`
- 真实场景：智能问卷处理系统
- 演示如何构建完整的业务流程
- 包含错误处理和数据导出

**运行指令：**
```bash
python3 /Users/viosson/langgraph_survey_project.py
```

**项目特点：**
- 📋 输入验证和清洗
- 🔍 条件路由和错误处理
- 📝 生成报告和导出数据
- 📊 流程图可视化

---

## 🎯 按需求快速查找

### 我想要...

#### 1. 学习基础概念
```bash
cat /Users/viosson/LANGGRAPH_GUIDE.md
```

#### 2. 看实时运行的例子
```bash
python3 /Users/viosson/langgraph_tutorial.py
```

#### 3. 了解数据追踪
```bash
python3 /Users/viosson/langgraph_offline_tracking.py
```

#### 4. 看实战项目
```bash
python3 /Users/viosson/langgraph_survey_project.py
```

#### 5. 使用 Langfuse 云端追踪
编辑 `/Users/viosson/langgraph_langfuse.py`，添加 API Key

---

## 💡 快速参考

### 最简单的图
```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class State(TypedDict):
    text: str

def process(state):
    state["text"] += " processed"
    return state

graph = StateGraph(State)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)

app = graph.compile()
result = app.invoke({"text": "hello"})
print(result["text"])  # "hello processed"
```

### 带条件分支的图
```python
def route(state):
    return "a" if state["flag"] else "b"

graph.add_conditional_edges(
    "start",
    route,
    {"a": "node_a", "b": "node_b"}
)
```

### 循环结构
```python
graph.add_conditional_edges(
    "process",
    lambda s: "retry" if s["tries"] < 3 else "done",
    {"retry": "process", "done": END}
)
```

---

## 📊 文件详解

| 文件 | 大小 | 学习时间 | 难度 | 用途 |
|------|------|---------|------|------|
| LANGGRAPH_GUIDE.md | 6.4K | 15分钟 | ⭐ | 概念和API参考 |
| langgraph_tutorial.py | 8.5K | 30分钟 | ⭐⭐ | 5个实例从易到难 |
| langgraph_survey_project.py | 8.5K | 30分钟 | ⭐⭐ | 完整项目示例 |
| langgraph_complete_demo.py | 3.7K | 15分钟 | ⭐ | 追踪和可视化 |
| langgraph_offline_tracking.py | 2.7K | 10分钟 | ⭐ | 本地追踪演示 |
| langgraph_langfuse.py | 1.9K | 10分钟 | ⭐⭐ | 云端追踪集成 |

---

## 🔥 常用命令速查

```bash
# 运行所有教程
python3 /Users/viosson/langgraph_tutorial.py

# 运行实战项目
python3 /Users/viosson/langgraph_survey_project.py

# 查看快速参考
cat /Users/viosson/LANGGRAPH_GUIDE.md

# 查看导出的结果
cat /Users/viosson/survey_results.json
cat /Users/viosson/langgraph_traces.json

# 编辑代码
code /Users/viosson/langgraph_tutorial.py
```

---

## 🎓 学习路线建议

### 初学者（1-2天）
1. 阅读 `LANGGRAPH_GUIDE.md`（15分钟）
2. 运行 `langgraph_tutorial.py`（30分钟）
3. 修改代码，尝试自己的想法（30分钟）

### 进阶用户（2-3天）
1. 学习 `langgraph_survey_project.py`（30分钟）
2. 理解项目中的设计模式（30分钟）
3. 基于项目模板创建自己的应用（1小时+）

### 生产环境（3-5天）
1. 集成 Langfuse 追踪（`langgraph_langfuse.py`）
2. 添加错误处理和日志
3. 性能优化和测试
4. 部署到生产环境

---

## 🚀 下一步行动

### 快速开始（5分钟）
```bash
# 1. 进入目录
cd /Users/viosson

# 2. 运行一个示例
python3 langgraph_tutorial.py

# 3. 查看结果
cat langgraph_traces.json
```

### 创建自己的项目（30分钟）
```python
# 新建文件：my_app.py
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class MyState(TypedDict):
    input: str

# ... 按照教程编写你的代码
```

### 集成追踪（15分钟）
参考 `langgraph_langfuse.py`，添加 Langfuse 回调

---

## ❓ 常见问题

### Q：LangGraph 能做什么？
A：建立复杂的多步骤处理流程，包括：
- 顺序执行
- 条件分支
- 循环重试
- 并行处理
- 与 LLM 集成

### Q：如何调试我的图？
A：使用 `app.get_graph().draw_ascii()` 查看结构，使用 `app.stream()` 逐步执行

### Q：如何保存追踪数据？
A：参考 `langgraph_offline_tracking.py`，导出为 JSON 或连接 Langfuse

### Q：能在生产环境使用吗？
A：完全可以！LangGraph 是企业级框架，支持并发、错误处理、监控等

---

## 📖 官方资源

- 官方文档：https://langchain-ai.github.io/langgraph/
- GitHub：https://github.com/langchain-ai/langgraph
- LLM 集成：https://python.langchain.com/docs/

---

## 💬 获取帮助

### 遇到问题？
1. 查看 `LANGGRAPH_GUIDE.md` 中的"常见错误"章节
2. 运行对应的教程文件看示例
3. 检查 Python 版本和包版本

### 查看已安装的包
```bash
pip list | grep -i "lang"
```

### 更新包
```bash
pip install --upgrade langgraph langchain
```

---

**准备好了吗？开始你的 LangGraph 之旅吧！** 🚀

建议从这里开始：
```bash
python3 /Users/viosson/langgraph_tutorial.py
```
