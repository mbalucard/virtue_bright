"""
培训管理
    - 知识分类树: knowledge_classification_tree
    - 课件信息列表: courseware_info_page
    - 题库信息列表: question_bank_page
    - 任务信息列表: task_page
    - 培训计划列表: train_plan_page
"""


from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time


base_url = f"{yaoud_env['url']}/ehr"
TTL = yaoud_env["timeout"]

async def knowledge_classification_tree(
        authorization: str,
        tenant_id: Optional[int] = None,) -> dict:
    """
    知识分类树
    #! 无数据，待确认
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 知识分类树
    """
    url = f"{base_url}/knowledgeClassification/getTree"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "systemType": 0,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=TTL)
    return response.json()


async def courseware_info_page(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 10,
        coursewareName: Optional[str] = None,
        createIds: Optional[str] = None,
        coursewareStatus: Optional[int] = None,
        coursewareTypes: Optional[List[str]] = None,
        coursewareLevels: Optional[List[str]] = None,
        startDate: Optional[str] = None,
        endDate: Optional[str] = None,) -> dict:
    """
    课件信息列表
    #! 无数据，待确认
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 10.
        coursewareName (str, None): 课件名称. Defaults to None.
        createIds (str, None): 维护人. Defaults to None.
        coursewareStatus (int, None): 状态. Defaults to None.
            - 0: 已发布 1:草稿 2:已作废
        coursewareTypes (List[str], None): 课件类型. Defaults to None.
            - 0: 视频 1:音频 2:图片 3:ppt 4:pdf 5:word 6:excel
        coursewareLevels (List[str], None): 难度级别. Defaults to None.
            - 0: 简单 1:一般 2:较难 3:困难
        startDate (str, None): 维护日期时间区间-开始. Defaults to None.
            - 格式:yyyy-MM-dd
        endDate (str, None): 维护日期时间区间-结束. Defaults to None.
            - 格式:yyyy-MM-dd
    Returns:
        dict: 课件信息列表
    """
    url = f"{base_url}/coursewareInfo/pageList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    if startDate:
        startDate = get_date_start_and_end_time(startDate)
    if endDate:
        endDate = get_date_start_and_end_time(endDate)

    payload = {
        "systemType": 0,
        "current": current,
        "size": size,
        "coursewareName": coursewareName,
        "createIds": createIds,
        "coursewareStatus": coursewareStatus,
        "coursewareTypes": coursewareTypes,
        "coursewareLevels": coursewareLevels,
        "startDate": startDate['start_time'] if startDate else None,
        "endDate": endDate['end_time'] if endDate else None,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=TTL)
    return response.json()


async def question_bank_page(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 10,
        question: Optional[str] = None,
        createIds: Optional[str] = None,
        questionTypes: Optional[List[str]] = None,
        questionLevels: Optional[List[str]] = None,
        startDate: Optional[str] = None,
        endDate: Optional[str] = None,) -> dict:
    """
    题库信息列表
    #! 无数据，待确认
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 10.
        question (str, None): 题目. Defaults to None.
        createIds (str, None): 维护人. Defaults to None.
        questionTypes (List[str], None): 问题类型. Defaults to None.
            - 0:单选 1:多选 2:填空
        questionLevels (List[str], None): 难度级别. Defaults to None.
            - 0:简单 1:一般 2:较难 3:困难
        startDate (str, None): 维护日期时间区间-开始. Defaults to None.
            - 格式:yyyy-MM-dd
        endDate (str, None): 维护日期时间区间-结束. Defaults to None.
            - 格式:yyyy-MM-dd
    Returns:
        dict: 题库信息列表
    """
    url = f"{base_url}/questionBank/pageList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    if startDate:
        startDate = get_date_start_and_end_time(startDate)
    if endDate:
        endDate = get_date_start_and_end_time(endDate)

    payload = {
        "systemType": 0,
        "current": current,
        "size": size,
        "question": question,
        "createIds": createIds,
        "questionTypes": questionTypes,
        "questionLevels": questionLevels,
        "startDate": startDate['start_time'] if startDate else None,
        "endDate": endDate['end_time'] if endDate else None,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=TTL)
    return response.json()


