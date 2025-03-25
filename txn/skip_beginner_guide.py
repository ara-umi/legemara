#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

from loguru import logger

from exceptions import *
from instance import images
from instance import pos
from txn.base import LegecloTransaction


class SkipBeginnerGuide(LegecloTransaction):
    """
    第一次登录账号会进入新手引导，基本上除了引导让你点击的位置，其他位置点击都无效
    这个过程对应跳过引导，一直到跳过所有的公告，恢复到自由点击的状态
    """
    TXN_NAME = "SkipBeginnerGuide"

    def assert_start(self) -> bool:
        try:
            self.ctl.loop_find_template(
                template=images.BEGINNER_CONVERSATION,
                threshold=0.95,
                timeout=3,
            )
            logger.success(f"Transaction {self.TXN_NAME} start success")
            return True
        except TemplateNotFound:
            logger.error(f"Transaction {self.TXN_NAME} start failed")
            return False

    def assert_end(self) -> bool:
        """
        这个判断很难做很难做
        要把逻辑中心偏向于脚本一定要正常执行，公告一定要点完
        """
        try:
            self.ctl.loop_find_template(
                template=images.LIMITED_TIME_STORE,
                interval=1,
                timeout=2,
            )
            logger.success(f"Transaction {self.TXN_NAME} end success")
            time.sleep(3)
            return True
        except TemplateNotFound:
            logger.error(f"Transaction {self.TXN_NAME} end failed")
            return False

    def operate(self) -> None:
        """
        我不希望这里的逻辑出现任何图像检测的部分
        因为新手引导能点的位置是固定的，任何情况下只要还在新手引导，就都可以用重新点一遍的方式实现 recover
        """
        # 跳过对话框直到提示点击转蛋
        self.ctl.touch_pos_multiple(
            pos.HOMEPAGE_SAFE,
            interval=0.5,
            times=20,
        )  # 实际上点 3 次就够，多点没影响，可能会卡一下
        time.sleep(3)
        # 点击转蛋
        self.ctl.touch_pos(pos.HOMEPAGE_GACHA)
        time.sleep(5)  # 有可能有加载
        # 点击新手十连
        self.ctl.touch_pos(pos.BEGINNER_10X)
        time.sleep(3)
        # 点击确认
        self.ctl.touch_pos(pos.BEGINNER_10X_CONFIRM_OK)
        time.sleep(3)
        # 跳过抽取动画
        self.ctl.touch_pos_multiple(
            pos=pos.HOMEPAGE_SAFE,  # 点哪里都一样
            interval=0.2,
            times=80,
        )
        time.sleep(1)
        # 点击让你去强化的按钮
        self.ctl.touch_pos(pos.BEGINNER_10X_OVER_OK)
        time.sleep(5)  # 回退到主页，需要一点时间
        # 点击角色
        self.ctl.touch_pos(pos.HOMEPAGE_CHARACTER)
        time.sleep(3)
        # 点击主战角色
        self.ctl.touch_pos(pos.CHARACTER_MAIN)
        time.sleep(3)
        # 点击默认强化的第三个角色
        self.ctl.touch_pos(pos.THIRD_CHARACTER)
        time.sleep(2)  # 不切页面就可以快一点
        # 点击强化
        self.ctl.touch_pos(pos.CHAR_OVERVIEW_UPGRADE)
        time.sleep(4)  # 会切页面
        # 点击推荐素材
        self.ctl.touch_pos(pos.RECOMMENDED_MATERIALS)
        time.sleep(2)
        # 点击强化
        self.ctl.touch_pos(pos.RECOMMENDED_MATERIALS_CONFIRM)
        time.sleep(5)  # 会有个动画
        # 确认强化结果 OK
        self.ctl.touch_pos(pos.LEVEL_UP_OK)
        time.sleep(3)
        # 跳过一段对话后会回主页弹公告，疯狂点安全位置就行
        self.ctl.touch_pos_multiple(
            pos=pos.HOMEPAGE_SAFE,
            interval=0.2,
            times=200,
        )
        # 之后等待进入自由主页，逻辑交给 assert_end

    def recover_end(self) -> bool:
        time.sleep(10)
        logger.warning(f"Recover {self.TXN_NAME}")
        # 先尝试多次点击主页按钮，因为可能是广告没走完
        self.ctl.touch_pos_multiple(
            pos=pos.HOMEPAGE_HOMEPAGE,
            times=10,
            interval=0.5,
        )
        if self.assert_end():
            return True

        # 如果没效果，说明可能卡在了中间某一步，就从头再点一遍
        self.operate()
        # 点完再手动进主页
        self.ctl.touch_pos_multiple(
            pos=pos.HOMEPAGE_HOMEPAGE,
            times=10,
            interval=0.5,
        )
        # 返回，如果还不行就说明没办法
        return self.assert_end()

    def execute(self) -> None:
        can_start = self.assert_start()
        if not can_start:
            # 修复逻辑，暂时不知道怎么写，可能就只有等待，如果等待之后再不成功就 fatal
            pass
        self.operate()
        can_end = self.assert_end()
        if not can_end:
            # 再点一次
            can_recover = self.recover_end()
            if not can_recover:
                logger.error(f"Transaction {self.TXN_NAME} recover failed")
                raise ValueError(f"Transaction {self.TXN_NAME} failed")


if __name__ == "__main__":
    pass
