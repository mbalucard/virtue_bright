import os
import dotenv

dotenv.load_dotenv()
yaoud_env = {
    "url":os.getenv("YAOUD_URL"),
    "public_key":os.getenv("YAOUD_PUBLIC_KEY"),
    "timeout":20,
}

if __name__ == "__main__":
    print(yaoud_env)