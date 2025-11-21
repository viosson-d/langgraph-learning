"""
Agent 追踪模板生成器
用于快速创建带 Langfuse 追踪的新 Agent

使用方法:
python agent_template_generator.py --name "MyAgent" --department "技术部" --position "开发专家"
"""

import os
import argparse
from typing import Optional


AGENT_TEMPLATE = '''"""
{agent_name} Agent (带 Langfuse 追踪)
{description}
"""

import os
from datetime import datetime
from typing import Any, Dict, List, Optional

# 导入追踪基类
from agent_tracking_base import TrackedAgent, track_agent_action, langfuse_track


# ============= Agent 职能定义 =============
class {class_name}Role:
    """Agent 职能定义"""
    
    TITLE = "{agent_title}"
    TITLE_CN = "{agent_title_cn}"
    
    RESPONSIBILITIES = [
        "{responsibility_1}",
        "{responsibility_2}",
        "{responsibility_3}"
    ]
    
    SKILLS = [
        "{skill_1}",
        "{skill_2}",
        "{skill_3}"
    ]


# ============= {class_name} Agent (带追踪) =============
class {class_name}(TrackedAgent):
    """{agent_title_cn} - 继承 TrackedAgent 自动获得 Langfuse 追踪"""
    
    def __init__(
        self,
        agent_id: str = "{default_agent_id}",
        **kwargs
    ):
        # 初始化追踪基类
        super().__init__(
            agent_id=agent_id,
            agent_name="{agent_title_cn}",
            agent_type="{agent_type}",
            department="{department}",
            position="{position}",
            **kwargs
        )
        
        self.role = {class_name}Role()
        
        # 添加你的初始化代码
        self.config = {{
            # Agent 配置
        }}
    
    @track_agent_action("执行主要任务")
    def execute(self, task: str, **kwargs) -> Dict[str, Any]:
        """
        执行主要任务 - 自动追踪到 Langfuse
        
        Args:
            task: 任务描述
            **kwargs: 其他参数
        
        Returns:
            执行结果
        """
        # 实现你的任务逻辑
        result = {{
            "status": "completed",
            "task": task,
            "timestamp": datetime.now().isoformat()
        }}
        
        return result
    
    @track_agent_action("处理数据")
    def process_data(self, data: Any) -> Any:
        """
        处理数据 - 自动追踪
        
        Args:
            data: 输入数据
        
        Returns:
            处理后的数据
        """
        # 实现数据处理逻辑
        processed = data  # 替换为实际逻辑
        
        return processed
    
    @langfuse_track
    def analyze(self, input_data: Dict) -> Dict[str, Any]:
        """
        分析数据 - 使用简化装饰器追踪
        
        Args:
            input_data: 输入数据
        
        Returns:
            分析结果
        """
        # 实现分析逻辑
        analysis = {{
            "input": input_data,
            "result": "analysis_result",
            "timestamp": datetime.now().isoformat()
        }}
        
        return analysis


# ============= 测试 =============
if __name__ == "__main__":
    print("\\n" + "="*60)
    print("🤖 {agent_title_cn} 测试 (带 Langfuse 追踪)")
    print("="*60)
    
    # 创建 Agent
    agent = {class_name}(agent_id="{test_agent_id}")
    
    # 显示 Agent 信息
    print("\\n📋 Agent 信息:")
    trace_info = agent.get_trace_info()
    for key, value in trace_info.items():
        print(f"  {{key}}: {{value}}")
    
    print(f"\\n🎯 职责范围:")
    for resp in agent.role.RESPONSIBILITIES:
        print(f"  • {{resp}}")
    
    print(f"\\n💡 技能:")
    for skill in agent.role.SKILLS:
        print(f"  • {{skill}}")
    
    # 测试功能
    print("\\n🚀 执行测试:")
    
    try:
        # 执行任务
        print("\\n1️⃣ 执行任务:")
        result = agent.execute("测试任务")
        print(f"  结果: {{result}}")
        
        # 处理数据
        print("\\n2️⃣ 处理数据:")
        processed = agent.process_data({{"test": "data"}})
        print(f"  处理结果: {{processed}}")
        
        # 分析数据
        print("\\n3️⃣ 分析数据:")
        analysis = agent.analyze({{"input": "test"}})
        print(f"  分析结果: {{analysis}}")
        
        if agent.trace_enabled:
            print(f"\\n✅ 所有操作已追踪到 Langfuse!")
            print(f"   查看地址: {{agent.langfuse_client.base_url if agent.langfuse_client else 'N/A'}}")
        else:
            print(f"\\n⚠️  Langfuse 未启用，请配置环境变量")
    
    except Exception as e:
        print(f"\\n❌ 错误: {{e}}")
    
    print("\\n" + "="*60 + "\\n")
'''


