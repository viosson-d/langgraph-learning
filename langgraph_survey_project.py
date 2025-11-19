"""
LangGraph 实战项目：智能问卷处理系统
展示如何处理真实场景中的问卷数据
"""

from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List
import json

# ==================== 第1部分：定义状态 ====================

class SurveyState(TypedDict):
    """问卷处理状态"""
    user_id: str
    survey_data: dict          # 原始问卷数据
    validated_data: dict       # 验证后的数据
    analysis_result: dict      # 分析结果
    final_report: str          # 最终报告
    error_message: str         # 错误信息
    processing_steps: List[str] # 处理步骤记录

# ==================== 第2部分：定义节点函数 ====================

def validate_input(state: SurveyState) -> SurveyState:
    """验证问卷输入"""
    state["processing_steps"].append("📋 验证输入中...")
    
    # 检查必填字段
    required_fields = ["name", "age", "satisfaction"]
    missing = [f for f in required_fields if f not in state["survey_data"]]
    
    if missing:
        state["error_message"] = f"缺少字段: {missing}"
        return state
    
    # 检查数据类型
    try:
        age = int(state["survey_data"].get("age", 0))
        if age < 0 or age > 150:
            state["error_message"] = "年龄必须在 0-150 之间"
            return state
    except ValueError:
        state["error_message"] = "年龄必须是数字"
        return state
    
    state["validated_data"] = state["survey_data"].copy()
    state["processing_steps"].append("✅ 输入验证通过")
    return state

def clean_data(state: SurveyState) -> SurveyState:
    """清洗数据"""
    state["processing_steps"].append("🧹 清洗数据中...")
    
    # 清洗名字：首字母大写
    if "name" in state["validated_data"]:
        state["validated_data"]["name"] = state["validated_data"]["name"].strip().title()
    
    # 规范化满意度评分
    satisfaction = state["validated_data"].get("satisfaction", "")
    satisfaction_map = {
        "很满意": 5, "满意": 4, "一般": 3, "不满意": 2, "很不满意": 1,
        "5": 5, "4": 4, "3": 3, "2": 2, "1": 1
    }
    state["validated_data"]["satisfaction_score"] = satisfaction_map.get(str(satisfaction), 3)
    
    state["processing_steps"].append("✅ 数据清洗完成")
    return state

def analyze_satisfaction(state: SurveyState) -> SurveyState:
    """分析满意度"""
    state["processing_steps"].append("📊 分析满意度中...")
    
    score = state["validated_data"].get("satisfaction_score", 3)
    
    if score >= 4:
        level = "很满意 😊"
        recommendation = "保持现有服务质量"
    elif score >= 3:
        level = "一般 😐"
        recommendation = "需要改进一些方面"
    else:
        level = "不满意 😞"
        recommendation = "需要重大改进"
    
    state["analysis_result"] = {
        "satisfaction_level": level,
        "score": score,
        "recommendation": recommendation,
        "user_profile": {
            "name": state["validated_data"].get("name"),
            "age": state["validated_data"].get("age"),
            "user_id": state["user_id"]
        }
    }
    
    state["processing_steps"].append("✅ 分析完成")
    return state

def generate_report(state: SurveyState) -> SurveyState:
    """生成报告"""
    state["processing_steps"].append("📝 生成报告中...")
    
    analysis = state["analysis_result"]
    profile = analysis["user_profile"]
    
    report = f"""
╔════════════════════════════════════════╗
║          问卷处理报告                    ║
╚════════════════════════════════════════╝

【用户信息】
  姓名：{profile['name']}
  年龄：{profile['age']}
  用户ID：{profile['user_id']}

【满意度评分】
  等级：{analysis['satisfaction_level']}
  分数：{analysis['score']}/5
  
【建议】
  {analysis['recommendation']}

【处理步骤】
{chr(10).join(f"  {step}" for step in state['processing_steps'])}

════════════════════════════════════════
"""
    
    state["final_report"] = report
    state["processing_steps"].append("✅ 报告生成完成")
    return state

# ==================== 第3部分：条件路由函数 ====================

