"""
用户接口
    - 获取用户信息 get_user_info
    - 获取部门用户列表-简易信息 department_user_simplelist
    - 获取部门用户列表-详细信息 department_user_list
    - 将企业微信用户ID转换为OpenID convert_to_openid
    - 根据手机号获取用户ID userid_by_mobile
    - 将邮箱转换为用户ID userid_by_email
"""

from configs.api_configes import qy_env
from httpx import AsyncClient
from typing import Optional

base_url = f"{qy_env['base_url']}/user"
ttl = qy_env["ttl"]


async def get_user_info(
        access_token: str,
        userid: str,) -> dict:
    """
    获取用户信息
    文档: https://developer.work.weixin.qq.com/document/path/90196
    Args:
        access_token (str): 企业微信 access_token
        userid (str): 用户ID,也是用户的账号
    Returns:
        用户信息
    """
    url = f"{base_url}/get"
    params = {
        "access_token": access_token,
        "userid": userid,
    }
    async with AsyncClient() as client:
        response = await client.get(url, params=params, timeout=ttl)
        response.raise_for_status()
        return response.json()


async def department_user_simplelist(
        access_token: str,
        department_id: int = 1,) -> dict:
    """
    获取部门用户列表-简易信息
    文档: https://developer.work.weixin.qq.com/document/path/90200
    Args:
        access_token (str): 企业微信 access_token
        department_id (int): 部门ID, Defaults to 1.
            - 1: 根部门ID
    Returns:
        部门用户列表
        包含: name, department, userid
    """
    url = f"{base_url}/simplelist"
    params = {
        "access_token": access_token,
        "department_id": department_id,
    }
    async with AsyncClient() as client:
        response = await client.get(url, params=params, timeout=ttl)
        response.raise_for_status()
        return response.json()


async def department_user_list(
        access_token: str,
        department_id: int = 1,) -> dict:
    """
    获取部门用户列表-详细信息
    文档: https://developer.work.weixin.qq.com/document/path/90201
    Args:
        access_token (str): 企业微信 access_token
        department_id (int): 部门ID, Defaults to 1.
            - 1: 根部门ID
    Returns:
        部门用户列表
        包含: name, department, position, status, enable, isleader, extattr, hide_mobile, telephone, order, external_profile, main_department, alias, is_leader_in_dept, userid, direct_leader
    """
    url = f"{base_url}/list"
    params = {
        "access_token": access_token,
        "department_id": department_id,
    }
    async with AsyncClient() as client:
        response = await client.get(url, params=params, timeout=ttl)
        response.raise_for_status()
        return response.json()


async def convert_to_openid(
        access_token: str,
        userid: str,) -> dict:
    """
    将企业微信用户ID转换为OpenID
    文档: https://developer.work.weixin.qq.com/document/path/90202
    Args:
        access_token (str): 企业微信 access_token
        userid (str): 用户ID,也是用户的账号
    Returns:
        OpenID
    """
    url = f"{base_url}/convert_to_openid"
    params = {
        "access_token": access_token,
    }
    payload = {
        "userid": userid,
    }
    async with AsyncClient() as client:
        response = await client.post(url, params=params, json=payload, timeout=ttl)
        response.raise_for_status()
        return response.json()


async def userid_by_mobile(
        access_token: str,
        mobile: str,) -> dict:
    """
    将手机号转换为用户ID
    文档: https://developer.work.weixin.qq.com/document/path/95402
    Args:
        access_token (str): 企业微信 access_token
        mobile (str): 手机号
    Returns:
        用户ID
    """
    url = f"{base_url}/getuserid"
    params = {
        "access_token": access_token,
    }
    payload = {
        "mobile": mobile,
    }
    async with AsyncClient() as client:
        response = await client.post(url, params=params, json=payload, timeout=ttl)
        response.raise_for_status()
        return response.json()


async def userid_by_email(
        access_token: str,
        email: str,
        email_type: Optional[int] = None,) -> dict:
    """
    将邮箱转换为用户ID
    文档: https://developer.work.weixin.qq.com/document/path/95895
    Args:
        access_token (str): 企业微信 access_token
        email (str): 邮箱
        email_type (int, None): 邮箱类型, Defaults to None.
            - 1: 企业邮箱(默认)
            - 2: 个人邮箱
    Returns:
        用户ID
    """
    url = f"{base_url}/get_userid_by_email"
    params = {
        "access_token": access_token,
    }
    payload = {
        "email": email,
        "email_type": email_type,
    }
    async with AsyncClient() as client:
        response = await client.post(url, params=params, json=payload, timeout=ttl)
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    import asyncio
    from access_token import get_access_token

    auth = get_access_token()
    access_token = auth["access_token"]
    userid = "PanXuSheng"
    mobile = "18991373511"
    email = "panxusheng@demingjiankang.cn"

    async def main():
        data = await userid_by_email(
            access_token=access_token,
            email=email,
        )
        print(data)

    asyncio.run(main())