def generate_agent(
    name: str,
    department: str = "技术部",
    position: str = "专家",
    description: Optional[str] = None,
    output_file: Optional[str] = None
) -> str:
    """
    生成 Agent 代码
    
    Args:
        name: Agent 名称（如 "DataAnalyst"）
        department: 部门
        position: 职位
        description: 描述
        output_file: 输出文件路径
    
    Returns:
        生成的代码
    """
    # 生成默认值
    class_name = name.replace(" ", "").replace("_", "")
    agent_title = name.replace("_", " ").title()
    agent_title_cn = description or f"{name} Agent"
    agent_type = name.lower().replace(" ", "_")
    default_agent_id = f"{agent_type}_001"
    test_agent_id = f"{agent_type}_test_001"
    
    # 填充模板
    code = AGENT_TEMPLATE.format(
        agent_name=agent_title,
        class_name=class_name,
        agent_title=agent_title,
        agent_title_cn=agent_title_cn,
        description=description or f"{agent_title_cn} - 自动生成的 Agent",
        agent_type=agent_type,
        department=department,
        position=position,
        default_agent_id=default_agent_id,
        test_agent_id=test_agent_id,
        responsibility_1="执行核心任务",
        responsibility_2="处理相关数据",
        responsibility_3="提供专业分析",
        skill_1="task_execution",
        skill_2="data_processing",
        skill_3="analysis"
    )
    
    # 保存到文件
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(code)
        print(f"✅ Agent 代码已生成: {output_file}")
    
    return code


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description="生成带 Langfuse 追踪的 Agent")
    parser.add_argument("--name", required=True, help="Agent 名称（如 DataAnalyst）")
    parser.add_argument("--department", default="技术部", help="所属部门")
    parser.add_argument("--position", default="专家", help="职位")
    parser.add_argument("--description", help="Agent 描述")
    parser.add_argument("--output", help="输出文件路径")
    
    args = parser.parse_args()
    
    # 生成输出文件名
    output_file = args.output
    if not output_file:
        output_file = f"{args.name.lower()}_agent.py"
    
    # 生成代码
    print("\n" + "="*60)
    print("🏭 Agent 追踪模板生成器")
    print("="*60)
    print(f"\nAgent 名称: {args.name}")
    print(f"部门: {args.department}")
    print(f"职位: {args.position}")
    print(f"输出文件: {output_file}")
    print("\n生成中...")
    
    code = generate_agent(
        name=args.name,
        department=args.department,
        position=args.position,
        description=args.description,
        output_file=output_file
    )
    
    print("\n" + "="*60)
    print("📚 使用说明:")
    print("="*60)
    print(f"""
1. 编辑生成的文件: {output_file}
2. 根据需求修改职责、技能和方法
3. 实现具体的业务逻辑
4. 运行测试: python {output_file}

所有方法都已自动添加 Langfuse 追踪！
    """)
    print("="*60 + "\n")


# ============= 快速创建函数 =============
def create_quick_agent(name: str, **kwargs) -> str:
    """
    快速创建 Agent（Python API）
    
    使用示例:
    >>> code = create_quick_agent("DataAnalyst", department="数据部")
    >>> exec(code)  # 直接执行
    
    或:
    >>> create_quick_agent("DataAnalyst", output_file="data_analyst.py")
    """
    return generate_agent(name, **kwargs)


if __name__ == "__main__":
    # 如果直接运行，提供交互式创建
    import sys
    
    if len(sys.argv) == 1:
        print("\n" + "="*60)
        print("🏭 Agent 追踪模板生成器 - 交互模式")
        print("="*60)
        
        name = input("\nAgent 名称 (如 DataAnalyst): ").strip()
        if not name:
            print("❌ Agent 名称不能为空")
            sys.exit(1)
        
        department = input("部门 (默认: 技术部): ").strip() or "技术部"
        position = input("职位 (默认: 专家): ").strip() or "专家"
        description = input("描述 (可选): ").strip() or None
        output_file = input(f"输出文件 (默认: {name.lower()}_agent.py): ").strip() or f"{name.lower()}_agent.py"
        
        print("\n生成中...")
        generate_agent(
            name=name,
            department=department,
            position=position,
            description=description,
            output_file=output_file
        )
        
        print(f"\n✅ 完成！文件已保存: {output_file}")
        print(f"运行测试: python {output_file}\n")
    else:
        main()
