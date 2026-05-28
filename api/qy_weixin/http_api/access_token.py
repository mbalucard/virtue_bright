"""
access_token接口
    - 获取access_token
"""

from httpx import request, AsyncClient
from configs.api_configes import qy_env
from configs.server import RedisServer
from redis import Redis


def get_access_token():
    """获取企业微信access_token"""
    r = Redis(host=RedisServer.Host, port=RedisServer.Port, db=RedisServer.DB,password=RedisServer.Password,decode_responses=True)
    key = "qy_access_token"
    if r.exists(key):
        js_data = r.hgetall(key)
        js_data['expires_in']=r.ttl(key)
        r.hset(key,mapping=js_data)
        return js_data
    else:
        token_url = f"{qy_env['base_url']}/gettoken?corpid={qy_env['corp_id']}&corpsecret={qy_env['secret']}"
        response = request("GET", token_url)
        response_json = response.json()
        r.hset(key,mapping=response_json)
        r.expire(key,response_json['expires_in'])
        return response_json

if __name__ == '__main__':
    data = get_access_token()
    print(data)