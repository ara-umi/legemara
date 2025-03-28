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
        """
        逻辑上要注意不能在弹出断连或者换日时一直卡在抽卡循环里
        不可能时时刻刻检测有没有弹窗，最好办法就是把规定个抽卡次数上限，自动退出
        对于免费转蛋还好办，因为是否继续抽的逻辑是检测 *有继续抽的按钮*
        这个按钮呗弹窗挡住，就会自动退出
        但对于用免费钻抽的池子，是否继续抽的逻辑是检测 *没用跳出魔晶石不足*
        有弹窗遮挡就会死循环
        所以规定了个抽卡次数上限来避免这种情况
        """
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
        # 循环抽卡，设置个最大循环次数避免死循环
        for _ in range(10):
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

        # 这里根据脚本的运行时间是需要修改的，要么就引入图片识别的逻辑
        # 在抽完免费十连池子后，免费十连池会直接消失，联动池变为第一个
        self.ctl.touch_pos(pos.GACHA_POOL1)
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
        # 循环抽卡，设置个最大循环次数避免死循环
        for _ in range(10):
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
