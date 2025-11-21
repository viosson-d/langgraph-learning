"""
Langfuse 追踪基类
所有 Agent 都应继承此基类以自动获得 Langfuse 追踪能力
"""

import os
from functools import wraps
from typing import Any, Dict, Optional, Callable
from datetime import datetime
from langfuse import Langfuse
from langfuse.decorators import observe


# ============= Langfuse 配置 =============
class LangfuseConfig:
    """Langfuse 配置管理"""
    
    HOST = os.getenv("LANGFUSE_HOST", "http://localhost:3000")
    PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY", "")
    SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY", "")
    
    @classmethod
    def is_enabled(cls) -> bool:
        """检查 Langfuse 是否启用"""
        return bool(cls.PUBLIC_KEY and cls.SECRET_KEY)
    
    @classmethod
    def get_client(cls) -> Optional[Langfuse]:
        """获取 Langfuse 客户端"""
        if not cls.is_enabled():
            return None
        
        return Langfuse(
            public_key=cls.PUBLIC_KEY,
            secret_key=cls.SECRET_KEY,
            host=cls.HOST
        )


# ============= 追踪装饰器 =============
def track_agent_action(action_name: Optional[str] = None):
    """
    追踪 Agent 动作的装饰器
    
    使用方法:
    @track_agent_action("process_task")
    def execute_task(self, task):
        return result
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # 如果 Langfuse 未启用，直接执行原函数
            if not LangfuseConfig.is_enabled():
                return func(self, *args, **kwargs)
            
            # 获取 agent 信息
            agent_name = getattr(self, 'agent_name', self.__class__.__name__)
            agent_id = getattr(self, 'agent_id', 'unknown')
            
            # 使用 Langfuse observe 装饰器
            name = action_name or func.__name__
            
            @observe(name=f"{agent_name}.{name}")
            def traced_func():
                return func(self, *args, **kwargs)
            
            return traced_func()
        
        return wrapper
    return decorator


# ============= Agent 追踪基类 =============
class TrackedAgent:
    """
    所有 Agent 的追踪基类
    
    所有新创建的 Agent 都应该继承此类，自动获得 Langfuse 追踪能力。
    
    使用示例:
    
    class MyAgent(TrackedAgent):
        def __init__(self):
            super().__init__(
                agent_id="my_agent_001",
                agent_name="我的智能助手",
                agent_type="assistant"
            )
        
        @track_agent_action("执行任务")
        def execute_task(self, task):
            # 任务逻辑
            return result
    """
    
    def __init__(
        self,
        agent_id: str,
        agent_name: str,
        agent_type: str = "general",
        department: Optional[str] = None,
        position: Optional[str] = None,
        **kwargs
    ):
        """
        初始化追踪 Agent
        
        Args:
            agent_id: Agent 唯一标识
            agent_name: Agent 名称
            agent_type: Agent 类型
            department: 所属部门
            position: 职位
        """
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.agent_type = agent_type
        self.department = department
        self.position = position
        
        # Langfuse 客户端
        self.langfuse_client = LangfuseConfig.get_client()
        
        # 追踪信息
        self.trace_enabled = LangfuseConfig.is_enabled()
        
        # 记录 Agent 初始化
        if self.trace_enabled:
            self._trace_initialization()
    
    def _trace_initialization(self):
        """追踪 Agent 初始化"""
        if not self.langfuse_client:
            return
        
        try:
            self.langfuse_client.trace(
                name=f"{self.agent_name}.initialized"
            )
        except Exception as e:
            # 静默处理追踪错误
            pass
    
    @observe(name="agent_execute")
    def execute(self, *args, **kwargs) -> Any:
        """
        通用执行方法（子类应重写此方法）
        自动追踪所有执行
        """
        raise NotImplementedError("子类必须实现 execute 方法")
    
    def get_trace_info(self) -> Dict[str, Any]:
        """获取追踪信息"""
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "agent_type": self.agent_type,
            "department": self.department,
            "position": self.position,
            "trace_enabled": self.trace_enabled,
            "langfuse_host": LangfuseConfig.HOST if self.trace_enabled else None
        }


# ============= 快速装饰器（简化版）=============
def langfuse_track(func: Callable) -> Callable:
    """
    简化的追踪装饰器，自动使用函数名
    
    使用方法:
    @langfuse_track
    def my_function(self, param):
        return result
    """
    return track_agent_action(func.__name__)(func)


# ============= 示例 Agent =============
class ExampleTrackedAgent(TrackedAgent):
    """示例：带追踪的 Agent"""
    
    def __init__(self):
        super().__init__(
            agent_id="example_001",
            agent_name="示例 Agent",
            agent_type="example",
            department="技术部",
            position="开发专家"
        )
    
    @track_agent_action("处理任务")
    def execute(self, task: str) -> str:
        """执行任务"""
        result = f"处理完成: {task}"
        return result
    
    @track_agent_action("分析数据")
    def analyze(self, data: Dict) -> Dict:
        """分析数据"""
        return {
            "status": "analyzed",
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
    
    @langfuse_track
    def simple_action(self, param: str) -> str:
        """使用简化装饰器的动作"""
        return f"Processed: {param}"


# ============= 测试 =============
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🔍 Langfuse 追踪基类测试")
    print("="*60)
    
    # 检查配置
    print(f"\n📊 Langfuse 状态:")
    print(f"  Host: {LangfuseConfig.HOST}")
    print(f"  启用状态: {LangfuseConfig.is_enabled()}")
    
    # 创建示例 Agent
    print("\n🤖 创建示例 Agent:")
    agent = ExampleTrackedAgent()
    
    # 获取追踪信息
    trace_info = agent.get_trace_info()
    print(f"\n📋 Agent 信息:")
    for key, value in trace_info.items():
        print(f"  {key}: {value}")
    
    # 执行追踪动作
    print("\n🚀 执行追踪动作:")
    
    try:
        result1 = agent.execute("测试任务")
        print(f"  ✅ execute: {result1}")
        
        result2 = agent.analyze({"test": "data"})
        print(f"  ✅ analyze: {result2}")
        
        result3 = agent.simple_action("test")
        print(f"  ✅ simple_action: {result3}")
        
        if agent.trace_enabled:
            print(f"\n✅ 所有动作已追踪到 Langfuse: {LangfuseConfig.HOST}")
        else:
            print(f"\n⚠️  Langfuse 未启用，请配置环境变量:")
            print(f"  export LANGFUSE_PUBLIC_KEY=<your-key>")
            print(f"  export LANGFUSE_SECRET_KEY=<your-key>")
    
    except Exception as e:
        print(f"\n❌ 错误: {e}")
    
    print("\n" + "="*60)
    print("📚 使用指南:")
    print("="*60)
    print("""
1. 继承 TrackedAgent 基类:
   class MyAgent(TrackedAgent):
       def __init__(self):
           super().__init__(
               agent_id="my_001",
               agent_name="我的 Agent"
           )

2. 使用装饰器追踪方法:
   @track_agent_action("动作名称")
   def my_method(self):
       return result

3. 或使用简化装饰器:
   @langfuse_track
   def my_method(self):
       return result

所有动作自动追踪到 Langfuse！
    """)
    print("="*60 + "\n")
