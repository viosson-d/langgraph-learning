"""
LangGraph 完整使用教程 - 从入门到精通
"""

# ==================== 1. 最简单的例子：顺序执行 ====================

print("\n" + "="*60)
print("1️⃣  最简单的例子：顺序执行")
print("="*60)

from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# 定义状态（State）- 图中流动的数据
class State(TypedDict):
    message: str

# 创建图
graph = StateGraph(State)

# 定义处理函数
def add_hello(state: State) -> State:
    """在消息前添加 'Hello'"""
    state["message"] = f"Hello, {state['message']}"
    return state

def add_exclamation(state: State) -> State:
    """在消息后添加感叹号"""
    state["message"] = f"{state['message']}!"
    return state

# 添加节点
graph.add_node("add_hello", add_hello)
graph.add_node("add_exclamation", add_exclamation)

# 连接节点（START -> add_hello -> add_exclamation -> END）
graph.add_edge(START, "add_hello")
graph.add_edge("add_hello", "add_exclamation")
graph.add_edge("add_exclamation", END)

# 编译并运行
app = graph.compile()
result = app.invoke({"message": "World"})
print(f"输入: 'World'")
print(f"输出: {result['message']}")


# ==================== 2. 条件分支：根据条件选择路径 ====================

print("\n" + "="*60)
print("2️⃣  条件分支：根据条件选择路径")
print("="*60)

class ChatState(TypedDict):
    user_input: str
    response: str

graph2 = StateGraph(ChatState)

def process_input(state: ChatState) -> ChatState:
    """处理用户输入"""
    state["response"] = f"你说: {state['user_input']}"
    return state

def check_intent(state: ChatState) -> str:
    """检查用户意图，返回下一个节点"""
    if "问好" in state["user_input"]:
        return "greet"
    elif "问题" in state["user_input"]:
        return "answer"
    else:
        return "default"

def greet_response(state: ChatState) -> ChatState:
    """问好应答"""
    state["response"] = "你好！很高兴认识你 👋"
    return state

def answer_response(state: ChatState) -> ChatState:
    """回答问题"""
    state["response"] = "这是一个好问题！让我想想... 🤔"
    return state

def default_response(state: ChatState) -> ChatState:
    """默认应答"""
    state["response"] = "我收到了你的消息 📝"
    return state

# 添加节点
graph2.add_node("process", process_input)
graph2.add_node("greet", greet_response)
graph2.add_node("answer", answer_response)
graph2.add_node("default", default_response)

# 添加条件分支
graph2.add_edge(START, "process")
graph2.add_conditional_edges(
    "process",
    check_intent,  # 这个函数决定下一个节点
    {
        "greet": "greet",
        "answer": "answer",
        "default": "default"
    }
)
graph2.add_edge("greet", END)
graph2.add_edge("answer", END)
graph2.add_edge("default", END)

app2 = graph2.compile()

# 测试三种情况
for user_input in ["你好，问好", "我有个问题", "随便说说"]:
    result = app2.invoke({"user_input": user_input, "response": ""})
    print(f"输入: '{user_input}'")
    print(f"输出: {result['response']}\n")


# ==================== 3. 并行节点：顺序执行多个任务 ====================

print("\n" + "="*60)
print("3️⃣  顺序执行多个任务")
print("="*60)

class TaskState(TypedDict):
    task_name: str
    results: list

graph3 = StateGraph(TaskState)

def analyze_task(state: TaskState) -> TaskState:
    """分析任务"""
    state["results"].append("任务已分析 ✓")
    return state

def fetch_data(state: TaskState) -> TaskState:
    """获取数据"""
    state["results"].append("数据已获取 ✓")
    return state

def validate_input(state: TaskState) -> TaskState:
    """验证输入"""
    state["results"].append("输入已验证 ✓")
    return state

# 添加节点
graph3.add_node("analyze", analyze_task)
graph3.add_node("fetch", fetch_data)
graph3.add_node("validate", validate_input)

# 定义执行流（顺序执行）
graph3.add_edge(START, "analyze")
graph3.add_edge("analyze", "fetch")
graph3.add_edge("fetch", "validate")
graph3.add_edge("validate", END)

app3 = graph3.compile()
result = app3.invoke({"task_name": "demo_task", "results": []})
print("任务执行结果:")
for i, result_item in enumerate(result['results'], 1):
    print(f"  {i}. {result_item}")
