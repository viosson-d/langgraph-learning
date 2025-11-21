"""
Tool Operations Specialist Agent (带 Langfuse 追踪)
工具操作专家 Agent - 负责与各种工具交互，记录每次操作
"""

import os
import json
import requests
from datetime import datetime
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
import logging

# 导入追踪基类
from agent_tracking_base import TrackedAgent, track_agent_action, langfuse_track


# ============= Agent 职能定义 =============
class ToolOperationsRole:
    """工具操作专家的职能"""
    
    TITLE = "Tool Operations Specialist"
    TITLE_CN = "工具操作专家"
    
    RESPONSIBILITIES = [
        "执行工具操作命令",
        "记录每次工具交互",
        "处理工具调用错误",
        "维护操作日志",
        "工具状态检查",
        "操作历史追溯"
    ]
    
    SKILLS = [
        "tool_invocation",          # 工具调用
        "interaction_logging",      # 交互日志
        "error_handling",           # 错误处理
        "operation_tracking",       # 操作追踪
        "retry_mechanism",          # 重试机制
        "state_management"          # 状态管理
    ]
    
    SUPPORTED_TOOLS = [
        "langfuse",         # 监控工具
        "github",           # 代码托管
        "slack",            # 沟通工具
        "jira",             # 项目管理
        "database",         # 数据库
        "api_endpoints"     # 各种 API
    ]


# ============= 数据模型 =============
class OperationType(Enum):
    """操作类型"""
    READ = "read"
    WRITE = "write"
    UPDATE = "update"
    DELETE = "delete"
    EXECUTE = "execute"
    QUERY = "query"


