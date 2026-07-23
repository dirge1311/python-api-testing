"""
test_09.py — 独立练习：从零写完，不靠模板
===========================================

这是第一个完全独立完成的文件。老师只给了需求：
    函数1：POST 添加宠物（parametrize 数据驱动，3组数据）
    函数2：GET 查宠物（3个断言）

踩过的坑（全部自己排查并修复）：
    坑1：列表和字典里漏逗号 → 每一项后面必须加英文逗号
    坑2：函数没写参数 → parametrize 的数据需要函数"开门接收"
    坑3：assert 用 = 而不是 == → = 是赋值，== 才是判断
    坑4：args 字段名写错 → URL 里的参数名是什么，args 里的 key 就是什么
         URL: ?pet_type=dog  →  args: {"pet_type": "dog"}  → 取值 ["pet_type"]

你现在已经能够：
    ✅ 看懂需求 → 翻译成代码 → 自己排查报错 → 全部跑通
    ✅ 这就是接口自动化测试工程师的日常工作流程。
"""

import requests
import pytest

# ============================================================
# 函数1：添加宠物 — parametrize 数据驱动
# ============================================================
test_data = [
    ("小黄", "dog",    100, 200),
    ("小黑", "cat",    200, 200),
    ("小白", "rabbit", 150, 200),
]

@pytest.mark.parametrize("pet_name,type,price,expected_status", test_data)
def test_添加宠物(pet_name, type, price, expected_status):
    """POST 添加宠物 —— 参数化3组数据"""
    r = requests.post(
        "https://postman-echo.com/post",
        json={
            "pet_name": pet_name,
            "type": type,
            "price": price,
        }
    )
    # 断言1：HTTP 状态码正确
    assert r.status_code == expected_status
    # 断言2：服务器正确识别 JSON 格式
    assert "json" in r.json()


# ============================================================
# 函数2：查宠物 — 普通测试函数
# ============================================================
def test_查宠物():
    """GET 查询宠物 —— 根据 pet_type 筛选"""
    r = requests.get("https://postman-echo.com/get?pet_type=dog")

    # 断言1：状态码 200
    assert r.status_code == 200

    # 断言2：pet_type 参数被服务器正确接收
    # URL 里写的是 ?pet_type=dog，所以 args 里的 key 就是 pet_type
    assert r.json()["args"]["pet_type"] == "dog"

    # 断言3：url 字段存在（服务器回显了完整请求地址）
    assert "url" in r.json()

# ============================================================
# 你现在的完整技能栈：
# ============================================================
#   requests.get() / requests.post()    → 发请求
#   assert == / assert in               → 断言
#   def test_xxx():                     → pytest 用例
#   @pytest.mark.parametrize            → 数据驱动
#   python -m pytest xxx.py -v          → 跑用例看结果
#   看报错 → 定位 → 修改 → 跑通         → 独立排查问题
# ============================================================
