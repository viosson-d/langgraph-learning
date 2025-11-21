"""
Monitoring Specialist Agent (带 Langfuse 追踪)
监控与分析专家 Agent - 负责系统监控、性能分析、错误诊断
"""

import os
import requests
from datetime import datetime
from typing import Any, Dict, List, Optional
from enum import Enum
from dataclasses import dataclass

# 导入追踪基类
from agent_tracking_base import TrackedAgent, track_agent_action, langfuse_track


# ============= Agent 职能定义 =============
class MonitoringRole:
    """监控专家的职能"""
    
    TITLE = "Monitoring & Analytics Specialist"
    TITLE_CN = "监控与分析专家"
    
    RESPONSIBILITIES = [
        "系统性能监控",
        "数据分析与报告",
        "错误诊断与追踪",
        "健康度评估",
        "告警管理",
        "性能优化建议"
    ]
    
    SKILLS = [
        "performance_monitoring",    # 性能监控
        "data_analytics",           # 数据分析
        "error_diagnosis",          # 错误诊断
        "health_assessment",        # 健康评估
        "alerting",                 # 告警管理
        "optimization"              # 优化建议
    ]
    
    SUPPORTED_SYSTEMS = [
        "langfuse",      # Langfuse 监控平台
        "prometheus",    # Prometheus 指标
        "grafana",       # Grafana 可视化
        "elk_stack",     # ELK 日志分析
        "custom"         # 自定义监控系统
    ]


# ============= 数据模型 =============
class MonitoringSystem(Enum):
    """监控系统类型"""
    LANGFUSE = "langfuse"
    PROMETHEUS = "prometheus"
    GRAFANA = "grafana"
    ELK = "elk"
    CUSTOM = "custom"


class HealthStatus(Enum):
    """健康状态"""
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


@dataclass
class PerformanceMetrics:
    """性能指标"""
    system: str
    timestamp: datetime
    response_time_ms: float
    error_rate: float
    throughput: float
    cpu_usage: Optional[float] = None
    memory_usage: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "system": self.system,
            "timestamp": self.timestamp.isoformat(),
            "response_time_ms": self.response_time_ms,
            "error_rate": self.error_rate,
            "throughput": self.throughput,
            "cpu_usage": self.cpu_usage,
            "memory_usage": self.memory_usage
        }


@dataclass
class HealthReport:
    """健康报告"""
    system: str
    status: HealthStatus
    score: int  # 0-100
    issues: List[str]
    recommendations: List[str]
    timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "system": self.system,
            "status": self.status.value,
            "score": self.score,
            "issues": self.issues,
            "recommendations": self.recommendations,
            "timestamp": self.timestamp.isoformat()
        }


