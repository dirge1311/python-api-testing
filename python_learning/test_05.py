"""
test_05.py — 数据驱动测试：CSV 文件 + for 循环 = Postman Collection Runner
============================================================================

Postman 对照：
    Postman                            Python
    ────────                           ──────
    准备 CSV 文件（login_data.csv）     同一个 CSV 文件
    Runner → Select File 加载 CSV      with open("文件.csv") as f:
    Runner 逐行读取                      for row in reader:
    用 {{变量名}} 替换 Body 里的值       row["列名"] 取对应列的值
    每行跑一次请求                      循环体里每次 requests.post()
    跑完看汇总                          assert 挨个判断

==============================================================================
CSV 文件格式回顾：
==============================================================================

    用户名,密码,预期包含        ← 第一行：列名（表头）
    admin,123456,登录成功       ← 第二行开始：测试数据
    testuser,abcdef,登录成功
    ,,用户名不能为空            ← 空值就什么都不写，两个逗号中间留空

    DictReader 做的事：把每一行转成字典，列名就是 key
    第一行数据 → {"用户名": "admin", "密码": "123456", "预期包含": "登录成功"}
    第二行数据 → {"用户名": "testuser", "密码": "abcdef", "预期包含": "登录成功"}

==============================================================================
逐行解释核心语法：
==============================================================================
"""

import requests
import csv    # Python 自带的 CSV 读写库，不需要额外安装

def test_数据驱动():
    # ---------------------------------------------------------------
    # with open(...) as f:
    #   打开文件，把文件对象赋值给 f
    #   "r" = read 只读模式
    #   encoding="utf-8" = 中文不乱码的关键
    #   with 的好处：代码块结束后自动关闭文件，不用手动关
    # ---------------------------------------------------------------
    with open("python_learning/login_data.csv", "r", encoding="utf-8") as f:

        # ---------------------------------------------------------------
        # csv.DictReader(f)
        #   Dict = Dictionary = 字典
        #   把 CSV 第一行当 key（列名），后面每一行变成 {"列名": "值"}
        #   普通 Reader 返回列表 ["admin", "123456", "登录成功"]
        #   DictReader 返回字典 {"用户名": "admin", "密码": "123456", ...}
        #   → DictReader 更好用，因为用列名取值比用序号取值直观
        # ---------------------------------------------------------------
        reader = csv.DictReader(f)

        # ---------------------------------------------------------------
        # for row in reader:
        #   逐行遍历，每次循环 row 就是一行数据（一个字典）
        #   3 行数据 → 循环跑 3 次
        #   等价于 Postman Runner 里 Iterations 那个进度条
        # ---------------------------------------------------------------
        for row in reader:
            # ---------------------------------------------------------------
            # row["用户名"] = 取当前行"用户名"那一列的值
            # row["密码"]   = 取当前行"密码"那一列的值
            #
            # json={"username": row["用户名"], "password": row["密码"]}
            #   等价于 Postman Body 里写：
            #   {"username": "{{用户名}}", "password": "{{密码}}"}
            #
            #   第一轮：json={"username": "admin", "password": "123456"}
            #   第二轮廓：json={"username": "testuser", "password": "abcdef"}
            #   第三轮廓：json={"username": "", "password": ""}
            # ---------------------------------------------------------------
            r = requests.post(
                "https://postman-echo.com/post",
                json={"username": row["用户名"], "password": row["密码"]}
            )

            # f"..." 是 f-string，花括号里的变量会自动替换成值
            # f"测试: {row['用户名']}" → 第一轮打印 "测试: admin"
            print(f"测试: {row['用户名']} / {row['密码']}")

            assert r.status_code == 200
            print("  通过！")

    print("\n全部数据跑完！")

# ============================================================
# 你现在掌握了 Python 接口测试的完整闭环：
# ============================================================
#
#   test_01.py  → GET 请求（= Postman GET + Send）
#   test_02.py  → POST 请求（= Postman Body → raw → JSON）
#   test_03.py  → assert 断言（= Postman Tests 标签页）
#   test_04.py  → pytest 框架（= Postman Collection Runner）
#   test_05.py  → CSV 数据驱动（= Runner 加载 CSV 批量跑）
#
#   Postman 能做的，Python 全部能做，而且能写进脚本自动化。
