#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import time

from loguru import logger

from exceptions import *
from instance import images
from instance import pos
from models.pos import DevPos
from txn.base import LegecloTransaction
from utils.account import create_erolabs_account
from utils.slider import process_erolabs_slider


class LoginToHomepage(LegecloTransaction):
    """
    从登录页面开始，保证点击 GAME START 后直接跳转进入取名
        只要之前删除过账号一次，就可以永久跳过 erolabs 黑端登录界面
    之后执行取名、确认跳过新手教程，到达主页（主页会立刻跳出剩余的新手教程，除了指定按钮其他位置都非高光）

    凡是涉及到进 erolabs 黑端的逻辑，用的模拟器设备都要打开平板模式
    实现的效果是 erolabs 黑端就中间一条，如果用手机模式可能会有变化
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

    def _create_account(self) -> None:
        """
        创建账号
        会抛出异常
        """
        # 识别 EROLABS 注册新账号
        find, _pos = self.ctl.loop_find_template_no_exception(
            template=images.NO_EROLABS_ACCOUNT,
            interval=1,
            timeout=60,
        )
        if not find:
            raise TransactionRecoverError("Erolabs account register error, need reboot to solve")
        time.sleep(2)
        # 点击注册新账号
        self.ctl.touch(_pos)
        time.sleep(2)
        # 输入账号密码
        account = create_erolabs_account()
        logger.info(f"Create account: {account}")
        self.ctl.touch_pos(pos.EROLABS_REGISTER_EMAIL_INPUT)
        time.sleep(1)
        self.ctl.type_text(account.email)
        time.sleep(1)
        self.ctl.touch_pos(pos.EROLABS_REGISTER_PASSWORD_INPUT)
        time.sleep(1)
        self.ctl.type_text(account.password)
        time.sleep(1)
        self.ctl.touch_pos(pos.EROLABS_REGISTER_PASSWORD_INPUT_AGAIN)
        time.sleep(1)
        self.ctl.type_text(account.password)
        time.sleep(1)
        # 点击安全位置取消输入状态
        self.ctl.touch_pos(pos.EROLABS_REGISTER_SAFE)
        time.sleep(1)
        # 下滑滚轮
        self.ctl.scroll(
            start_pos=pos.EROLABS_REGISTER_SCROLL_START,
            end_pos=pos.EROLABS_REGISTER_SCROLL_END,
            steps=50,
        )

        register_success: bool = False
        # 滑动验证码
        for _ in range(10):  # 避免死循环
            image = self.ctl.capture_region(
                top_left=pos.EROLABS_REGISTER_SLIDER_TOP_LEFT,
                bottom_right=pos.EROLABS_REGISTER_SLIDER_BOTTOM_RIGHT,
            )
            x = process_erolabs_slider(image)
            if not x:
                # 检测不出来就拖到死，让它自动刷新
                x = 300

            # 写死在这里得了
            # 这里没去检测那个箭头，直接记录了位置
            # 不同页面在都拖到底的情况下箭头的位置都可能不一样
            # 所以干脆就写在这里
            start_pos = DevPos(
                x=671,
                y=496,
                description="滑动验证码起始位置，箭头的中心",
            )
            end_pos = DevPos(
                x=671 + x,
                y=496,
            )
            self.ctl.scroll(
                start_pos=start_pos,
                end_pos=end_pos,
                duration=1,
                steps=300,
            )
            time.sleep(1)

            # 检测是否有可以注册的按键
            find, _pos = self.ctl.loop_find_template_no_exception(
                template=images.EROLABS_CAN_REGISTER,
                interval=1,
                timeout=15,  # 有可能会卡
            )
            if find:
                register_success = True
                self.ctl.touch(_pos)
                time.sleep(1)
                # 会直接跳到账号登录界面
                break

        if not register_success:
            raise TransactionRecoverError("Erolabs account register error, need reboot to solve")

        # 登入逻辑

    def operate(self) -> None:
        # 点击 GAME START
        self.ctl.touch_pos(pos.GAME_START)
        # 进入起名界面
        self.ctl.loop_find_template_no_exception(
            template=images.NAME_RULE,
            interval=1,
            timeout=120,  # 会直接跑加载条，可能花费很长时间
        )  # 点击 GAME START 成功，哪怕找不到也不抛出异常，仅用于脚本提速
        time.sleep(0.5)
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
        # 检测弹出输入邀请码（不确定是不是会常驻）
        self.ctl.loop_find_template_no_exception(
            template=images.INPUT_INVITE_CODE,
            timeout=30,  # 可能需要花费一定时间
        )
        # 点击跳过邀请码
        self.ctl.touch_pos(pos.SKIP_INVITE_CODE)
        # 检测弹出跳过新手教程提示
        self.ctl.loop_find_template_no_exception(
            template=images.IF_SKIP_BEGINNER,
            timeout=30,  # 可能需要花费一定时间
        )
        time.sleep(2)
        # 点击跳过新手教程
        self.ctl.touch_pos(pos.SKIP_BEGINNER)
        # 之后等待进入主页，逻辑交给 assert_end

    def execute(self) -> None:
        try:
            can_start = self.assert_start()
            if not can_start:
                # 修复逻辑，暂时不知道怎么写，可能就只有等待，如果等待之后再不成功就 fatal
                pass
            self.operate()
            can_end = self.assert_end()
            if not can_end:
                # 理论上这里就是没登录进游戏
                # 可能的情况是，登录卡太久超时了，或者中间哪里点快了，或者其他情况（id 都是数字，一定合法）
                # 能处理的激素登录卡太久超时，我能再等待一会
                # 点快了都很难处理，只能通过代码逻辑保证不会出现这种情况，出现之后我是不知道卡在哪里的，是没有简单统一的办法可以回到登录界面的
                # 所以这里逻辑上只处理超时
                time.sleep(30)
                can_end = self.assert_end()
                if not can_end:
                    logger.warning(f"Transaction {self.TXN_NAME} failed to recover")
                    raise TransactionRecoverError("Transaction failed to recover")
        except TransactionRecoverError:
            logger.warning(f"Transaction {self.TXN_NAME} failed to recover, rebooting...")
            self.ctl.reboot_legeclo()  # 重启游戏
            # 之后我无法确定之前是起名成功还是失败，所以无法知道会直接进主页还是跳起名框
            # 只要能进主页，就会直接继续新手教程，不用考虑换日弹公告的事情，因为新手教程还没跳过
            time.sleep(3)
            # 点击 GAME START
            self.ctl.touch_pos(pos.GAME_START)
            if self.assert_end():  # 直接就进去了，
                logger.success(f"Transaction {self.TXN_NAME} reboot success")
                return

            # 不能直接进去，说明弹了起名框，那就继续走一遍流程
            # 流程里会再点一次 GAME START，对执行没有影响
            self.operate()
            can_end = self.assert_end()
            if not can_end:
                logger.error(f"Transaction {self.TXN_NAME} failed to reboot")
                raise TransactionRebootError


if __name__ == "__main__":
    pass
