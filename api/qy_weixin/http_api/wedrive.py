"""
微盘接口
    - 创建空间 space_create
    - 解散空间 space_dismiss
"""
from configs.api_configes import qy_env
from httpx import AsyncClient
from typing import Optional

base_url = f"{qy_env['base_url']}/wedrive"
ttl = qy_env["ttl"]


async def space_create(
    access_token: str,
    space_name: str,
    member_type: int = 1,
    userid: Optional[str] = None,
    departmentid: Optional[int] = None,
    auth_type: int = 7) -> dict:
    """
    创建空间
    文档: https://developer.work.weixin.qq.com/document/path/93655
    Args:
        access_token (str): 企业微信 access_token
        space_name (str): 空间名称
        member_type (int): 成员类型, Defaults to 1.
            - 1: 用户
            - 2: 部门
        userid (str,None): 用户ID,也是用户的账号. Defaults to None.
        departmentid (int,None): 部门ID. Defaults to None.
        auth_type (int): 授权类型, Defaults to 7.
            - 7: 空间管理员(最多可指定3个)
            - 1: 仅下载
            - 4: 可预览
    Returns:
        空间信息
        包含: spaceid
    """
    url = f"{base_url}/space_create"
    params = {
        "access_token": access_token,
    }
    auth_info = {
        "type": member_type,
        "auth": auth_type,
    }
    if member_type == 1 and userid:
        auth_info["userid"] = userid
    if departmentid and member_type == 2:
        auth_info["departmentid"] = departmentid
        if auth_type == 7:
            auth_info["auth"] = 1

    payload = {
        "space_name": space_name,
        "auth_info": [auth_info],
        "space_sub_type": 0
    }
    async with AsyncClient() as client:
        response = await client.post(url, params=params, json=payload, timeout=ttl)
        response.raise_for_status()
        return response.json()


async def space_dismiss(
    access_token: str,
    spaceid: str,) -> dict:
    """
    解散空间
    文档: https://developer.work.weixin.qq.com/document/path/97857
    Args:
        access_token (str): 企业微信 access_token
        spaceid (str): 空间ID
    Returns:
        空字典
    """
    url = f"{base_url}/space_dismiss"
    params = {
        "access_token": access_token,
    }
    payload = {
        "spaceid": spaceid,
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
    userid = "ma_bo@demingjiankang.cn"

    async def main():

        data = await space_create(
            access_token=access_token,
            space_name="测试空间1",
            member_type=2
            # admin_users=userid,
        )
        print(data)

    asyncio.run(main())
