#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

from loguru import logger

from exceptions import *
from instance import images
from instance import pos
from txn.base import LegecloTransaction


class CollectGifts(LegecloTransaction):
    """
    从能自由点击的主页开始领取礼物，最终再回到主页
    """
    TXN_NAME = "CollectGifts"

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
        # 点击礼物箱
        self.ctl.touch_pos(pos.HOMEPAGE_GIFTS)
        time.sleep(5)  # 东西多可能会卡
        # 点击全部领取，一直点这里就行
        self.ctl.touch_pos_multiple(
            pos=pos.GIFTS_RECEIVE_ALL,
            interval=0.5,
            times=30,
        )  # 第一次领可能会卡
        # 点击主页
        self.ctl.touch_pos_multiple(
            pos=pos.HOMEPAGE_HOMEPAGE,
            interval=1,
            times=3,
        )
        # 之后逻辑交给 assert_end

    def recover_end(self) -> bool:
        time.sleep(10)
        logger.warning(f"Recover {self.TXN_NAME}")
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
                # 修复逻辑
                # 通过确保回到主页来跳过这一步
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
            # 反正 recover 逻辑里都没保证操作再执行，理论上这里再执行也没问题
            if self.assert_end():
                logger.success(f"Transaction {self.TXN_NAME} reboot success")
                return

            logger.error(f"Transaction {self.TXN_NAME} failed to reboot")
            raise TransactionRebootError


if __name__ == "__main__":
    pass
