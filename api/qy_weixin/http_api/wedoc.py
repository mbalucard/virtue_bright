"""
文档接口
    - 新建文档 create_doc
"""

from configs.api_configes import qy_env
from httpx import AsyncClient
from typing import Optional

base_url = f"{qy_env['base_url']}/wedoc"
ttl = qy_env["ttl"]


async def create_doc(
        access_token: str,
        doc_name: str,
        spaceid: Optional[str] = None,
        fatherid: Optional[str] = None,
        doc_type: int = 3,
        admin_users: Optional[list[str]] = None,) -> dict:
    """
    新建文档
    文档: https://developer.work.weixin.qq.com/document/path/97460
    Args:
        access_token (str): 企业微信 access_token
        doc_name (str): 文档名称
            - 超过225个字符会被截断
        spaceid (Optional[str], optional): 空间 ID. Defaults to None.
            - 若制定 spaceid，则必须指定 fatherid
        fatherid (Optional[str], optional): 父文档 ID. Defaults to None.
            - 若在跟目录，fatherid 为 spaceid
        doc_type (int, optional): 文档类型. Defaults to 3.
            - 3: 普通文档
            - 4: 表格
            - 10: 智能表格
        admin_users (Optional[list], optional): 管理员用户列表. Defaults to None.
    """
    url = f"{base_url}/create_doc"
    params = {
        "access_token": access_token,
    }
    payload = {
        "doc_name": doc_name,
        "spaceid": spaceid if fatherid else None,
        "fatherid": fatherid,
        "doc_type": doc_type,
        "admin_users": admin_users,
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

        data = await create_doc(
            access_token=access_token,
            doc_name="测试文档1",
            admin_users=[userid],
        )
        print(data)

    asyncio.run(main())
