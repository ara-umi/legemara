#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

from loguru import logger

from controller.android import AndroidController
from instance import images
from instance import pos
from settings import Settings

"""
思想

思想是程序的灵魂，孔子说：要有思想

这个脚本要正常跑一遍，不难，难的是一直跑
就像造一辆车，上路一天不出事情，不难，跑十万公里不出事情，难
单次执行过程中出现的问题，无非就是延迟时间没调好，调一调又能跑
但当重复执行的时候，会出现非常随机的网络波动问题甚至是断网，包括日期变更的时候也会强制踢回登录界面
要解决这些问题才是最难的

把整个脚本过程拆解成一个一个的小阶段
把每个小阶段看作一个事务，只有在小阶段的操作全部执行完成时才做检测，期间不做检测
当检测发现该小阶段未正常运行的时候，应该提供简单的恢复方法
比如对于简单的点击的事务，最简单的方法就是直接重新点一遍
当整个事务不能在期间任何一个时段都通过 *从头到尾再点一遍* 来确保二次执行时，那么就尝试恢复到任务的初始状态，再点一遍
当整个事务无法回到初始状态，或者再点一遍回出现不可预料的结果的时候，那么就尝试跳过该事务
如果跳过该事务将造成后续事务无法执行的时候，那么就尝试执行用于结束循环的事务来中止本次循环，比如直接消除账号
当以上的方法都无法解决的时候，就尝试通过最简单的关闭程序并重启，来实现恢复到初始状态
当哪怕重启都无法恢复初始状态的时候，就尝试维护一个状态机，记录状态并在下次启动时继续执行
不考虑解决更深的问题，解决模拟器崩溃的难度基本上和解决小区停电的难度一样高了

一切异常处理都是保险绳，代码的重点不是在写健全的异常处理逻辑，而是保证尽可能不出异常
"""


class LegecloController(AndroidController):
    """
    用于写一些封装好的专用于传奇四叶草的方法
    如你所见，我什么也没写，相当于冗余设计了
    """

    def __init__(
            self,
            settings: Settings,
    ):
        super().__init__(settings=settings)

    def close_all_apps(self):
        """
        切出多任务试图并清楚全部 app（相当于把传草关了，单独要找传奇四叶草在哪里还挺麻烦的，反正不会开其他应用）
        仅用于蓝叠模拟器
        不同模拟器用的安卓版本可能不一样
        我都不能保证 keyevent 能实现出一样的效果，就更别提保证 UI 一致了
        """
        self.app_switch()
        time.sleep(2)
        self.touch_pos(pos.CLOSE_ALL_APPS)  # 清理完会自动退回桌面
        time.sleep(1)
        logger.success("Close all apps")

    def start_legeclo(self):
        """
        从桌面启动传奇四叶草
        找不到会直接报错，超时启动失败也会报错
        """
        _pos = self.loop_find_template(
            template=images.LEGECLO_APP_ICON,
            timeout=0,
        )
        self.touch(_pos)
        time.sleep(10)
        self.loop_find_template(
            template=images.LOGIN_PAGE_SYMBOL,
            interval=3,
            timeout=120,
        )
        logger.success("Start Legeclo")

    def reboot_legeclo(self):
        """
        重启传奇四叶草
        """
        self.close_all_apps()
        time.sleep(3)
        self.start_legeclo()


if __name__ == "__main__":
    pass