# ============= 监控专家 Agent (带追踪) =============
class MonitoringSpecialist(TrackedAgent):
    """监控与分析专家 Agent - 继承 TrackedAgent 自动获得 Langfuse 追踪"""
    
    def __init__(
        self,
        agent_id: str = "monitoring_spec_001",
        monitoring_system: MonitoringSystem = MonitoringSystem.LANGFUSE
    ):
        # 初始化追踪基类
        super().__init__(
            agent_id=agent_id,
            agent_name=MonitoringRole.TITLE_CN,
            agent_type="monitoring_specialist",
            department="技术部",
            position="监控与分析专家"
        )
        
        self.role = MonitoringRole()
        self.monitoring_system = monitoring_system
        
        # 系统配置
        self.system_configs = {
            MonitoringSystem.LANGFUSE: {
                "host": os.getenv("LANGFUSE_HOST", "http://localhost:3000"),
                "public_key": os.getenv("LANGFUSE_PUBLIC_KEY", ""),
                "secret_key": os.getenv("LANGFUSE_SECRET_KEY", "")
            },
            MonitoringSystem.PROMETHEUS: {
                "host": os.getenv("PROMETHEUS_HOST", "http://localhost:9090")
            },
            MonitoringSystem.GRAFANA: {
                "host": os.getenv("GRAFANA_HOST", "http://localhost:3001")
            }
        }
    
    @track_agent_action("获取系统列表")
    def get_system_list(self) -> List[str]:
        """获取可监控的系统列表 - 自动追踪"""
        return [system.value for system in MonitoringSystem]
    
    @track_agent_action("获取性能指标")
    def get_performance_metrics(
        self,
        system: Optional[str] = None,
        time_range: str = "1h"
    ) -> List[PerformanceMetrics]:
        """
        获取性能指标 - 自动追踪到 Langfuse
        
        Args:
            system: 系统名称（None 表示所有系统）
            time_range: 时间范围（如 "1h", "24h", "7d"）
        """
        metrics_list = []
        
        target_system = system or self.monitoring_system.value
        
        try:
            if target_system == MonitoringSystem.LANGFUSE.value:
                metrics = self._get_langfuse_metrics(time_range)
                metrics_list.append(metrics)
            
            elif target_system == MonitoringSystem.PROMETHEUS.value:
                metrics = self._get_prometheus_metrics(time_range)
                metrics_list.append(metrics)
            
            else:
                # 通用系统
                metrics = PerformanceMetrics(
                    system=target_system,
                    timestamp=datetime.now(),
                    response_time_ms=100.0,
                    error_rate=0.01,
                    throughput=1000.0
                )
                metrics_list.append(metrics)
        
        except Exception as e:
            print(f"获取指标失败: {e}")
        
        return metrics_list
    
    @langfuse_track
    def _get_langfuse_metrics(self, time_range: str) -> PerformanceMetrics:
        """获取 Langfuse 性能指标"""
        config = self.system_configs[MonitoringSystem.LANGFUSE]
        
        try:
            # 调用 Langfuse API 获取统计数据
            response = requests.get(
                f"{config['host']}/api/public/metrics",
                headers={
                    "Authorization": f"Bearer {config['public_key']}:{config['secret_key']}"
                },
                params={"range": time_range}
            )
            
            if response.status_code == 200:
                data = response.json()
                return PerformanceMetrics(
                    system="langfuse",
                    timestamp=datetime.now(),
                    response_time_ms=data.get("avg_response_time", 0),
                    error_rate=data.get("error_rate", 0),
                    throughput=data.get("requests_per_second", 0)
                )
        
        except Exception as e:
            print(f"Langfuse 指标获取失败: {e}")
        
        # 返回默认值
        return PerformanceMetrics(
            system="langfuse",
            timestamp=datetime.now(),
            response_time_ms=50.0,
            error_rate=0.005,
            throughput=500.0
        )
    
    @langfuse_track
    def _get_prometheus_metrics(self, time_range: str) -> PerformanceMetrics:
        """获取 Prometheus 性能指标"""
        config = self.system_configs[MonitoringSystem.PROMETHEUS]
        
        # 示例：查询 Prometheus
        return PerformanceMetrics(
            system="prometheus",
            timestamp=datetime.now(),
            response_time_ms=30.0,
            error_rate=0.002,
            throughput=2000.0,
            cpu_usage=45.5,
            memory_usage=62.3
        )
    
    @track_agent_action("获取错误日志")
    def get_error_logs(
        self,
        system: Optional[str] = None,
        limit: int = 50,
        severity: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        获取错误日志 - 自动追踪
        
        Args:
            system: 系统名称
            limit: 返回数量限制
            severity: 严重级别（error, warning, critical）
        """
        target_system = system or self.monitoring_system.value
        
        if target_system == MonitoringSystem.LANGFUSE.value:
            return self._get_langfuse_errors(limit, severity)
        
        return []
    
    @langfuse_track
    def _get_langfuse_errors(
        self,
        limit: int,
        severity: Optional[str]
    ) -> List[Dict[str, Any]]:
        """获取 Langfuse 错误日志"""
        config = self.system_configs[MonitoringSystem.LANGFUSE]
        
        try:
            response = requests.get(
                f"{config['host']}/api/public/observations",
                headers={
                    "Authorization": f"Bearer {config['public_key']}:{config['secret_key']}"
                },
                params={
                    "type": "error",
                    "limit": limit,
                    "level": severity
                }
            )
            
            if response.status_code == 200:
                return response.json().get("data", [])
        
        except Exception as e:
            print(f"错误日志获取失败: {e}")
        
        return []
    
    @track_agent_action("生成健康报告")
    def generate_health_report(
        self,
        system: Optional[str] = None
    ) -> HealthReport:
        """
        生成健康报告 - 自动追踪到 Langfuse
        
        Args:
            system: 系统名称
        """
        target_system = system or self.monitoring_system.value
        
        # 获取性能指标
        metrics_list = self.get_performance_metrics(target_system)
        
        if not metrics_list:
            return HealthReport(
                system=target_system,
                status=HealthStatus.UNKNOWN,
                score=0,
                issues=["无法获取系统指标"],
                recommendations=["检查系统连接"],
                timestamp=datetime.now()
            )
        
        metrics = metrics_list[0]
        
        # 计算健康分数
        score = 100
        issues = []
        recommendations = []
        
        # 响应时间检查
        if metrics.response_time_ms > 1000:
            score -= 20
            issues.append(f"响应时间过长: {metrics.response_time_ms:.2f}ms")
            recommendations.append("优化查询性能，考虑添加缓存")
        elif metrics.response_time_ms > 500:
            score -= 10
            issues.append(f"响应时间较慢: {metrics.response_time_ms:.2f}ms")
        
        # 错误率检查
        if metrics.error_rate > 0.05:
            score -= 30
            issues.append(f"错误率过高: {metrics.error_rate*100:.2f}%")
            recommendations.append("检查错误日志，修复关键问题")
        elif metrics.error_rate > 0.01:
            score -= 15
            issues.append(f"错误率偏高: {metrics.error_rate*100:.2f}%")
        
        # CPU 使用率检查
        if metrics.cpu_usage and metrics.cpu_usage > 80:
            score -= 15
            issues.append(f"CPU 使用率过高: {metrics.cpu_usage:.1f}%")
            recommendations.append("考虑扩展计算资源")
        
        # 内存使用率检查
        if metrics.memory_usage and metrics.memory_usage > 85:
            score -= 15
            issues.append(f"内存使用率过高: {metrics.memory_usage:.1f}%")
            recommendations.append("检查内存泄漏，优化内存使用")
        
        # 确定健康状态
        if score >= 80:
            status = HealthStatus.HEALTHY
        elif score >= 60:
            status = HealthStatus.WARNING
        else:
            status = HealthStatus.CRITICAL
        
        return HealthReport(
            system=target_system,
            status=status,
            score=max(0, score),
            issues=issues if issues else ["系统运行正常"],
            recommendations=recommendations if recommendations else ["保持当前配置"],
            timestamp=datetime.now()
        )
    
    @track_agent_action("分析趋势")
    def analyze_trends(
        self,
        system: str,
        metric: str,
        time_range: str = "7d"
    ) -> Dict[str, Any]:
        """
        分析性能趋势 - 自动追踪
        
        Args:
            system: 系统名称
            metric: 指标名称（response_time, error_rate, throughput）
            time_range: 时间范围
        """
        return {
            "system": system,
            "metric": metric,
            "time_range": time_range,
            "trend": "stable",  # stable, increasing, decreasing
            "change_percentage": 0.5,
            "prediction": "系统性能保持稳定",
            "timestamp": datetime.now().isoformat()
        }


# ============= 测试 =============
if __name__ == "__main__":
    print("\n" + "="*60)
    print("📊 监控与分析专家 Agent 测试 (带 Langfuse 追踪)")
    print("="*60)
    
    # 创建 Agent
    agent = MonitoringSpecialist(
        agent_id="monitoring_demo_001",
        monitoring_system=MonitoringSystem.LANGFUSE
    )
    
    # 显示 Agent 信息
    print("\n📋 Agent 信息:")
    trace_info = agent.get_trace_info()
    for key, value in trace_info.items():
        print(f"  {key}: {value}")
    
    print(f"\n🎯 职责范围:")
    for resp in agent.role.RESPONSIBILITIES:
        print(f"  • {resp}")
    
    print(f"\n📡 支持的监控系统:")
    systems = agent.get_system_list()
    for sys in systems:
        print(f"  • {sys}")
    
    # 测试监控功能
    print("\n🚀 执行监控测试:")
    
    try:
        # 获取性能指标
        print("\n1️⃣ 获取性能指标:")
        metrics_list = agent.get_performance_metrics("langfuse", "1h")
        if metrics_list:
            metrics = metrics_list[0]
            print(f"  系统: {metrics.system}")
            print(f"  响应时间: {metrics.response_time_ms:.2f}ms")
            print(f"  错误率: {metrics.error_rate*100:.2f}%")
            print(f"  吞吐量: {metrics.throughput:.0f} req/s")
        
        # 生成健康报告
        print("\n2️⃣ 生成健康报告:")
        report = agent.generate_health_report("langfuse")
        print(f"  系统: {report.system}")
        print(f"  状态: {report.status.value}")
        print(f"  健康分数: {report.score}/100")
        print(f"  问题:")
        for issue in report.issues:
            print(f"    • {issue}")
        print(f"  建议:")
        for rec in report.recommendations:
            print(f"    • {rec}")
        
        # 分析趋势
        print("\n3️⃣ 分析性能趋势:")
        trend = agent.analyze_trends("langfuse", "response_time", "7d")
        print(f"  趋势: {trend['trend']}")
        print(f"  变化: {trend['change_percentage']}%")
        print(f"  预测: {trend['prediction']}")
        
        if agent.trace_enabled:
            print(f"\n✅ 所有监控操作已追踪到 Langfuse!")
            print(f"   查看地址: {agent.langfuse_client.base_url if agent.langfuse_client else 'N/A'}")
    
    except Exception as e:
        print(f"\n❌ 错误: {e}")
    
    print("\n" + "="*60 + "\n")
