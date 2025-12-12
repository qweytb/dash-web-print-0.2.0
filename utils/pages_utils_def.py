from copy import deepcopy
from typing import Any, Dict, List, Union


# 删除指定 UUID 的 FefferyRND 组件
def remove_rnd_by_uuid(rnd_list, target_uuid):
    """
    rnd_list : 你贴出的 FefferyRND 组件列表
    target_uuid: 只想删的 UUID 字符串，例如
                 '2e5bb0b6-a318-4598-ac7d-62bd609dc5fa'
    返回: 删除后的新列表（原列表不变）
    """
    # 深拷贝一份，避免意外改到原数据
    new_list = deepcopy(rnd_list)
    # 倒序遍历，删除时不会影响前面索引
    for i in range(len(new_list) - 1, -1, -1):
        comp = new_list[i]
        # 取出 UUID
        cid = comp["props"]["id"]["id"]  # {'type':'RND','id':UUID}
        if cid == target_uuid:
            del new_list[i]
            break  # 只删第一个匹配就结束
    return new_list


# 只保留指定 UUID 的组件 特效
def select_only_uuid(components: Union[List[Any], Any], target_uuid: str) -> Union[List[Any], Any]:
    """
    只保留指定 UUID 的组件
    :param components: 组件列表
    :param target_uuid: 目标 UUID
    :return: 新的组件列表
    """
    if not isinstance(components, list):
        wrapped, components = True, [components]
    else:
        wrapped = False

    new_comps = components  # copy.deepcopy(components)

    def walk(nodes: List[Any]):
        for node in nodes:
            # ① 必须是字典 ② 必须是 FefferyRND
            if isinstance(node, dict) and node.get("type") == "FefferyRND":
                rid = node.get("props", {}).get("id", {})
                if rid.get("type") == "RND" and rid.get("id") == target_uuid:
                    node["props"]["selected"] = True
                    node["props"]["selectedStyle"] = {
                        # "border": "2px solid #1976D2",  # 粗蓝框
                        "backgroundColor": "#e3f2fd",  # 淡蓝背景（实色）
                        "boxShadow": "none",
                        "boxSizing": "border-box",  # 🔥 关键：边框算在总尺寸内
                    }
                else:
                    node["props"]["selected"] = False
                    node["props"]["selectedStyle"] = {}

                # 继续递归它的 children
                children = node.get("props", {}).get("children", [])
                if isinstance(children, list):
                    walk(children)

    walk(new_comps)
    return new_comps[0] if wrapped else new_comps


def find_field_value(data, field_name):
    """
    递归查找 JSON 数据中指定字段的值。

    :param data: JSON 数据（可以是字典或列表）
    :param field_name: 要查找的字段名
    :return: 字段的值，如果未找到则返回 None
    """
    if isinstance(data, dict):  # 如果是字典
        for key, value in data.items():
            if key == field_name:
                return value
            if isinstance(value, (dict, list)):  # 如果值是字典或列表，递归查找
                result = find_field_value(value, field_name)
                if result is not None:
                    return result
    elif isinstance(data, list):  # 如果是列表
        for item in data:
            result = find_field_value(item, field_name)
            if result is not None:
                return result
    return None


# ------------------- 用例 -------------------
# if __name__ == '__main__':
#     # 假设上面那段大列表变量叫 rnd_list
#     updated = remove_rnd_by_uuid(rnd_list,
#                                 '2e5bb0b6-a318-4598-ac7d-62bd609dc5fa')
#     print(f"删除后还剩 {len(updated)} 个组件")
