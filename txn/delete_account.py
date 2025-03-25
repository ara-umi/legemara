#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

from loguru import logger

from exceptions import *
from instance import images
from instance import pos
from txn.base import LegecloTransaction


class DeleteAccount(LegecloTransaction):
    """
    从能自由点击的主页开始删除账号，退回登录界面
    """
    TXN_NAME = "DeleteAccount"

    def assert_start(self) -> bool:
        try:
            self.ctl.loop_find_template(
                template=images.LIMITED_TIME_STORE,
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
                template=images.LOGIN_PAGE_SYMBOL,
                threshold=0.75,  # logo 会闪烁，适当降低阈值
                interval=3,
                timeout=60,
            )
            logger.success(f"Transaction {self.TXN_NAME} end success")
            time.sleep(3)
            return True
        except TemplateNotFound:
            logger.error(f"Transaction {self.TXN_NAME} end failed")
            return False

    def operate(self) -> None:
        # 点击选单
        self.ctl.touch_pos(pos.HOMEPAGE_MENU)
        time.sleep(2)
        # 点击删除账号
        self.ctl.touch_pos(pos.MENU_DELETE_ACCOUNT)
        time.sleep(2)
        self.ctl.touch_pos(pos.DELETE_ATTENTION_CONFIRM1)
        time.sleep(2)
        self.ctl.touch_pos(pos.DELETE_ATTENTION_CONFIRM2)
        time.sleep(5)
        self.ctl.touch_pos(pos.DELETE_SUCCESS_OK)
        # 之后会加载进登录界面，逻辑交给 assert_end

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
