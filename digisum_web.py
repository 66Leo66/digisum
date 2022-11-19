from pywebio.input import input_group, input, select, checkbox, NUMBER
from pywebio.output import (
    put_markdown,
    use_scope,
    put_processbar,
    set_processbar,
    put_button,
    put_file,
    put_text,
    put_loading,
)
from pywebio.platform.tornado import start_server
from pywebio_battery import put_logbox, logbox_append, confirm
from libdigisum import Step, solve_max, solve_min, expected_answer, digisum
import random

MAX_NUMBER = 1e9 + 5


def validate_n(n):
    if n <= 1:
        return "需要一个超过1的正整数"
    elif n >= MAX_NUMBER:
        return "数字太大了，请在本地部署并计算"
    return None


def logbox_callback(prog: float, step: Step):
    logbox_append("out", step.to_string() + "\n")


def progress_callback(prog: float, step: Step):
    set_processbar("progress", prog)


def get_file(res: dict):
    with put_loading():
        alphabet = [chr(i) for i in range(ord("a"), ord("z") + 1)]
        random.shuffle(alphabet)
        rand = "".join(random.sample(alphabet, 6))
        msg = ""
        for st in res["steps"]:
            msg += st.to_string()
            msg += "\n"
        ctnt = msg.encode("utf-8")
        put_file(name=f"result-{rand}.txt", content=ctnt, scope="result")


def digisum_io():
    put_markdown("# 数位和求解程序")
    user_input = input_group(
        "运行参数",
        [
            input(
                label="输入参数 n", name="num", type=NUMBER, validate=validate_n, value=2018
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
                options=[{"label": "实时显示结果", "value": "live_output"}],
            ),
        ],
    )
    display_msg: str
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
                    res = solve_max(int(user_input["num"]), callback)
                else:
                    res = solve_min(int(user_input["num"]), callback)
                put_markdown(f"### 解得答案为: {res['answer']}")
                put_button(label="将步骤保存为文本文件", onclick=lambda: get_file(res))
            else:
                put_text(display_msg)
                put_markdown("### 感谢使用")


if __name__ == "__main__":
    digisum_io()
    exit(0)
    start_server(
        digisum_io,
        port=0,
        host="",
        remote_access=True,
        # cdn="https://cdn1.tianli0.top/gh/wang0618/PyWebIO-assets@v{version}/",
    )
