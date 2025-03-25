#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

from loguru import logger

from exceptions import *
from instance import images
from instance import pos
from txn.base import LegecloTransaction


class SkipStage(LegecloTransaction):
    """
    从能自由点击的主页开始跳过新手教程，最终再回到主页
    """
    TXN_NAME = "SkipStage"

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
                template=images.LIMITED_TIME_STORE,
                timeout=20,
            )
            logger.success(f"Transaction {self.TXN_NAME} end success")
            time.sleep(3)
            return True
        except TemplateNotFound:
            logger.error(f"Transaction {self.TXN_NAME} end failed")
            return False

    def operate(self) -> None:
        # 点击关卡
        self.ctl.touch_pos(pos.HOMEPAGE_STAGE)
        time.sleep(3)
        # 点击主线关卡
        self.ctl.touch_pos(pos.STAGE_MAIN)
        time.sleep(5)  # 有可能有长时间加载
        # 点击跳过关卡
        self.ctl.touch_pos(pos.STAGE_SKIP)
        time.sleep(3)
        # 点击决定
        self.ctl.touch_pos(pos.STAGE_SKIP_DECIDE)
        time.sleep(3)
        # 确认跳过
        self.ctl.touch_pos(pos.STAGE_SKIP_DECIDE_CONFIRM)
        time.sleep(10)  # 这里可能会卡一会儿
        # 确认成功跳过
        self.ctl.touch_pos(pos.STAGE_SKIP_SUCCESS_OK)
        # 会在长加载后回到主页，逻辑交给 assert_end

    def recover_end(self) -> bool:
        time.sleep(10)
        logger.warning(f"Recover {self.TXN_NAME}")
        # 如果是确认成功跳过没点上，点主页会无效，这里就尝试再点一下
        self.ctl.touch_pos(pos.STAGE_SKIP_SUCCESS_OK)
        time.sleep(10)
        # 也不用检测说明主页按钮了，一定在
        # 哪怕不在，检测不在然后报错，和执行 recover 后再次报错，效果都一样
        self.ctl.touch_pos_multiple(
            pos=pos.HOMEPAGE_HOMEPAGE,
            times=10,
            interval=1,
        )
        return self.assert_end()

    def execute(self) -> None:
        can_start = self.assert_start()
        if not can_start:
            # 修复逻辑，暂时不知道怎么写，可能就只有等待，如果等待之后再不成功就 fatal
            pass
        self.operate()
        can_end = self.assert_end()
        if not can_end:
            # 修复逻辑
            # 整个过程都可以看得左下方的主页按钮，除非非常特殊的情况
            # 不如卡在了白屏加载过程中，或者因为网络原因所有的按钮都失效
            # 这里的修复逻辑就是，只要确保回了主页就行，就当跳过这一步，对后续也没有影响
            # 不要考虑怎么保证一定跳过主线，意义很小，操作难度很高
            can_recover = self.recover_end()
            if not can_recover:
                logger.error(f"Transaction {self.TXN_NAME} recover failed")
                # 这样就只能报错了，异常我还没写
                raise ValueError(f"Transaction {self.TXN_NAME} failed")


if __name__ == "__main__":
    pass
