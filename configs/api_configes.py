import os
import dotenv

dotenv.load_dotenv()
yaoud_envs = {
    "url": os.getenv("YAOUD_URL"),
    "public_key": os.getenv("YAOUD_PUBLIC_KEY"),
    "timeout": 20,
}


deming_env = {
    "url": os.getenv("DEMING_URL"),
    "public_key": os.getenv("DEMING_PUBLIC_KEY"),
    "timeout": 20,
}


yaoud_env = yaoud_envs



if __name__ == "__main__":
    print(yaoud_env)
