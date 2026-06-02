import os
from dotenv import load_dotenv

_ = load_dotenv()

# 从环境变量中获取API密钥和URL

# 1. Deepseek API
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = os.getenv("DEEPSEEK_BASE_URL")


# 2. Dashscope API
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
DASHSCOPE_API_URL = os.getenv("DASHSCOPE_API_URL")

# 3. Bigmodel API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = os.getenv("OPENAI_API_URL")

# 4. AI Hub API
AI_HUB_API_KEY = os.getenv("AI_HUB_API_KEY")
AI_HUB_API_URL = os.getenv("AI_HUB_BASE_URL")
