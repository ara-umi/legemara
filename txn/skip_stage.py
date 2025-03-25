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
        try:
            can_start = self.assert_start()
            if not can_start:
                # 修复逻辑，暂时不知道怎么写，可能就只有等待，如果等待之后再不成功就 fatal
                pass
            self.operate()
            can_end = self.assert_end()
            if not can_end:
                # 整个过程都可以看得左下方的主页按钮
                # 只要确保回了主页就行，就当跳过这一步，对后续也没有影响
                # 我不敢再点一遍，因为如果是已经跳过了的情况，会点到很奇怪位置比如实力测试，产生不可预料的后果
                can_recover = self.recover_end()
                if not can_recover:
                    logger.warning(f"Transaction {self.TXN_NAME} failed to recover")
                    raise TransactionRecoverError(f"Transaction {self.TXN_NAME} failed to recover")
        except TransactionRecoverError:
            logger.warning(f"Transaction {self.TXN_NAME} failed to recover, rebooting...")
            self.ctl.reboot_legeclo()  # 重启游戏
            time.sleep(3)
            # 点击 GAME START
            self.ctl.touch_pos(pos.GAME_START)
            # 一定能直接登录进去
            # 如果换日了就会有公告
            self.ctl.loop_find_template_no_exception(
                template=images.HOMEPAGE_FREE,  # 有公告的时候会不是高光，所以需要降低阈值
                interval=1,
                timeout=60,
                threshold=0.6,
            )  # 动态判断是否登录进主页
            # 不管有没有公告，都当有公告处理
            self.ctl.touch_pos_multiple(
                pos=pos.HOMEPAGE_SAFE,
                interval=0.2,
                times=200,
            )
            # 操作就不保证再执行，只要在主页就行
            if self.assert_end():
                logger.success(f"Transaction {self.TXN_NAME} reboot success")
                return

            logger.error(f"Transaction {self.TXN_NAME} failed to reboot")
            raise TransactionRebootError


if __name__ == "__main__":
    pass
