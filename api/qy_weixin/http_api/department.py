"""
部门接口
    - 获取子部门ID列表 department_simplelist
    - 获取部门详情 department_info
    - 获取部门列表 department_list
"""

from configs.api_configes import qy_env
from httpx import AsyncClient

base_url = f"{qy_env['base_url']}/department"
ttl = qy_env["ttl"]


async def department_simplelist(
        access_token: str,
        id: int = 1) -> dict:
    """
    获取子部门ID列表
    文档: https://developer.work.weixin.qq.com/document/path/95350
    Args:
        access_token (str): 企业微信 access_token
        id (int): 部门ID, Defaults to 1.
            - 1: 根部门ID
    Returns:
        子部门ID列表
    """
    url = f"{base_url}/simplelist"
    params = {
        "access_token": access_token,
        "id": id,
    }
    async with AsyncClient() as client:
        response = await client.get(url, params=params, timeout=ttl)
        response.raise_for_status()
        return response.json()


async def department_info(
        access_token: str,
        id: int = 1) -> dict:
    """
    获取部门详情
    文档: https://developer.work.weixin.qq.com/document/path/95351
    Args:
        access_token (str): 企业微信 access_token
        id (int): 部门ID, Defaults to 1.
            - 1: 根部门ID
    Returns:
        部门详情
    """
    url = f"{base_url}/get"
    params = {
        "access_token": access_token,
        "id": id,
    }
    async with AsyncClient() as client:
        response = await client.get(url, params=params, timeout=ttl)
        response.raise_for_status()
        return response.json()


async def department_list(
        access_token: str,
        id: int = 1) -> dict:
    """
    获取部门列表
    文档: https://developer.work.weixin.qq.com/document/path/90208
    Args:
        access_token (str): 企业微信 access_token
        id (int): 部门ID, Defaults to 1.
            - 1: 根部门ID
    Returns:
        部门列表
    """
    url = f"{base_url}/list"
    params = {
        "access_token": access_token,
        "id": id,
    }
    async with AsyncClient() as client:
        response = await client.get(url, params=params, timeout=ttl)
        response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    import asyncio
    from access_token import get_access_token

    async def main():
        auth = get_access_token()
        access_token = auth["access_token"]
        data = await department_list(access_token)
        print(data)

    asyncio.run(main())