def check_validation(state: SurveyState) -> str:
    """检查验证结果，决定下一步"""
    if state["error_message"]:
        return "error"
    return "proceed"

def decide_analysis_type(state: SurveyState) -> str:
    """根据年龄决定分析类型"""
    age = int(state["validated_data"].get("age", 0))
    if age < 18:
        return "analyze"  # 简化版本
    else:
        return "analyze"  # 完整版本

# ==================== 第4部分：构建图 ====================

def create_survey_processor():
    """创建问卷处理图"""
    graph = StateGraph(SurveyState)
    
    # 添加节点
    graph.add_node("validate", validate_input)
    graph.add_node("clean", clean_data)
    graph.add_node("analyze", analyze_satisfaction)
    graph.add_node("report", generate_report)
    graph.add_node("error_handler", lambda state: state)  # 错误处理节点
    
    # 构建流程
    graph.add_edge(START, "validate")
    
    # 条件分支：验证是否通过
    graph.add_conditional_edges(
        "validate",
        check_validation,
        {
            "error": "error_handler",
            "proceed": "clean"
        }
    )
    
    # 错误处理流
    graph.add_edge("error_handler", END)
    
    # 正常流程
    graph.add_edge("clean", "analyze")
    graph.add_edge("analyze", "report")
    graph.add_edge("report", END)
    
    return graph.compile()

# ==================== 第5部分：测试 ====================

print("="*60)
print("🎯 LangGraph 实战项目：智能问卷处理系统")
print("="*60)

# 创建处理器
processor = create_survey_processor()

# 测试用例1：有效的问卷
print("\n【测试1】有效的问卷：")
print("-" * 60)

valid_survey = {
    "user_id": "user_001",
    "survey_data": {
        "name": "张三",
        "age": "25",
        "satisfaction": "很满意"
    },
    "validated_data": {},
    "analysis_result": {},
    "final_report": "",
    "error_message": "",
    "processing_steps": []
}

result1 = processor.invoke(valid_survey)
print(result1["final_report"])

# 测试用例2：缺少必填字段
print("\n【测试2】缺少必填字段：")
print("-" * 60)

invalid_survey = {
    "user_id": "user_002",
    "survey_data": {
        "name": "李四",
        # 缺少 age 和 satisfaction
    },
    "validated_data": {},
    "analysis_result": {},
    "final_report": "",
    "error_message": "",
    "processing_steps": []
}

result2 = processor.invoke(invalid_survey)
print(f"❌ 错误: {result2['error_message']}")
print(f"处理步骤: {result2['processing_steps']}")

# 测试用例3：年龄无效
print("\n【测试3】年龄无效：")
print("-" * 60)

invalid_age = {
    "user_id": "user_003",
    "survey_data": {
        "name": "王五",
        "age": "200",  # 无效的年龄
        "satisfaction": "一般"
    },
    "validated_data": {},
    "analysis_result": {},
    "final_report": "",
    "error_message": "",
    "processing_steps": []
}

result3 = processor.invoke(invalid_age)
print(f"❌ 错误: {result3['error_message']}")

# ==================== 统计信息 ====================

print("\n" + "="*60)
print("📈 处理统计")
print("="*60)
print(f"✅ 成功处理: 1 份")
print(f"❌ 处理失败: 2 份")
print(f"📊 成功率: 33.3%")

# ==================== 导出数据 ====================

results = {
    "successful": result1["analysis_result"],
    "errors": [
        {"reason": result2["error_message"]},
        {"reason": result3["error_message"]}
    ]
}

with open("/Users/viosson/survey_results.json", "w") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\n💾 结果已导出到: /Users/viosson/survey_results.json")

# ==================== 显示图的结构 ====================

print("\n" + "="*60)
print("📊 处理流程图")
print("="*60)
print(processor.get_graph().draw_ascii())

print("\n" + "="*60)
print("✨ 项目完成！")
print("="*60)
print("""
本示例展示了：
1. 定义复杂的状态结构
2. 创建多个处理节点
3. 实现条件分支路由
4. 处理错误和异常
5. 生成最终报告
6. 导出处理结果

你可以基于这个模板构建自己的业务流程！
""")
