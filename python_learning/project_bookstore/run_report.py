"""
一键运行全项目 + 生成 HTML 测试报告

用法：
    python run_report.py

等价于手敲：
    python -m pytest . -v --html=report.html --self-contained-html
"""
import pytest
import os

# 获取当前文件所在目录
project_dir = os.path.dirname(__file__)

# 运行 pytest
# --html= 指定报告输出路径
# --self-contained-html 让 CSS 样式打包进一个文件
exit_code = pytest.main([
    project_dir,
    "-v",
    "--html=" + os.path.join(project_dir, "report.html"),
    "--self-contained-html"
])

# exit_code = 0 表示全部通过
if exit_code == 0:
    print("\n>>> 全部通过！报告已生成：report.html")
else:
    print(f"\n>>> 有失败用例，退出码：{exit_code}")
