import autogen
from autogen import AssistantAgent, UserProxyAgent

# 配置 LLM（这里使用 OpenAI GPT-4，需要设置 API 密钥）
config_list = [
    {
        "model": "gpt-4",
        "api_key": "YOUR_OPENAI_API_KEY",  # 请替换为你的 OpenAI API 密钥
    }
]

# 创建助手代理
assistant = AssistantAgent(
    name="assistant",
    llm_config={
        "config_list": config_list,
        "temperature": 0.7,
    },
)

# 创建用户代理（模拟用户输入）
user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="ALWAYS",  # 总是等待用户输入
    code_execution_config=False,  # 不执行代码
)

# 启动对话
user_proxy.initiate_chat(
    assistant,
    message="Hello! How can I help you today?",
)