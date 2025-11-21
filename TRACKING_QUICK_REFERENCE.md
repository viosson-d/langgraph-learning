# 🎯 Langfuse Agent 追踪 - 快速参考卡

## 📌 一句话总结

**所有新 Agent 都继承 `TrackedAgent`，方法加 `@track_agent_action()`，自动追踪到 Langfuse！**

---

## ⚡ 3 分钟快速开始

### 1️⃣ 检查配置（1 分钟）

```bash
# 确保 .env 包含：
cat .env | grep LANGFUSE
# 应该看到：
# LANGFUSE_HOST=http://localhost:3000
# LANGFUSE_PUBLIC_KEY=pk-lf-xxx
# LANGFUSE_SECRET_KEY=sk-lf-xxx
```

### 2️⃣ 创建 Agent（1 分钟）

```bash
# 使用模板生成器
python3 agent_template_generator.py --name "MyAgent"

# 或手动创建
vim my_agent.py
```

### 3️⃣ 编写代码（1 分钟）

```python
from agent_tracking_base import TrackedAgent, track_agent_action

class MyAgent(TrackedAgent):
    def __init__(self):
        super().__init__(
            agent_id="my_001",
            agent_name="我的 Agent"
        )
    
    @track_agent_action("执行任务")
    def execute(self, task):
        return {"result": "done"}
```

### ✅ 完成！

```bash
python3 my_agent.py  # 测试
# 打开 http://localhost:3000 查看追踪
```

---

## 📚 核心 API

### TrackedAgent 基类

```python
class MyAgent(TrackedAgent):
    def __init__(self):
        super().__init__(
            agent_id="唯一ID",        # 必填
            agent_name="Agent名称",   # 必填
            agent_type="类型",        # 可选，默认 "general"
            department="部门",        # 可选
            position="职位"           # 可选
        )
```

### 装饰器

```python
# 方式一：详细追踪
@track_agent_action("动作名称")
def my_method(self, param):
    return result

# 方式二：简化追踪（使用方法名）
from agent_tracking_base import langfuse_track

@langfuse_track
def my_method(self, param):
    return result
```

### 追踪信息

```python
agent = MyAgent()

# 获取追踪状态
info = agent.get_trace_info()
# 返回：
# {
#   "agent_id": "...",
#   "agent_name": "...",
#   "trace_enabled": True/False,
#   "langfuse_host": "http://localhost:3000"
# }
```

---

## 🎨 常用模式

### 模式 1: 基础 Agent

```python
from agent_tracking_base import TrackedAgent, track_agent_action

class SimpleAgent(TrackedAgent):
    def __init__(self):
        super().__init__(
            agent_id="simple_001",
            agent_name="简单 Agent"
        )
    
    @track_agent_action("处理")
    def process(self, data):
        return data
```

### 模式 2: 带配置的 Agent

```python
class ConfigAgent(TrackedAgent):
    def __init__(self, config: dict):
        super().__init__(
            agent_id=config["id"],
            agent_name=config["name"],
            department=config.get("department"),
            position=config.get("position")
        )
        self.config = config
    
    @track_agent_action("初始化")
    def setup(self):
        # 配置初始化
        pass
```

### 模式 3: 多方法 Agent

```python
class MultiAgent(TrackedAgent):
    def __init__(self):
        super().__init__(
            agent_id="multi_001",
            agent_name="多功能 Agent"
        )
    
    @track_agent_action("读取")
    def read(self, source):
        return data
    
    @track_agent_action("处理")
    def process(self, data):
        return processed
    
    @track_agent_action("写入")
    def write(self, data, target):
        return status
```

---

## 🔧 迁移指南

### 从现有 Agent 迁移

#### 之前：
```python
class OldAgent:
    def __init__(self, name):
        self.name = name
    
    def execute(self, task):
        return result
```

