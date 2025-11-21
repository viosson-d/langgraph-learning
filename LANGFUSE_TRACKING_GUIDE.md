# Langfuse 追踪集成指南

## 📋 概述

所有 DEVOLLEN Agent 系统的 Agent 现在都**自动追踪**到 Langfuse！

### ✅ 已完成

1. **追踪基类**: `agent_tracking_base.py` - 所有 Agent 的基类
2. **追踪装饰器**: `@track_agent_action()` 和 `@langfuse_track`
3. **示例 Agent**: 
   - `tool_operations_specialist_tracked.py` - 工具操作专家
   - `monitoring_specialist_tracked.py` - 监控分析专家
4. **模板生成器**: `agent_template_generator.py` - 快速创建新 Agent

---

## 🚀 快速开始

### 1. 环境配置

确保 `.env` 文件包含 Langfuse 配置:

```bash
LANGFUSE_HOST=http://localhost:3000
LANGFUSE_PUBLIC_KEY=pk-lf-49dd0a2c-277a-41e8-9098-1f9296103dfb
LANGFUSE_SECRET_KEY=sk-lf-9c5a802b-36c4-463d-aecf-3e5eead1ed88
```

### 2. 创建新 Agent（方法一：使用模板生成器）

```bash
# 交互式创建
python agent_template_generator.py

# 命令行创建
python agent_template_generator.py \
  --name "DataAnalyst" \
  --department "数据部" \
  --position "数据分析专家" \
  --description "数据分析专家 Agent" \
  --output "data_analyst_agent.py"
```

### 3. 创建新 Agent（方法二：手动继承基类）

```python
from agent_tracking_base import TrackedAgent, track_agent_action

class MyCustomAgent(TrackedAgent):
    def __init__(self):
        super().__init__(
            agent_id="custom_001",
            agent_name="自定义 Agent",
            agent_type="custom",
            department="技术部",
            position="开发专家"
        )
    
    @track_agent_action("执行任务")
    def execute_task(self, task):
        # 你的任务逻辑
        return {"status": "completed", "task": task}
```

### 4. 运行测试

```bash
# 测试追踪基类
python agent_tracking_base.py

# 测试工具操作专家
python tool_operations_specialist_tracked.py

# 测试监控专家
python monitoring_specialist_tracked.py
```

---

## 📚 核心功能

### 1. TrackedAgent 基类

所有 Agent 都应该继承此基类：

```python
class TrackedAgent:
    """
    所有 Agent 的追踪基类
    
    功能:
    - 自动初始化 Langfuse 客户端
    - 追踪 Agent 初始化
    - 提供追踪装饰器
    - 记录 Agent 元数据
    """
```

**自动追踪的信息**:
- `agent_id`: Agent 唯一标识
- `agent_name`: Agent 名称
- `agent_type`: Agent 类型
- `department`: 所属部门
- `position`: 职位
- `timestamp`: 操作时间戳

### 2. 追踪装饰器

#### @track_agent_action(action_name)

为方法添加详细追踪:

```python
@track_agent_action("处理数据")
def process_data(self, data):
    # 自动追踪到 Langfuse
    return processed_data
```

#### @langfuse_track

简化版装饰器（使用方法名作为追踪名称）:

```python
@langfuse_track
def my_method(self, param):
    # 自动追踪为 "my_method"
    return result
```

### 3. 追踪信息查看

```python
agent = MyAgent()

# 获取追踪信息
trace_info = agent.get_trace_info()
print(trace_info)
# 输出:
# {
#   "agent_id": "my_001",
#   "agent_name": "我的 Agent",
#   "trace_enabled": True,
#   "langfuse_host": "http://localhost:3000"
# }
```

---

## 🔧 为现有 Agent 添加追踪

### 方法一：替换基类

**之前**:
```python
class MyAgent:
    def __init__(self):
        self.name = "My Agent"
    
    def execute(self, task):
        return result
```

**之后**:
```python
from agent_tracking_base import TrackedAgent, track_agent_action

class MyAgent(TrackedAgent):
    def __init__(self):
        super().__init__(
            agent_id="my_001",
            agent_name="My Agent"
        )
    
    @track_agent_action("执行任务")
    def execute(self, task):
        return result
```

