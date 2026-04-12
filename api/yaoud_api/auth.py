from httpx import AsyncClient
from api.yaoud_api.aes_tool import aes_cfb_encrypt_base64
from configs.api_configes import yaoud_env


async def log_in(username: str, password: str) -> dict:
    """
    登陆药德系统

    Args:
        username (str): 药德用户名
        password (str): 药德密码

    Returns:
        dict: 登陆成功返回的人员信息
    """
    user_url = f"{yaoud_env['url']}/auth/oauth2/token"
    password_encrypted = aes_cfb_encrypt_base64(password)
    headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "authorization": yaoud_env["public_key"],
        "client-tom": "Y",
        "skipToken": "true",
    }
    params = {
        "grant_type": "password",
        "username": username,
        "randomStr": "blockPuzzle",
        "code": "",
        "scope": "server",
    }
    payload = {
        "password": password_encrypted,
    }
    async with AsyncClient() as client:
        response = await client.post(
            user_url, headers=headers,
            params=params, data=payload,timeout=yaoud_env["timeout"])
    return response.json()


async def get_authorization(username: str, password: str) -> dict:
    """
    获取药德系统的授权信息

    Args:
        username (str): 药德用户名
        password (str): 药德密码

    Returns:
        dict: 包含授权信息和租户ID的字典
    """

    response = await log_in(username, password)
    authorization = response["token_type"]+" "+response["access_token"]
    current_status = {
        "tenantId": response["tenantId"],
        "enterpriseId": response["enterpriseId"],
        "organId": response["organId"],
        "organType": response["organType"],
        "user_id": response["user_id"]
    }
    resource = {"organIds": response["organIds"],
                "tenantIds": response["tenantIds"],
                "enterpriseIds": response["enterpriseIds"]}
    return {"authorization": authorization, "currentStatus": current_status, "resource": resource}


if __name__ == "__main__":
    import asyncio
    # res = asyncio.run(log_in("18991373511", "Mb19860221"))
    # print(res)
    auth = asyncio.run(get_authorization("13396129397", "xl6688"))
    print("auth:", auth)
