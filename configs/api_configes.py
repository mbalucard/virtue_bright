import os
import dotenv

dotenv.load_dotenv()
yaoud_envs = {
    "url": os.getenv("YAOUD_URL"),
    "public_key": os.getenv("YAOUD_PUBLIC_KEY"),
    "timeout": 20,
}


deming_uat_env = {
    "url": os.getenv("DEMING_UAT_URL"),
    "public_key": os.getenv("DEMING_PUBLIC_KEY"),
    "timeout": 20,
}

deming_env = {
    "url": os.getenv("DEMING_URL"),
    "public_key": os.getenv("DEMING_PUBLIC_KEY"),
    "timeout": 20,
}

qy_env = {
    "base_url": os.getenv("QYAPI_BASE_URL"),
    "corp_id": os.getenv("QYAPI_CORP_ID"),
    "secret": os.getenv("QYAPI_SECRET"),
    "enterprise_id": os.getenv("QYAPI_ENTERPRISE_ID"),
    "agent_id": os.getenv("QYAPI_AGENT_ID"),
    "ttl": int(os.getenv("QYAPI_TTL")),
}

yaoud_env = deming_env


if __name__ == "__main__":
    print(qy_env)
