"""
通用工具函数
    - 获取当前时间戳 timestamp
    - 获取当前日期 get_current_date
    - 获取指定日期的开始和结束时间 get_date_start_and_end_time
    - 获取过去的日期 retrieve_past_date
    - 将时间字符串转为秒级时间戳 get_second
"""
import time
from datetime import datetime, date, time as dt_time, timedelta
from zoneinfo import ZoneInfo


def timestamp(is_second: bool = False):
    """
    获取当前时间戳
    Args:
        is_second (bool): 是否返回秒级时间戳. Defaults to False（毫秒）.
    Returns:
        int: 当前时间戳，默认毫秒；is_second=True 时为秒
    """
    if is_second:
        return int(time.time())
    return time.time_ns() // 1000000


def get_current_date():
    """
    获取当前日期
    Returns:
        str: 当前日期，格式为YYYY-MM-DD
    """
    return date.today().strftime("%Y-%m-%d")


def get_date_start_and_end_time(date_input: str):
    """
    获取指定日期的开始和结束时间
    Args:
        date_input (str | date): 日期，格式为YYYY-MM-DD 或 date 对象
    Returns:
        dict | None: 包含开始时间和结束时间的字典
        - start_time(str): 指定日期的开始时间 格式为YYYY-MM-DD 00:00:00
        - end_time(str): 指定日期的结束时间，格式为YYYY-MM-DD 23:59:59
    """
    if isinstance(date_input, str):
        try:
            target_date = datetime.strptime(date_input, "%Y-%m-%d").date()
        except ValueError as e:
            print(f"日期格式错误: {e}")
            return None
    elif isinstance(date_input, date):
        target_date = date_input
    else:
        raise ValueError(
            f"不支持的日期格式: {type(date_input)}，请使用字符串 'YYYY-MM-DD' 或 datetime.date 对象")

    start_time = datetime.combine(
        target_date, dt_time.min).strftime("%Y-%m-%d %H:%M:%S")
    end_time = datetime.combine(
        target_date, dt_time.max).strftime("%Y-%m-%d %H:%M:%S")
    return {
        "start_time": start_time,
        "end_time": end_time
    }


def retrieve_past_date(days_ago: int):
    """
    获取过去的日期
    Args:
        days_ago (int): 天数，例如1表示昨天，2表示前天，以此类推
    Returns:
        str: 过去的日期，格式为YYYY-MM-DD
    """
    current_date = date.today()
    delta = timedelta(days=days_ago)
    target_date = current_date - delta
    return target_date.strftime("%Y-%m-%d")


def get_second(time_minute: str):
    """
    将时间字符串转为秒级时间戳
    Args:
        time_minute (str): 时间字符串.
            - 格式为YYYY-MM-DD HH:MM
    Returns:
        int | None: 秒级时间戳
    """
    try:
        parsed = datetime.strptime(time_minute, "%Y-%m-%d %H:%M")
        parsed = parsed.replace(tzinfo=ZoneInfo("Asia/Shanghai"))
        return int(parsed.timestamp())
    except ValueError:
        print(f"时间字符串 {time_minute} 格式错误")
        return None
    except TypeError:
        print(f"时间字符串 {time_minute} 类型错误")
        return None


if __name__ == "__main__":
    print(f"当前时间戳为{timestamp()}毫秒")
    print(f"当前时间戳为{timestamp(is_second=True)}秒")
    print(f"当前日期为{get_current_date()}")
    print(f"昨天的日期为{retrieve_past_date(1)}")
    print(get_date_start_and_end_time("2025-12-10"))
    print(get_second("2026-03-25 20:00"))
