from pywebio.input import input_group, input, select, checkbox, NUMBER
from pywebio.output import (
    put_markdown,
    use_scope,
    put_processbar,
    set_processbar,
    put_buttons,
    put_file,
    put_text,
    put_loading,
    put_scrollable,
    popup,
    put_success,
    put_info,
    put_error,
    toast,
    clear_scope,
)
from pywebio.platform.tornado import start_server
from pywebio.platform import config
from pywebio_battery import put_logbox, logbox_append, confirm
from libdigisum import Step, solve_max, solve_min, expected_answer, digisum
import random
from functools import partial

MAX_NUMBER = 1e9 + 5


def validate_n(n):
    if n <= 1:
        return "需要一个超过1的正整数"
    elif n >= MAX_NUMBER:
        return "数字太大了，请在本地部署并计算"
    return None


def logbox_callback(prog: tuple, step: Step):
    logbox_append("out", step.to_string() + "\n")


def progress_callback(prog: tuple, step: Step):
    if prog[0] % (prog[1] // 100) == 0:
        set_processbar("progress", prog[0] / prog[1])


def get_file(res: dict):
    with use_scope("print_file_scope"):
        clear_scope()
        with put_loading():
            alphabet = [chr(i) for i in range(ord("a"), ord("z") + 1)]
            random.shuffle(alphabet)
            rand = "".join(random.sample(alphabet, 6))
            msg = ""
            for st in res["steps"]:
                msg += st.to_string()
                msg += "\n"
            ctnt = msg.encode("utf-8")
            put_file(name=f"result-{rand}.txt", content=ctnt)


def print_steps(res: dict):
    with use_scope("print_result_scope"):
        clear_scope()
        with put_loading():
            msg = ""
            for st in res["steps"]:
                msg += st.to_string()
                msg += "\n"
            put_scrollable(
                content=msg,
                height=400,
            )


def display_about():
    about_text = """
“数位和合并” 问题
Python 在线求解界面
由 PyWebIO 驱动

问题分析/解法提出：
    深圳实验学校高中部 高一(4)班 黎远睿
    深圳实验学校高中部 高一(2)班 吴书玮

C++ 求解程序：
    主要由 深圳实验学校高中部 高一(2)班 吴书玮 完成

Python 程序移植：
    由 深圳实验学校高中部 高一(4)班 黎远睿 完成

C++ 和 Python 程序开源于 https://git.6leo6.com/66Leo66/digisum
""".strip()

    popup(
        title="关于此程序",
        content=about_text,
    )


def result_btn_handler(res: dict, btn: str):
    if btn == "save":
        get_file(res)
    elif btn == "display":
        print_steps(res)
    elif btn == "about":
        display_about()


@config(theme="minty")
def digisum_io():
    put_markdown("# 数位和求解程序")
    user_input = input_group(
        "运行参数",
        [
            input(
                label="输入参数 n",
                name="num",
                type=NUMBER,
                validate=validate_n,
                value=2018,
                help_text="初始数列将为 [1, n] 中所有整数",
            ),
            select(
                label="选择求解类型",
                name="type",
                options=[
                    {"label": "最大值", "value": "max"},
                    {"label": "最小值", "value": "min"},
                ],
            ),
            checkbox(
                label="额外参数",
                name="extras",
                options=[
                    {"label": "实时显示结果", "value": "live_output"},
                    {"label": "启用 Debug", "value": "debug"},
                ],
            ),
        ],
    )
    display_msg: str
    exp_max: int
    exp_min: int
    exp_ans: int
    with use_scope("precalc"):
        inp = user_input["num"]
        exp_max = expected_answer(int(inp))
        exp_min = exp_max
        while exp_min > 10:
            exp_min = digisum(exp_min)

        display_msg = f"根据您的输入数据 n={inp}:\n结果的最小值为 {exp_min}\n结果的最大值为 {exp_max}"
        ask = confirm(
            title="计算已初步完成",
            content=[
                display_msg,
                put_markdown("### 您要继续求解运算步骤吗"),
            ],
        )
        with use_scope("result"):
            if ask:
                # print(int(user_input["num"]))
                callback: object
                if "live_output" in user_input["extras"]:
                    put_logbox("out")
                    callback = logbox_callback
                else:
                    put_processbar("progress")
                    callback = progress_callback

                res: dict
                if user_input["type"] == "max":
                    exp_ans = exp_max
                    res = solve_max(int(user_input["num"]), callback)
                    if "debug" in user_input["extras"]:
                        put_info(f"mid = {res['mid']}")
                        need_logs = 5
                        msg = ""
                        for i in range(need_logs, 0, -1):
                            st = res["steps"][-i].to_string()
                            msg += f"last {i} step: {st}\n"
                        put_info(msg)
                else:
                    exp_ans = exp_min
                    res = solve_min(int(user_input["num"]), callback)

                put_markdown("---")
                put_info(f"求解 {user_input['num']}, 解得答案为: {res['answer']}")
                if res["answer"] == exp_ans:
                    put_success(
                        "✅ 求得的答案 {} 与预期答案 {} 相符！".format(res["answer"], exp_ans)
                    )
                else:
                    put_error("❌ 求得的答案 {} 与预期答案 {} 不符！".format(res["answer"], exp_ans))
                result_btn = [{"label": "将步骤保存为文本文件", "value": "save"}]
                # put_button(label="将步骤保存为文本文件", onclick=lambda: get_file(res))

                if not "live_output" in user_input["extras"]:
                    # put_button(label="显示步骤", onclick=lambda: print_steps(res))
                    result_btn.append({"label": "显示求解步骤", "value": "display"})
                result_btn.append({"label": "关于", "value": "about"})
                put_buttons(result_btn, partial(result_btn_handler, res))
            else:
                put_text(display_msg)
                put_markdown("### 感谢使用")


if __name__ == "__main__":
    digisum_io()
    exit(0)
    start_server(
        digisum_io,
        port=80,
        host="",
        remote_access=False,
        # cdn="https://cdn1.tianli0.top/gh/wang0618/PyWebIO-assets@v{version}/",
    )
