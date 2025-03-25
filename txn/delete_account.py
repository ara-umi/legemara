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
                # 修复逻辑，很麻烦，因为可能删除成功可能没成功
                # 比如到了删除账号成功点 OK 这一步就已经是删除成功了，其他位置点击是没反应的
                # 我建议直接抛出异常，让重启逻辑来判断
                raise TransactionRecoverError(f"Transaction {self.TXN_NAME} failed to recover")
        except TransactionRecoverError:
            logger.warning(f"Transaction {self.TXN_NAME} failed to recover, rebooting...")
            self.ctl.reboot_legeclo()  # 重启游戏
            time.sleep(3)
            # 点击 GAME START
            self.ctl.touch_pos(pos.GAME_START)
            # 能不能登录进去就要靠检测是否弹出了起名的窗口
            if self.ctl.loop_find_template_no_exception(
                    template=images.NAME_RULE,
                    interval=1,
                    timeout=60,
                    threshold=0.9,
            ):
                # 这里说明已经删除成功了
                # 取消起名窗口
                self.ctl.touch_pos(pos.Name_INPUT_CANCEL)
                time.sleep(3)
                # 这里就不用 assert_end 了，没影响，哪怕不取消起名，下一个 loop 也不会有影响
                logger.success(f"Transaction {self.TXN_NAME} reboot success")
                return

            # 如果能登录进去，重新删一遍
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
            # 从头删一遍
            self.operate()
            if self.assert_end():
                logger.success(f"Transaction {self.TXN_NAME} reboot success")
                return

            logger.error(f"Transaction {self.TXN_NAME} failed to reboot")
            raise TransactionRebootError


if __name__ == "__main__":
    pass
