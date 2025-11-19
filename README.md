# 🎯 LangGraph 学习和项目资源

欢迎使用 LangGraph！这个目录包含了完整的学习资源和实战项目。

## 📂 文件结构

```
/Users/viosson/
├── 📖 LEARNING_PATH.md              ← 从这里开始！推荐学习路径
├── 📖 LANGGRAPH_GUIDE.md            ← 核心概念和 API 参考
├── 📖 LANGFUSE_CONFIG.md            ← Langfuse 配置指南
│
├── 🐍 langgraph_tutorial.py         ← 5个教学示例（推荐！）
├── 🐍 langgraph_survey_project.py   ← 完整项目示例
├── 🐍 langgraph_complete_demo.py    ← 追踪和可视化演示
├── 🐍 langgraph_offline_tracking.py ← 本地追踪示例
├── 🐍 langgraph_langfuse.py         ← 云端追踪集成
├── 🐍 langgraph_demo.py             ← 简单示例
│
└── 📊 输出文件
    ├── langgraph_traces.json        ← 追踪日志
    └── survey_results.json          ← 项目输出
```

## 🚀 快速开始（5分钟）

### 1️⃣ 查看学习路径
```bash
cat /Users/viosson/LEARNING_PATH.md
```

### 2️⃣ 运行第一个示例
```bash
python3 /Users/viosson/langgraph_tutorial.py
```

### 3️⃣ 运行完整项目
```bash
python3 /Users/viosson/langgraph_survey_project.py
```

## 📚 学习路线

### 初级（1天）
- [ ] 读 `LEARNING_PATH.md`（5分钟）
- [ ] 读 `LANGGRAPH_GUIDE.md`（15分钟）
- [ ] 运行 `langgraph_tutorial.py`（30分钟）
- [ ] 修改代码并再次运行（30分钟）

### 中级（2-3天）
- [ ] 理解 `langgraph_survey_project.py`（1小时）
- [ ] 基于项目创建自己的应用（2-3小时）
- [ ] 添加错误处理和日志（1小时）

### 高级（3-5天）
- [ ] 集成 Langfuse 追踪（1小时）
- [ ] 优化性能和并发（2小时）
- [ ] 部署到生产环境（2-3小时）

## 🎓 核心概念速览

### State（状态）
在图中流动的数据结构：
```python
class MyState(TypedDict):
    input: str
    output: str
```

### Node（节点）
处理数据的函数：
```python
def process(state: MyState) -> MyState:
    state["output"] = state["input"].upper()
    return state
```

### Edge（边）
连接节点的路径：
```python
graph.add_edge(START, "process")
graph.add_edge("process", END)
```

## 🔥 常用命令

```bash
# 运行所有示例
python3 /Users/viosson/langgraph_tutorial.py        # 5个教学示例
python3 /Users/viosson/langgraph_survey_project.py  # 完整项目
python3 /Users/viosson/langgraph_complete_demo.py   # 追踪演示

# 查看输出
cat /Users/viosson/langgraph_traces.json
cat /Users/viosson/survey_results.json

# 编辑代码
code /Users/viosson/langgraph_tutorial.py
```

## 💡 使用场景示例

### 1. 数据处理管道
```
输入 → 验证 → 清洗 → 分析 → 输出
```

### 2. AI 对话系统
```
用户输入 → 理解意图 → 检索信息 → 生成回复 → 输出
```

### 3. 决策树
```
输入 → 判断条件 → 路径A/B/C → 处理 → 输出
```

### 4. 重试机制
```
尝试 → 失败? → 重试 → 成功/失败 → 输出
```

## 🛠️ 关键方法

| 方法 | 用途 |
|------|------|
| `StateGraph(State)` | 创建图 |
| `add_node(name, func)` | 添加节点 |
| `add_edge(from, to)` | 连接节点 |
| `add_conditional_edges()` | 条件分支 |
| `compile()` | 编译图 |
| `invoke(input)` | 运行图 |
| `stream(input)` | 流式运行 |
| `get_graph().draw_ascii()` | 可视化 |

## 📊 项目成果

完成学习后，你可以：
- ✅ 构建复杂的多步骤流程
- ✅ 实现条件判断和循环
- ✅ 集成 LLM 进行 AI 应用
- ✅ 添加错误处理和日志
- ✅ 追踪和监控流程执行
- ✅ 部署到生产环境

## 🔗 相关资源

- [官方文档](https://langchain-ai.github.io/langgraph/)
- [GitHub 仓库](https://github.com/langchain-ai/langgraph)
- [LangChain 文档](https://python.langchain.com/)
- [Langfuse 文档](https://langfuse.com/)

## 💬 需要帮助？

1. 查看 `LANGGRAPH_GUIDE.md` 的"常见错误"章节
2. 运行对应的教程文件看示例
3. 修改示例代码进行实验

## 📋 下一步

1. **现在就开始**
   ```bash
   python3 /Users/viosson/langgraph_tutorial.py
   ```

2. **理解项目结构**
   - 阅读 `langgraph_survey_project.py` 的注释

3. **创建自己的项目**
   - 复制一个示例文件
   - 修改代码以适应你的需求
   - 逐步构建你的应用

## ✨ 提示

- 🎯 开始时从简单的例子开始
- 📝 在代码中添加注释理解每一步
- 🧪 尝试修改代码并看看会发生什么
- 📊 使用 `draw_ascii()` 可视化你的图
- 🔍 使用 `stream()` 进行调试

---

**祝你学习愉快！** 🚀

从这里开始：[LEARNING_PATH.md](./LEARNING_PATH.md)
