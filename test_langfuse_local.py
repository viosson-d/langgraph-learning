"""
本地快速测试 - 不依赖 Docker
如果 Docker 无法连接 Docker Hub，可以用这个脚本测试 Langfuse 集成
"""
from langfuse import Langfuse

# 初始化 Langfuse 客户端（即使服务不运行也可以测试）
langfuse = Langfuse(
    public_key="pk_default",
    secret_key="sk_default",
    host="http://localhost:3000",
    enabled=True,
    debug=False
)

# 测试追踪
with langfuse.trace(name="test_trace", input="Hello") as trace:
    print(f"✅ Trace created: {trace.id}")
    
    # 添加生成
    generation = trace.generation(
        name="test_generation",
        input="input text",
        model="gpt-4",
        usage={"prompt_tokens": 10, "completion_tokens": 20}
    )
    generation.end(output="output text")
    print(f"✅ Generation created: {generation.id}")

print("\n📊 如果看到上面的 trace 和 generation IDs，说明追踪已记录！")
print("请访问 http://localhost:3000 查看（如果 Langfuse 正在运行）")
