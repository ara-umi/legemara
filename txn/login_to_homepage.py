#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import time

from loguru import logger

from exceptions import *
from instance import images
from instance import pos
from txn.base import LegecloTransaction


class LoginToHomepage(LegecloTransaction):
    """
    从登录页面开始，保证点击 GAME START 后直接跳转进入取名
        只要之前删除过账号一次，就可以永久跳过 erolabs 黑端登录界面
    之后执行取名、确认跳过新手教程，到达主页（主页会立刻跳出剩余的新手教程，除了指定按钮其他位置都非高光）
    """
    TXN_NAME = "LoginToHomepage"

    def assert_start(self) -> bool:
        try:
            self.ctl.loop_find_template(
                template=images.LOGIN_PAGE_SYMBOL,
                threshold=0.75,  # logo 会闪烁，适当降低阈值
                timeout=3,
            )
            logger.success(f"Transaction {self.TXN_NAME} start success")
            return True
        except TemplateNotFound:
            logger.error(f"Transaction {self.TXN_NAME} start failed")
            return False

    def assert_end(self) -> bool:
        try:
            self.ctl.loop_find_template(
                template=images.BEGINNER_CONVERSATION,
                interval=3,
                timeout=60,
            )
            logger.success(f"Transaction {self.TXN_NAME} end success")
            time.sleep(3)  # 统一都做短暂休眠，方便不同事务间衔接
            return True
        except TemplateNotFound:
            logger.error(f"Transaction {self.TXN_NAME} end failed")
            return False

    def operate(self) -> None:
        # 点击 GAME START
        self.ctl.touch_pos(pos.GAME_START)
        # 进入起名界面
        self.ctl.loop_find_template_no_exception(
            template=images.NAME_RULE,
            interval=1,
            timeout=60,  # 会直接跑加载条，可能花费很长时间
        )  # 点击 GAME START 成功，哪怕找不到也不抛出异常，仅用于脚本提速
        # 点击起名输入框
        self.ctl.touch_pos(pos.NAME_INPUT)
        time.sleep(1)
        # 输入玩家名
        alphabet = "1234567890"
        length = 3
        gamer_name: str = ''.join(random.choice(alphabet) for _ in range(length))
        self.ctl.type_text(gamer_name)
        time.sleep(1)
        # 点击确认，要点两下，第一下来退出输入框
        self.ctl.touch_pos_multiple(
            pos=pos.NAME_INPUT_OK,
            times=2,
            interval=1
        )
        time.sleep(3)
        # 检测弹出跳过新手教程提示
        self.ctl.loop_find_template_no_exception(
            template=images.IF_SKIP_BEGINNER,
            timeout=30,  # 可能需要花费一定时间
        )  # 起名成功
        time.sleep(1)
        # 点击跳过新手教程
        self.ctl.touch_pos(pos.SKIP_BEGINNER)
        # 之后等待进入主页，逻辑交给 assert_end

    def execute(self) -> None:
        can_start = self.assert_start()
        if not can_start:
            # 修复逻辑，暂时不知道怎么写，可能就只有等待，如果等待之后再不成功就 fatal
            pass
        self.operate()
        can_end = self.assert_end()
        if not can_end:
            # 修复逻辑，暂时不知道怎么写
            pass


if __name__ == "__main__":
    pass
