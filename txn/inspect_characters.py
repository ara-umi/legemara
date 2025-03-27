#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import time

import numpy as np
from loguru import logger

from exceptions import *
from instance import images
from instance import pos
from models.template import CharacterPortrait
from txn.base import LegecloTransaction


class InspectCharacters(LegecloTransaction):
    """
    从能自由点击的主页开始，进入角色界面，检测有哪些角色
    评分大于等于 target_score 算刷取成功
    """
    TXN_NAME = "InspectCharacters"

    def __init__(
            self,
            ctl,
            save_dir: str = "./result",
            required_main_char: list[CharacterPortrait] = None,
            required_sub_char: list[CharacterPortrait] = None,
            must_have_main_char: list[CharacterPortrait] = None,
            must_have_sub_char: list[CharacterPortrait] = None,
            target_score: int = 1,  # 稍稍大于 0 而让如果没有获取到必须的角色则不通过评分检测
    ):
        """
        must have 中的角色一定要存在，否则评分为 -np.inf
        required 中的角色表示全部参与统计分数的角色，要包含 must have 中的角色，计分只会在 required 中的角色中进行
        没办法做到检测全部的角色，整个过程不如丢到截图后另开脚本处理，同时也需要全部角色的模板
        """
        super(InspectCharacters, self).__init__(ctl)
        self.save_dir = save_dir

        if not required_main_char:
            self.required_main_char = []
        else:
            self.required_main_char = required_main_char

        if not required_sub_char:
            self.required_sub_char = []
        else:
            self.required_sub_char = required_sub_char

        if not must_have_main_char:
            self.must_have_main_char = []
        else:
            self.must_have_main_char = must_have_main_char

        if not must_have_sub_char:
            self.must_have_sub_char = []
        else:
            self.must_have_sub_char = must_have_sub_char

        self.target_score = target_score

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

    def _inspect_main(
            self,
            filename: str = None
    ):
        """
        检测战角色并且返回评分
        这个逻辑是建立在已经进入默认的主战总览上的
        理论上还要再加个点击角色总览的主战键会更好
        如果 must_have_main_char 没有获取到，则返回 -np.inf
        如果沒有传入 filename 会自动生成
        """
        # 点击显示条件
        self.ctl.touch_pos(pos.CHARACTER_FILTER_BY)
        time.sleep(3)
        # 只看 SSR
        self.ctl.touch_pos(pos.CHARACTER_FILTER_BY_RARE_SSR)
        time.sleep(3)
        # 点击 OK
        self.ctl.touch_pos(pos.CHARACTER_FILTER_BY_CONFIRM_OK)
        time.sleep(3)
        # 不一定会真 OK，因为如果没有 SSR 这里会是灰的
        # 这里再点一下关闭显示条件，如果已经触发了 OK，点这里也不会有影响
        self.ctl.touch_pos(pos.CHARACTER_FILTER_BY_CLOSE)
        time.sleep(3)

        # 开始评分
        score: float = 0
        check_required: bool = True  # must have 都没有就可以直接跳过 required 的检测，直接到解雇
        for char in self.must_have_main_char:
            find, _ = self.ctl.loop_find_template_no_exception(
                template=char,
                timeout=0,
                interval=1,
            )
            if not find:
                logger.warning(f"Character {char.name} not found")
                score = -np.inf
                check_required = False

        if check_required:
            for char in self.required_main_char:
                find, _ = self.ctl.loop_find_template_no_exception(
                    template=char,
                    timeout=0,
                    interval=1,
                )
                if find:
                    logger.success(f"Character {char.name} found, score +{char.score}")
                    score += char.score

        # 截图保存
        if not filename:
            dt = datetime.datetime.now().strftime("%m%d_%H_%M")
            filename = f"{dt}_main.png"
        save_path = f"{self.save_dir}/{filename}"
        self.ctl.take_screenshot(save_path=save_path)

        return score

    def _inspect_sub(
            self,
            filename: str = None
    ):
        """
        检测后援角色并且返回评分
        这个逻辑是建立在已经进入默认的角色总览上的
        如果 must_have_sub_char 没有获取到，则返回 -np.inf
        如果沒有传入 filename 会自动生成
        """
        # 点击后援
        self.ctl.touch_pos(pos.CHARACTER_OVERVIEW_SUP)
        time.sleep(3)
        # 点击显示条件
        self.ctl.touch_pos(pos.CHARACTER_FILTER_BY)
        time.sleep(3)
        # 检查下 SSR 是否勾上，这里可能勾上可能没勾上，没主战 SSR 这里就没勾上，单独跑也没勾上
        ssr_active, _ = self.ctl.loop_find_template_no_exception(
            template=images.FILTER_BY_RARE_SSR_ACTIVE,
            timeout=1,
            threshold=0.95,
        )
        if not ssr_active:
            # 只看 SSR
            self.ctl.touch_pos(pos.CHARACTER_FILTER_BY_RARE_SSR)
            time.sleep(3)
        # 点击 OK
        self.ctl.touch_pos(pos.CHARACTER_FILTER_BY_CONFIRM_OK)
        time.sleep(3)
        # 不一定会真 OK，因为如果没有 SSR 这里会是灰的
        # 这里再点一下关闭显示条件，如果已经触发了 OK，点这里也不会有影响
        self.ctl.touch_pos(pos.CHARACTER_FILTER_BY_CLOSE)
        time.sleep(3)

        # 开始评分
        score: float = 0
        check_required: bool = True  # must have 都没有就可以直接跳过 required 的检测，直接到解雇
        for char in self.must_have_sub_char:
            find, _ = self.ctl.loop_find_template_no_exception(
                template=char,
                timeout=0,
                interval=1,
            )
            if not find:
                logger.warning(f"Character {char.name} not found")
                score = -np.inf
                check_required = False

        if check_required:
            for char in self.required_sub_char:
                find, _ = self.ctl.loop_find_template_no_exception(
                    template=char,
                    timeout=0,
                    interval=1,
                )
                if find:
                    logger.success(f"Character {char.name} found, score +{char.score}")
                    score += char.score

        # 截图保存
        if not filename:
            dt = datetime.datetime.now().strftime("%m%d_%H_%M")
            filename = f"{dt}_sup.png"
        save_path = f"{self.save_dir}/{filename}"
        self.ctl.take_screenshot(save_path=save_path)

        return score

    def operate(self) -> bool:
        """
        会返回是否满足 target_score 的 bool
        后续要调整返回，看需不需要返回获取到的角色列表等
        """
        # 点击角色
        self.ctl.touch_pos(pos.HOMEPAGE_CHARACTER)
        time.sleep(3)
        # 点击主战
        self.ctl.touch_pos(pos.CHARACTER_MAIN)
        time.sleep(3)

        # 计算分数
        dt = datetime.datetime.now().strftime("%m%d_%H_%M")
        score_main = self._inspect_main(filename=f"{dt}_main.png")
        score_sub = self._inspect_sub(filename=f"{dt}_sub.png")
        score = score_main + score_sub
        logger.success(
            f"Main score: {score_main}, sub score: {score_sub}, score: {score}, target score: {self.target_score}")
        if score >= self.target_score:
            logger.success(f"Meet target score, got score: {score}, target score: {self.target_score}")
            marathon_success = True
        else:
            marathon_success = False

        # 退出到主页，这里直接设置点击多次就行
        self.ctl.touch_pos_multiple(
            pos=pos.HOMEPAGE_HOMEPAGE,
            times=2,
            interval=1,
        )
        # 之后逻辑交给 assert_end
        return marathon_success

    def recover_end(self) -> bool:
        time.sleep(10)
        logger.warning(f"Recover {self.TXN_NAME}")
        self.ctl.touch_pos_multiple(
            pos=pos.HOMEPAGE_HOMEPAGE,
            times=10,
            interval=1,
        )
        return self.assert_end()

    def execute(self) -> bool:
        try:
            can_start = self.assert_start()
            if not can_start:
                # 修复逻辑，暂时不知道怎么写，可能就只有等待，如果等待之后再不成功就 fatal
                pass
            marathon_success = self.operate()
            can_end = self.assert_end()
            if not can_end:
                # 修复逻辑
                # 通过确保回到主页来跳过这一步
                can_recover = self.recover_end()
                if not can_recover:
                    logger.warning(f"Transaction {self.TXN_NAME} failed to recover")
                    raise ValueError(f"Transaction {self.TXN_NAME} failed to recover")

            return marathon_success

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
            # 是否刷取成功就当 False
            if self.assert_end():
                logger.success(f"Transaction {self.TXN_NAME} reboot success")
                return False

            logger.error(f"Transaction {self.TXN_NAME} failed to reboot")
            raise TransactionRebootError


if __name__ == "__main__":
    pass