#### 之后：
```python
from agent_tracking_base import TrackedAgent, track_agent_action

class OldAgent(TrackedAgent):  # 1. 改基类
    def __init__(self, name):
        super().__init__(        # 2. 调用 super().__init__
            agent_id="old_001",
            agent_name=name
        )
    
    @track_agent_action("执行")  # 3. 添加装饰器
    def execute(self, task):
        return result           # 业务逻辑不变
```

---

## 📊 查看追踪

### 在浏览器中

```bash
# 打开 Langfuse UI
open http://localhost:3000

# 导航：Traces → 查看所有追踪
```

### 使用 DEVOLLEN Studio

```bash
# 启动桌面应用
open /Users/viosson/DEVOLLEN.app
```

### 追踪信息包含

- ✅ Agent ID 和名称
- ✅ 部门和职位
- ✅ 方法名称
- ✅ 输入参数
- ✅ 返回值
- ✅ 执行时间
- ✅ 错误信息（如果有）

---

## 🚨 故障排查

### 问题 1: 追踪未启用

```python
# 检查环境变量
import os
print(os.getenv("LANGFUSE_PUBLIC_KEY"))  # 应该不为空

# 检查 Agent 状态
agent = MyAgent()
print(agent.trace_enabled)  # 应该为 True
```

### 问题 2: Langfuse 连接失败

```bash
# 检查 Docker 服务
docker ps | grep langfuse

# 应该看到：
# viosson-langfuse-1  Up X hours  0.0.0.0:3000->3000/tcp

# 如果没有运行，启动它：
docker start viosson-langfuse-1
```

### 问题 3: 追踪数据看不到

```bash
# 1. 检查 Agent 是否追踪
agent = MyAgent()
print(agent.get_trace_info())

# 2. 检查装饰器
# 确保方法有 @track_agent_action() 或 @langfuse_track

# 3. 刷新 Langfuse UI
# 浏览器中按 Cmd+R 刷新
```

---

## 📁 文件位置

```
/Users/viosson/
├── agent_tracking_base.py              # 追踪基类
├── agent_template_generator.py         # 模板生成器
├── tool_operations_specialist_tracked.py  # 示例 1
├── monitoring_specialist_tracked.py    # 示例 2
├── LANGFUSE_TRACKING_GUIDE.md         # 完整指南
└── AGENT_TRACKING_DEPLOYMENT.md       # 部署文档
```

---

## 🎯 最佳实践

### ✅ 推荐

```python
# 1. 使用有意义的 agent_id
agent_id = "customer_service_001"  # ✅

# 2. 使用描述性的动作名称
@track_agent_action("解析用户输入")  # ✅

# 3. 为所有关键方法添加追踪
@track_agent_action("调用外部API")  # ✅
```

### ❌ 避免

```python
# 1. 不要使用无意义的 ID
agent_id = "agent1"  # ❌

# 2. 不要使用模糊的动作名称
@track_agent_action("do_stuff")  # ❌

# 3. 不要忘记调用 super().__init__
class MyAgent(TrackedAgent):
    def __init__(self):
        # super().__init__(...) 缺失  # ❌
        pass
```

---

## 🔗 快速链接

| 资源 | 位置 |
|------|------|
| 追踪基类 | `agent_tracking_base.py` |
| 模板生成器 | `agent_template_generator.py` |
| 完整指南 | `LANGFUSE_TRACKING_GUIDE.md` |
| 部署文档 | `AGENT_TRACKING_DEPLOYMENT.md` |
| Langfuse UI | http://localhost:3000 |
| DEVOLLEN Studio | `/Users/viosson/DEVOLLEN.app` |
| GitHub 仓库 | https://github.com/viosson-d/langgraph-learning |

---

## 💡 记住这些

1. **所有新 Agent** → 继承 `TrackedAgent`
2. **所有关键方法** → 加 `@track_agent_action()`
3. **测试时** → 检查 `agent.trace_enabled`
4. **查看追踪** → 打开 http://localhost:3000

---

**版本**: 1.0.0  
**最后更新**: 2025-11-21  
**快速生成 Agent**: `python3 agent_template_generator.py`