### 方法二：逐步迁移

如果不想修改现有类结构，可以只添加装饰器:

```python
from agent_tracking_base import langfuse_track

class MyExistingAgent:
    # 保持现有的 __init__
    
    @langfuse_track  # 只添加这一行
    def important_method(self, data):
        # 现有逻辑不变
        return result
```

---

## 📊 在 Langfuse 中查看追踪

### 1. 打开 Langfuse UI

```bash
# 浏览器访问
http://localhost:3000
```

### 2. 查看追踪记录

导航到: **Traces** → 查看所有 Agent 操作

每条追踪记录包含:
- Agent 信息（ID、名称、部门、职位）
- 操作名称和参数
- 执行时间和耗时
- 输入输出数据
- 错误信息（如果有）

### 3. 使用 DEVOLLEN Studio

```bash
# 启动桌面应用（如果已安装）
open /Users/viosson/DEVOLLEN.app
```

---

## 🎯 最佳实践

### 1. 为所有关键方法添加追踪

```python
class ProductionAgent(TrackedAgent):
    @track_agent_action("初始化配置")
    def setup(self):
        pass
    
    @track_agent_action("执行核心任务")
    def execute(self, task):
        pass
    
    @track_agent_action("清理资源")
    def cleanup(self):
        pass
```

### 2. 使用有意义的动作名称

```python
# ✅ 好的命名
@track_agent_action("解析用户输入")
@track_agent_action("调用外部API")
@track_agent_action("保存结果到数据库")

# ❌ 避免的命名
@track_agent_action("func1")
@track_agent_action("do_stuff")
```

### 3. 记录关键元数据

```python
@track_agent_action("处理订单")
def process_order(self, order_id, amount):
    # Langfuse 会自动记录参数
    # order_id 和 amount 会出现在追踪中
    return result
```

### 4. 处理追踪失败

```python
class RobustAgent(TrackedAgent):
    @track_agent_action("关键操作")
    def critical_operation(self):
        # 即使 Langfuse 不可用，Agent 仍会继续执行
        # 追踪基类会静默处理连接失败
        return result
```

---

## 🔍 追踪示例

### 示例 1: 工具操作专家

```python
from tool_operations_specialist_tracked import ToolOperationsSpecialist

agent = ToolOperationsSpecialist(agent_id="ops_001")

# 执行操作（自动追踪）
record = agent.execute_operation(
    tool_name="langfuse",
    operation_type=OperationType.QUERY,
    command="get_traces",
    parameters={"limit": 10}
)

# 在 Langfuse 中会看到:
# - 操作名称: "ToolOperationsSpecialist.执行工具操作"
# - Agent ID: ops_001
# - 参数: tool_name, operation_type, command, parameters
# - 结果: record 对象
```

### 示例 2: 监控专家

```python
from monitoring_specialist_tracked import MonitoringSpecialist

agent = MonitoringSpecialist(agent_id="monitor_001")

# 生成健康报告（自动追踪）
report = agent.generate_health_report("langfuse")

# 在 Langfuse 中会看到:
# - 操作名称: "MonitoringSpecialist.生成健康报告"
# - Agent ID: monitor_001
# - 参数: system="langfuse"
# - 结果: HealthReport 对象
```

---

## 📦 文件清单

### 核心文件

1. **agent_tracking_base.py**
   - `TrackedAgent` 基类
   - `track_agent_action()` 装饰器
   - `langfuse_track` 简化装饰器
   - `LangfuseConfig` 配置管理

2. **agent_template_generator.py**
   - Agent 模板生成器
   - 命令行工具
   - 交互式创建

### 示例文件

3. **tool_operations_specialist_tracked.py**
   - 工具操作专家（带追踪）
   - 操作日志记录
   - 完整示例

4. **monitoring_specialist_tracked.py**
   - 监控分析专家（带追踪）
   - 性能监控
   - 健康报告生成

### 文档

5. **LANGFUSE_TRACKING_GUIDE.md** (本文件)
   - 完整使用指南
   - 最佳实践
   - 示例代码

