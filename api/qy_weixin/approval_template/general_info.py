"""
审批通用信息
    - 审批流程节点 approval_process_node
    - 摘要行信息 summary_info_list
"""
from typing import List


def approval_process_node(
        userid_list: List[str],
        node_type: int = 1,
        apv_rel: int = 2,) -> dict:
    """
    审批流程节点
    Args:
        userid_list (List[str]): 审批人userid列表
        node_type (int, optional): 节点类型 type:int 1:审批人 2:抄送人 3:办理人. Defaults to 1.
        apv_rel (int, optional): 多人审批方式 type:int 1-会签 2-或签 3-依次审批. Defaults to 2.
    Returns:
        dict: 审批流程节点
    """
    return {
        "type": node_type,
        "apv_rel": apv_rel,
        "userid": userid_list
    }


def summary_info_list(
    text_list: List[str]) -> dict:
    """
    摘要行信息，用于定义某一行摘要显示的内容, 最多显示3行
    Args:
        text_list (List[str]): 摘要行显示文字列表
    Returns:
        dict: 摘要行信息
    """
    if len(text_list) > 3:
        text_list = text_list[:3]

    summary_list = []
    for text in text_list:
        summary_list.append({
            "text": text,
            "lang": "zh_CN"
        })
    return summary_list



if __name__ == '__main__':
    summary_info = summary_info_list(["请假信息"])
    summary_list = [{"summary_info": summary_info}]
    print(summary_list)
    process_node = approval_process_node(['user_id'])
    process = {"node_list": [process_node]}
    print(process)