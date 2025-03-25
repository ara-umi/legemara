#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

from loguru import logger

from exceptions import *
from instance import images
from instance import pos
from txn.base import LegecloTransaction


class GachaDC2(LegecloTransaction):
    """
    初音岛第二期联动专属转蛋
    从能自由点击的主页开始抽卡，最终回到主界面
    涉及的逻辑在里面写死
    """
    TXN_NAME = "GachaDC2"

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
        # 用于 skip 加速
        skip_click_times: int = 80
        skip_click_times_decrease: int = 10
        skip_click_times_min: int = 40

        ##############################
        # 抽白嫖十连
        ##############################
        # 点击转蛋
        self.ctl.touch_pos(pos.HOMEPAGE_GACHA)
        time.sleep(5)  # 有可能有加载

        # 白嫖十连在第一个位置（后续如果有更新再调整，位置可能有变动）
        self.ctl.touch_pos(pos.GACHA_POOL1)
        time.sleep(3)
        # 点击白嫖抽 10 次
        self.ctl.touch_pos(pos.FREE_10X)
        time.sleep(3)
        # 点击确认
        self.ctl.touch_pos(pos.GACHA_CONFIRM_OK)
        time.sleep(3)
        # 点击 skip
        self.ctl.touch_pos_multiple(
            pos=pos.GACHA_SKIP,
            interval=0.2,
            times=max(skip_click_times, skip_click_times_min),
        )
        skip_click_times -= skip_click_times_decrease  # 抽一次十连扣一下
        # 循环抽卡至力竭
        while True:
            # 白嫖十连如果不能抽了就不会有抽 10 次的按钮
            can_gacha, _pos = self.ctl.loop_find_template_no_exception(
                template=images.GACHA_RESULT_10X,
                timeout=2,
                threshold=0.95,
            )
            if not can_gacha:
                break
            # 点击抽 10 次
            self.ctl.touch(_pos)
            time.sleep(2)
            # 确认
            self.ctl.touch_pos(pos.GACHA_CONFIRM_OK)
            time.sleep(3)
            # 点击 skip
            self.ctl.touch_pos_multiple(
                pos=pos.GACHA_SKIP,
                interval=0.15,
                times=max(skip_click_times, skip_click_times_min),
            )
            skip_click_times -= skip_click_times_decrease

        # 退出位置在只有返回的白嫖池结果处，这里加个逻辑回到转蛋主页面
        self.ctl.touch_pos(pos.HOMEPAGE_GACHA)
        time.sleep(3)

        ##############################
        # 抽联动自选
        ##############################
        # 点击转蛋（无论在哪里都可以通过这种方式回到抽卡主页面）
        self.ctl.touch_pos(pos.HOMEPAGE_GACHA)
        time.sleep(3)  # 前面有点击过，这里就可以快点

        # 联动池子在第三个（至少目前在）
        self.ctl.touch_pos(pos.GACHA_POOL3)
        time.sleep(3)
        # 点击选择精选角色
        self.ctl.touch_pos(pos.GACHA_SELECT_CHARACTERS)
        time.sleep(2)
        # 点击联动武尊
        self.ctl.touch_pos(pos.GACHA_SELECT_CHARACTERS_1_1)
        time.sleep(2)
        # 点击选择
        self.ctl.touch_pos(pos.GACHA_SELECT_CHARACTERS_CONFIRM_SELECT)
        time.sleep(2)
        # 点击联动乌列尔
        self.ctl.touch_pos(pos.GACHA_SELECT_CHARACTERS_1_3)
        time.sleep(2)
        # 点击选择
        self.ctl.touch_pos(pos.GACHA_SELECT_CHARACTERS_CONFIRM_SELECT)
        time.sleep(2)
        # 点击 OK
        self.ctl.touch_pos(pos.GACHA_SELECT_CHARACTERS_OK)
        time.sleep(2)
        # 二度确认 OK
        self.ctl.touch_pos(pos.GACHA_SELECT_CHARACTERS_CONFIRM_OK)
        time.sleep(3)  # 池子会变，就会有抽卡按钮了

        # 点击免费钻抽 10 次
        self.ctl.touch_pos(pos.GACHA_SELECTED_10X)
        time.sleep(3)
        # 点击确认
        self.ctl.touch_pos(pos.GACHA_CONFIRM_OK)
        time.sleep(3)
        # 点击 skip
        self.ctl.touch_pos_multiple(
            pos=pos.GACHA_SKIP,
            interval=0.2,
            times=max(skip_click_times, skip_click_times_min),
        )
        skip_click_times -= skip_click_times_decrease
        # 循环抽卡至力竭
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
                break
            else:
                # 确认
                self.ctl.touch_pos(pos.GACHA_CONFIRM_OK)
                time.sleep(3)
                # 点击 skip
                self.ctl.touch_pos_multiple(
                    pos=pos.GACHA_SKIP,
                    interval=0.15,
                    times=max(skip_click_times, skip_click_times_min),
                )
                skip_click_times -= skip_click_times_decrease

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
