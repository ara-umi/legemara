#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

from loguru import logger

from exceptions import *
from instance import images
from instance import pos
from models.pos import DevPos
from txn.base import LegecloTransaction

"""
已经变成面条代码了，就放这里当摆设吧
"""


class Gacha(LegecloTransaction):
    """
    通用转蛋，更多的是当一个模板来用
    从能自由点击的主页开始抽卡，最终回到主界面
    """
    TXN_NAME = "Gacha"

    def __init__(
            self,
            ctl,
            gacha_pool_pos: DevPos = pos.GACHA_POOL3,
    ):
        super(Gacha, self).__init__(ctl)
        self.gacha_pool_pos = gacha_pool_pos

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
        # 点击转蛋
        self.ctl.touch_pos(pos.HOMEPAGE_GACHA)
        time.sleep(5)  # 有可能有加载
        # 切到要抽的池子
        self.ctl.touch_pos(self.gacha_pool_pos)
        time.sleep(3)
        # 点击免费钻抽 10 次（我很怕不同扭蛋位置不一样）
        self.ctl.touch_pos(pos.GACHA_10X)
        time.sleep(3)
        # 点击确认
        self.ctl.touch_pos(pos.GACHA_CONFIRM_OK)
        time.sleep(3)
        # 点击 skip
        self.ctl.touch_pos_multiple(
            pos=pos.GACHA_SKIP,
            interval=0.2,
            times=80,
        )

        def _loop_gacha():
            """
            起始位置是一次抽取完成后的位置，会有抽取结果和继续抽的按钮
            """
            loop: int = 1
            # 做个简单的提速，基本上会越抽越快
            skip_click_times: int = 80
            skip_click_times_decrease: int = 10
            skip_click_times_min: int = 40

            while True:
                # 点击继续抽 10 次
                self.ctl.touch_pos(pos.GACHA_RESULT_10X)
                time.sleep(2)
                insufficient_funds, _ = self.ctl.loop_find_template_no_exception(
                    template=images.INSUFFICIENT_FUNDS,
                    timeout=2,
                    threshold=0.95,
                )
                if insufficient_funds:
                    return

                else:
                    # 确认
                    self.ctl.touch_pos(pos.GACHA_CONFIRM_OK)
                    time.sleep(3)
                    # 点击 skip
                    skip_click_times -= skip_click_times_decrease
                    this_skip_click_times = max(skip_click_times, skip_click_times_min)
                    self.ctl.touch_pos_multiple(
                        pos=pos.GACHA_SKIP,
                        interval=0.15,  # 调小了一点
                        times=this_skip_click_times,
                    )
                    loop += 1

        _loop_gacha()
        # logger.success("Insufficient funds, stop gacha")
        # 点击两次主页按钮，第一次退出魔晶石不足提示，第二次回到主页
        # 这里直接设置点击多次就行
        self.ctl.touch_pos_multiple(
            pos=pos.HOMEPAGE_HOMEPAGE,
            times=5,
            interval=1,
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
                logger.error(f"Transaction {self.TXN_NAME} recover failed")
                raise ValueError(f"Transaction {self.TXN_NAME} failed")


if __name__ == "__main__":
    pass