class OperationStatus(Enum):
    """操作状态"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"
    RETRYING = "retrying"


@dataclass
class OperationRecord:
    """操作记录"""
    operation_id: str
    tool_name: str
    operation_type: OperationType
    command: str
    parameters: Dict[str, Any]
    status: OperationStatus
    request_payload: Optional[Dict] = None
    response_data: Optional[Dict] = None
    error_message: Optional[str] = None
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    duration_ms: Optional[float] = None
    retry_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "operation_id": self.operation_id,
            "tool_name": self.tool_name,
            "operation_type": self.operation_type.value,
            "command": self.command,
            "parameters": self.parameters,
            "status": self.status.value,
            "request_payload": self.request_payload,
            "response_data": self.response_data,
            "error_message": self.error_message,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_ms": self.duration_ms,
            "retry_count": self.retry_count,
            "metadata": self.metadata
        }


# ============= 操作日志记录器 =============
class OperationLogger:
    """操作日志记录器 - 记录所有工具交互"""
    
    def __init__(self, log_file: str = "tool_operations.jsonl"):
        self.log_file = log_file
        self.logger = logging.getLogger(__name__)
        
    def log_operation(self, record: OperationRecord):
        """记录操作到日志文件"""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                json.dump(record.to_dict(), f, ensure_ascii=False)
                f.write('\n')
        except Exception as e:
            self.logger.error(f"Failed to log operation: {e}")
    
    def get_operations(
        self,
        tool_name: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """获取操作历史"""
        operations = []
        
        try:
            if not os.path.exists(self.log_file):
                return operations
            
            with open(self.log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        op = json.loads(line)
                        if tool_name is None or op.get('tool_name') == tool_name:
                            operations.append(op)
                            if len(operations) >= limit:
                                break
        
        except Exception as e:
            self.logger.error(f"Failed to get operations: {e}")
        
        return operations


# ============= 工具操作专家 Agent (带追踪) =============
class ToolOperationsSpecialist(TrackedAgent):
    """工具操作专家 Agent - 继承 TrackedAgent 自动获得 Langfuse 追踪"""
    
    def __init__(
        self,
        agent_id: str = "tool_ops_001",
        max_retries: int = 3
    ):
        # 初始化追踪基类
        super().__init__(
            agent_id=agent_id,
            agent_name=ToolOperationsRole.TITLE_CN,
            agent_type="operations_specialist",
            department="运维部门",
            position="工具操作专家"
        )
        
        self.role = ToolOperationsRole()
        self.logger = OperationLogger()
        self.max_retries = max_retries
        
        # 工具配置
        self.tool_configs = {
            "langfuse": {
                "base_url": os.getenv("LANGFUSE_HOST", "http://localhost:3000"),
                "public_key": os.getenv("LANGFUSE_PUBLIC_KEY", ""),
                "secret_key": os.getenv("LANGFUSE_SECRET_KEY", "")
            },
            "github": {
                "base_url": "https://api.github.com",
                "token": os.getenv("GITHUB_TOKEN", "")
            }
        }
    
    @track_agent_action("执行工具操作")
    def execute_operation(
        self,
        tool_name: str,
        operation_type: OperationType,
        command: str,
        parameters: Dict[str, Any],
        **kwargs
    ) -> OperationRecord:
        """执行工具操作 - 自动追踪到 Langfuse"""
        
        # 生成操作 ID
        operation_id = f"{tool_name}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        
        # 创建操作记录
        record = OperationRecord(
            operation_id=operation_id,
            tool_name=tool_name,
            operation_type=operation_type,
            command=command,
            parameters=parameters,
            status=OperationStatus.PENDING
        )
        
        # 记录开始时间
        record.start_time = datetime.now()
        record.status = OperationStatus.IN_PROGRESS
        
        retry_count = 0
        last_error = None
        
        while retry_count <= self.max_retries:
            try:
                # 执行具体操作
                if tool_name == "langfuse":
                    result = self._execute_langfuse_operation(command, parameters)
                elif tool_name == "github":
                    result = self._execute_github_operation(command, parameters)
                else:
                    result = self._execute_generic_operation(tool_name, command, parameters)
                
                # 记录成功
                record.status = OperationStatus.SUCCESS
                record.response_data = result
                record.end_time = datetime.now()
                record.duration_ms = (record.end_time - record.start_time).total_seconds() * 1000
                record.retry_count = retry_count
                
                # 写入日志
                self.logger.log_operation(record)
                
                return record
            
            except Exception as e:
                last_error = str(e)
                retry_count += 1
                
                if retry_count <= self.max_retries:
                    record.status = OperationStatus.RETRYING
                else:
                    record.status = OperationStatus.FAILED
                    record.error_message = last_error
                    record.end_time = datetime.now()
                    record.duration_ms = (record.end_time - record.start_time).total_seconds() * 1000
                    record.retry_count = retry_count - 1
                    
                    # 写入失败日志
                    self.logger.log_operation(record)
        
        return record
    
    @langfuse_track
    def _execute_langfuse_operation(
        self,
        command: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """执行 Langfuse 操作"""
        config = self.tool_configs["langfuse"]
        base_url = config["base_url"]
        
        if command == "get_traces":
            # 获取追踪记录
            response = requests.get(
                f"{base_url}/api/public/traces",
                headers={
                    "Authorization": f"Bearer {config['public_key']}:{config['secret_key']}"
                },
                params=parameters
            )
            response.raise_for_status()
            return response.json()
        
        elif command == "create_trace":
            # 创建追踪
            response = requests.post(
                f"{base_url}/api/public/traces",
                headers={
                    "Authorization": f"Bearer {config['public_key']}:{config['secret_key']}"
                },
                json=parameters
            )
            response.raise_for_status()
            return response.json()
        
        else:
            raise ValueError(f"Unknown Langfuse command: {command}")
    
    @langfuse_track
    def _execute_github_operation(
        self,
        command: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """执行 GitHub 操作"""
        config = self.tool_configs["github"]
        base_url = config["base_url"]
        
        headers = {
            "Authorization": f"token {config['token']}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        if command == "get_repo":
            # 获取仓库信息
            owner = parameters.get("owner")
            repo = parameters.get("repo")
            response = requests.get(
                f"{base_url}/repos/{owner}/{repo}",
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        
        elif command == "create_issue":
            # 创建 Issue
            owner = parameters.get("owner")
            repo = parameters.get("repo")
            response = requests.post(
                f"{base_url}/repos/{owner}/{repo}/issues",
                headers=headers,
                json=parameters.get("data", {})
            )
            response.raise_for_status()
            return response.json()
        
        else:
            raise ValueError(f"Unknown GitHub command: {command}")
    
    @langfuse_track
    def _execute_generic_operation(
        self,
        tool_name: str,
        command: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """执行通用工具操作"""
        return {
            "status": "executed",
            "tool": tool_name,
            "command": command,
            "parameters": parameters,
            "timestamp": datetime.now().isoformat()
        }
    
    @track_agent_action("获取操作历史")
    def get_operation_history(
        self,
        tool_name: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """获取操作历史 - 自动追踪"""
        return self.logger.get_operations(tool_name, limit)
    
    @track_agent_action("检查工具状态")
    def check_tool_status(self, tool_name: str) -> Dict[str, Any]:
        """检查工具状态 - 自动追踪"""
        config = self.tool_configs.get(tool_name)
        
        if not config:
            return {
                "tool": tool_name,
                "status": "not_configured",
                "message": f"工具 {tool_name} 未配置"
            }
        
        try:
            if tool_name == "langfuse":
                response = requests.get(f"{config['base_url']}/api/public/health")
                if response.status_code == 200:
                    return {"tool": tool_name, "status": "healthy"}
            
            elif tool_name == "github":
                response = requests.get(
                    f"{config['base_url']}/user",
                    headers={"Authorization": f"token {config['token']}"}
                )
                if response.status_code == 200:
                    return {"tool": tool_name, "status": "healthy", "user": response.json()}
            
            return {"tool": tool_name, "status": "unknown"}
        
        except Exception as e:
            return {
                "tool": tool_name,
                "status": "error",
                "error": str(e)
            }


# ============= 测试 =============
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🔧 工具操作专家 Agent 测试 (带 Langfuse 追踪)")
    print("="*60)
    
    # 创建 Agent
    agent = ToolOperationsSpecialist(agent_id="tool_ops_demo_001")
    
    # 显示 Agent 信息
    print("\n📋 Agent 信息:")
    trace_info = agent.get_trace_info()
    for key, value in trace_info.items():
        print(f"  {key}: {value}")
    
    print(f"\n🎯 职责范围:")
    for resp in agent.role.RESPONSIBILITIES:
        print(f"  • {resp}")
    
    print(f"\n🛠️  支持的工具:")
    for tool in agent.role.SUPPORTED_TOOLS:
        print(f"  • {tool}")
    
    # 测试操作
    print("\n🚀 执行测试操作:")
    
    try:
        # 检查工具状态
        print("\n1️⃣ 检查 Langfuse 状态:")
        status = agent.check_tool_status("langfuse")
        print(f"  状态: {status}")
        
        # 执行 Langfuse 操作
        print("\n2️⃣ 获取 Langfuse 追踪记录:")
        record = agent.execute_operation(
            tool_name="langfuse",
            operation_type=OperationType.QUERY,
            command="get_traces",
            parameters={"limit": 10}
        )
        print(f"  操作状态: {record.status.value}")
        print(f"  操作ID: {record.operation_id}")
        print(f"  耗时: {record.duration_ms:.2f}ms")
        
        # 查看操作历史
        print("\n3️⃣ 查看操作历史:")
        history = agent.get_operation_history(limit=5)
        print(f"  历史记录数: {len(history)}")
        
        if agent.trace_enabled:
            print(f"\n✅ 所有操作已追踪到 Langfuse!")
            print(f"   查看地址: {agent.langfuse_client.base_url if agent.langfuse_client else 'N/A'}")
    
    except Exception as e:
        print(f"\n❌ 错误: {e}")
    
    print("\n" + "="*60 + "\n")