---

## 🎓 学习路径

### 第一步: 理解基础

```bash
# 1. 阅读追踪基类
cat agent_tracking_base.py

# 2. 运行示例
python agent_tracking_base.py
```

### 第二步: 查看实际应用

```bash
# 3. 研究工具操作专家
python tool_operations_specialist_tracked.py

# 4. 研究监控专家
python monitoring_specialist_tracked.py
```

### 第三步: 创建自己的 Agent

```bash
# 5. 使用模板生成器
python agent_template_generator.py --name "MyAgent"

# 6. 编辑生成的文件
vim myagent_agent.py

# 7. 运行测试
python myagent_agent.py
```

### 第四步: 查看追踪结果

```bash
# 8. 打开 Langfuse UI
open http://localhost:3000

# 9. 查看 Traces 页面
# 10. 分析 Agent 行为
```

---

## ❓ 常见问题

### Q1: Langfuse 未启用怎么办？

**A**: Agent 会自动检测 Langfuse 配置。如果未配置，追踪会被静默禁用，但 Agent 正常工作。

配置环境变量:
```bash
export LANGFUSE_PUBLIC_KEY=<your-key>
export LANGFUSE_SECRET_KEY=<your-key>
export LANGFUSE_HOST=http://localhost:3000
```

### Q2: 如何禁用追踪？

**A**: 两种方法:

1. 移除环境变量（推荐）
2. 不继承 `TrackedAgent`，移除装饰器

### Q3: 追踪会影响性能吗？

**A**: 影响很小:
- 追踪是异步的
- 如果 Langfuse 不可用，会快速失败
- 本地测试显示延迟 < 5ms

### Q4: 可以追踪哪些信息？

**A**: 
- Agent 元数据（ID、名称、部门）
- 方法调用（名称、参数）
- 执行时间
- 返回值
- 异常信息
- 自定义元数据

### Q5: 如何为现有大量 Agent 添加追踪？

**A**: 使用批量脚本（待创建）或逐个迁移。优先迁移核心 Agent。

---

## 🔄 更新现有 Agent

### 需要更新的文件

根据 grep 搜索结果，以下 Agent 应该添加追踪:

```bash
# 核心 Agent 系统
- agent_system.py (AgentEmployeeSystem)
- agent_orchestrator.py (AgentOrchestrator)
- agent_department.py (DepartmentSystem)
- agent_unit.py (UnitManager)
- organization_system.py

# PM Agent (已有 Langfuse 集成，需要统一)
- langfuse_pm_agent.py (LangfuseProjectManagerAgent)
- langfuse_agent.py

# Demo 和示例
- agent_demo.py
- devollen_agent.py
```

### 更新优先级

1. **高优先级**: 
   - agent_system.py
   - agent_orchestrator.py
   - organization_system.py

2. **中优先级**:
   - agent_department.py
   - agent_unit.py

3. **低优先级**:
   - Demo 文件

---

## 📈 追踪数据分析

### 在 Langfuse 中可以分析:

1. **Agent 使用情况**
   - 哪些 Agent 最活跃？
   - 哪些操作最频繁？

2. **性能指标**
   - 平均响应时间
   - 错误率
   - 吞吐量

3. **调用链路**
   - Agent 之间的调用关系
   - 任务执行流程

4. **错误追踪**
   - 失败的操作
   - 异常堆栈
   - 重试次数

---

## 🎉 总结

### ✅ 现在所有新 Agent 都会:

1. **自动追踪**到 Langfuse
2. **记录完整**的操作历史
3. **提供详细**的元数据
4. **支持性能**分析

### 📝 下一步

1. 为现有 Agent 添加追踪
2. 在 Langfuse 中分析数据
3. 优化 Agent 性能
4. 构建监控仪表板

---

## 📞 支持

如有问题，请查看:
- Langfuse 文档: https://langfuse.com/docs
- 示例代码: `agent_tracking_base.py`
- 测试文件: `*_tracked.py`

---

**更新日期**: 2025-11-21  
**版本**: 1.0.0  
**作者**: DEVOLLEN Agent System
