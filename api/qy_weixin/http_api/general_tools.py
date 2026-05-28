"""
通用工具函数
    - 获取当前时间戳 timestamp
    - 获取当前日期 get_current_date
    - 获取时间的秒数 get_second
    - 获取时间的分钟数 get_minute
"""
import time
from datetime import datetime,date
from zoneinfo import ZoneInfo

def timestamp():
    """
    获取当前时间戳
    Returns:
        int: 当前时间戳，单位为秒
    """
    return int(time.time())

def get_current_date():
    """
    获取当前日期
    Returns:
        str: 当前日期，格式为YYYY-MM-DD
    """
    return date.today().strftime("%Y-%m-%d")

def get_second(time_minute:str):
    """
    获取时间的秒数
    Args:
        time_minute (str): 时间字符串.
            - 格式为YYYY-MM-DD HH:MM
    Returns:
        int: 秒级时间戳
    """
    try:
        dt = datetime.strptime(time_minute, "%Y-%m-%d %H:%M")
        dt = dt.replace(tzinfo=ZoneInfo("Asia/Shanghai"))
        return int(dt.timestamp())
    except ValueError:
        print(f"时间字符串 {time_minute} 格式错误")
        return None
    except TypeError:
        print(f"时间字符串 {time_minute} 类型错误")
        return None
    
def get_minute(second:int):
    """
    获取时间的分钟数
    Args:
        second (int): 秒级时间戳
    Returns:
        str: 分钟级时间字符串，格式为YYYY-MM-DD HH:MM
    """
    try:
        dt = datetime.fromtimestamp(second, tz=ZoneInfo("Asia/Shanghai"))
        return dt.strftime("%Y-%m-%d %H:%M")
    except ValueError:
        print(f"时间戳 {second} 格式错误")
        return None
    except TypeError:
        print(f"时间戳 {second} 类型错误")
        return None

if __name__ == "__main__":
    s = "2026-03-25 20:00"
    print(get_second(s))