print(f"\n✅ 所有任务完成")


# ==================== 4. 循环：重复执行直到条件满足 ====================

print("\n" + "="*60)
print("4️⃣  循环：重复执行直到条件满足")
print("="*60)

class RetryState(TypedDict):
    attempt: int
    max_attempts: int
    success: bool
    message: str

graph4 = StateGraph(RetryState)

def try_operation(state: RetryState) -> RetryState:
    """尝试操作"""
    state["attempt"] += 1
    # 模拟：第三次尝试成功
    if state["attempt"] >= 3:
        state["success"] = True
        state["message"] = f"✓ 第 {state['attempt']} 次尝试成功"
    else:
        state["message"] = f"✗ 第 {state['attempt']} 次尝试失败，重试..."
    return state

def should_retry(state: RetryState) -> str:
    """检查是否继续重试"""
    if state["success"] or state["attempt"] >= state["max_attempts"]:
        return "end"
    else:
        return "retry"

# 添加节点
graph4.add_node("try", try_operation)

# 添加条件分支
graph4.add_edge(START, "try")
graph4.add_conditional_edges(
    "try",
    should_retry,
    {"retry": "try", "end": END}
)

app4 = graph4.compile()
result = app4.invoke({"attempt": 0, "max_attempts": 5, "success": False, "message": ""})
print(f"重试过程:")
print(f"  {result['message']}")


# ==================== 5. 高级：结合 LLM 的实际应用 ====================

print("\n" + "="*60)
print("5️⃣  高级示例：AI 对话系统")
print("="*60)

class MessageState(TypedDict):
    user_message: str
    conversation_history: list
    ai_response: str

graph5 = StateGraph(MessageState)

def store_user_message(state: MessageState) -> MessageState:
    """存储用户消息"""
    state["conversation_history"].append({
        "role": "user",
        "content": state["user_message"]
    })
    return state

def generate_response(state: MessageState) -> MessageState:
    """生成 AI 回复（模拟）"""
    # 在实际应用中，这里会调用 LLM API
    if "天气" in state["user_message"]:
        ai_response = "今天天气很好，阳光充足 ☀️"
    elif "帮助" in state["user_message"]:
        ai_response = "我可以帮你回答问题、编写代码、进行分析等 🤖"
    else:
        ai_response = "有什么我可以帮助你的吗？"
    
    state["ai_response"] = ai_response
    return state

def store_ai_response(state: MessageState) -> MessageState:
    """存储 AI 回复"""
    state["conversation_history"].append({
        "role": "assistant",
        "content": state["ai_response"]
    })
    return state

# 添加节点
graph5.add_node("store_user", store_user_message)
graph5.add_node("generate", generate_response)
graph5.add_node("store_ai", store_ai_response)

# 连接流
graph5.add_edge(START, "store_user")
graph5.add_edge("store_user", "generate")
graph5.add_edge("generate", "store_ai")
graph5.add_edge("store_ai", END)

app5 = graph5.compile()

# 测试对话
messages = ["今天天气如何？", "能帮我吗？", "谢谢"]
state = {"user_message": "", "conversation_history": [], "ai_response": ""}

print("对话过程:")
for msg in messages:
    state = app5.invoke({
        "user_message": msg,
        "conversation_history": state["conversation_history"],
        "ai_response": ""
    })
    print(f"👤 用户: {msg}")
    print(f"🤖 AI: {state['ai_response']}\n")


# ==================== 使用总结 ====================

print("\n" + "="*60)
print("📚 LangGraph 核心概念总结")
print("="*60)

summary = """
1️⃣  State（状态）
   - 定义图中流动的数据结构
   - 使用 TypedDict 定义

2️⃣  Node（节点）
   - 处理函数，接收 state 并返回更新后的 state
   - 使用 graph.add_node() 添加

3️⃣  Edge（边）
   - 连接节点的路径
   - 简单边：graph.add_edge()
   - 条件边：graph.add_conditional_edges()

4️⃣  START 和 END
   - START：图的起点
   - END：图的终点

5️⃣  关键方法
   - graph.compile()：生成可执行的应用
   - app.invoke()：运行图

6️⃣  常见模式
   - 顺序执行：A → B → C → END
   - 条件分支：根据条件选择不同的节点
   - 并行执行：多个节点同时运行
   - 循环：重复执行某个节点
   - 管道：多个图组合
"""

print(summary)
