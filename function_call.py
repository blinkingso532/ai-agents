"""Function Calling示例，展示如何使用工具函数来增强LLM的能力。"""

from openai import OpenAI
from load_env import DEEPSEEK_API_KEY, DEEPSEEK_API_URL
import json

# 初始化LLM实例
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_API_URL,
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "获取当前天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市名称，例如：北京",
                    }
                },
                "required": ["location"],
            },
        },
    }
]

USER_INPUT = "请告诉我北京现在的天气如何？"
messages = [{"role": "user", "content": USER_INPUT}]


def chat(message: str) -> str:
    """与LLM进行对话，返回模型回复"""
    messages.append({"role": "user", "content": message})
    return client.chat.completions.create(
        model="deepseek-v4-flash",
        tools=tools,
        tool_choice="auto",
        messages=messages,
        extra_body={"thinking": {"type": "disabled"}},
    )


completion = chat(USER_INPUT)


def get_weather(location: str) -> str:
    """通过指定城市或地区名称获取该地区的天气状况
    Args:
        location (str): 城市或地区名称，例如：北京
    Returns:
        str: 包含天气信息的字符串，例如："北京现在是晴天，温度25摄氏度。"
    """
    return f"{location}现在是晴天，温度25摄氏度。"


# 处理函数调用
ai_message = completion.choices[0].message
if ai_message.tool_calls:
    for tool_call in ai_message.tool_calls:
        if tool_call.function.name == "get_current_weather":
            # 模拟调用函数获取天气信息
            arguments = json.loads(tool_call.function.arguments)
            weather_info = get_weather(arguments["location"])
            print(weather_info)
            # 处理天气信息，并添加到消息列表中，发送给模型获取最终回复
            messages.append({"role": "assistant", "content": weather_info})
            final_reply = chat(weather_info)
            print(final_reply.choices[0].message.content)
        else:
            print(f"未知的工具调用: {tool_call.function.name}")
else:
    print(ai_message.content)