async def task_page(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 10,
        taskName: Optional[str] = None,
        updateUser: Optional[str] = None,
        taskTypeList: Optional[List[str]] = None,
        taskForms: Optional[List[int]] = None,
        taskSourceList: Optional[List[int]] = None,
        taskLimitStart: Optional[str] = None,
        taskLimitEnd: Optional[str] = None,
        publishDateStart: Optional[str] = None,
        publishDateEnd: Optional[str] = None,
        updateDateStart: Optional[str] = None,
        updateDateEnd: Optional[str] = None,) -> dict:
    """
    任务信息列表
    #! 无数据，待确认
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 10.
        taskName (str, None): 任务名称. Defaults to None.
        updateUser (str, None): 维护人. Defaults to None.
        taskTypeList (List[str], None): 任务类型. Defaults to None.
            - 0: 学习任务 1: 考试任务
        taskForms (List[int], None): 任务形式. Defaults to None.
            - 0:课件/课后练习 1:刷题 2:考试
        taskSourceList (List[int], None): 创建方式. Defaults to None.
            - 0: 自动生成 1: 手动创建
        taskLimitStart (str, None): 任务期限区间-开始. Defaults to None.
            - 格式:yyyy-MM-dd
        taskLimitEnd (str, None): 任务期限区间-结束. Defaults to None.
            - 格式:yyyy-MM-dd
        publishDateStart (str, None): 发布日期时间区间-开始. Defaults to None.
            - 格式:yyyy-MM-dd
        publishDateEnd (str, None): 发布日期时间区间-结束. Defaults to None.
            - 格式:yyyy-MM-dd
        updateDateStart (str, None): 维护日期时间区间-开始. Defaults to None.
            - 格式:yyyy-MM-dd
        updateDateEnd (str, None): 维护日期时间区间-结束. Defaults to None.
            - 格式:yyyy-MM-dd
        #! 缺少培训计划名称参数，有数据了再确认
    return:
        dict: 任务信息列表
    """
    url = f"{base_url}/ehrTask/pageList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    if updateDateStart:
        updateDateStart = get_date_start_and_end_time(updateDateStart)
    if updateDateEnd:
        updateDateEnd = get_date_start_and_end_time(updateDateEnd)
    payload = {
        "systemType": 0,
        "current": current,
        "size": size,
        "taskName": taskName,
        "updateUser": updateUser,
        "taskTypeList": taskTypeList,
        "taskForms": taskForms,
        "taskSourceList": taskSourceList,
        "taskLimitStart": taskLimitStart,
        "taskLimitEnd": taskLimitEnd,
        "publishDateStart": publishDateStart,
        "publishDateEnd": publishDateEnd,
        "updateDateStart": updateDateStart['start_time'] if updateDateStart else None,
        "updateDateEnd": updateDateEnd['end_time'] if updateDateEnd else None,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=TTL)
    return response.json()



async def train_plan_page(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 10,
    trainPlanName: Optional[str] = None,
    updateUser: Optional[str] = None,
    enabledList: Optional[List[int]] = None,
    planStatusList: Optional[List[int]] = None,
    effectiveDateBegin: Optional[str] = None,
    effectiveDateEnd: Optional[str] = None,
    updateDateStart: Optional[str] = None,
    updateDateEnd: Optional[str] = None,)->dict:
    """
    培训计划列表
    #! 无数据，待确认
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 10.
        trainPlanName (str, None): 计划名称. Defaults to None.
        updateUser (str, None): 维护人. Defaults to None.
        enabledList (List[int], None): 启用状态. Defaults to None.
            - 0: 未启用 1: 已启用
        planStatusList (List[int], None): 生效状态. Defaults to None.
            - 0:未开始 1:进行中 2:已过期 3:已作废
        effectiveDateBegin (str, None): 生效日期区间-开始. Defaults to None.
            - 格式:yyyy-MM-dd
        effectiveDateEnd (str, None): 生效日期区间-结束. Defaults to None.
            - 格式:yyyy-MM-dd
        updateDateStart (str, None): 维护日期时间区间-开始. Defaults to None.
            - 格式:yyyy-MM-dd
        updateDateEnd (str, None): 维护日期时间区间-结束. Defaults to None.
            - 格式:yyyy-MM-dd
    """
    url = f"{base_url}/trainPlan/pageList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "current": current,
        "size": size,
        "trainPlanName": trainPlanName,
        "updateUser": updateUser,
        "enabledList": enabledList,
        "planStatusList": planStatusList,
        "effectiveDateBegin": effectiveDateBegin,
        "effectiveDateEnd": effectiveDateEnd,
        "updateDateStart": updateDateStart,
        "updateDateEnd": updateDateEnd,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=TTL)
    return response.json()

if __name__ == "__main__":
    import asyncio

    authorization = "Bearer new_521d29cf-d5dd-450c-b2d0-9c05ebe77c50"
    tenant_id = 148

    async def main():
        data = await train_plan_page(authorization, tenant_id)
        print(data)
    asyncio.run(main())
