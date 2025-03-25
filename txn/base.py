#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC
from functools import wraps

from controller.legeclo import LegecloController
from txn.interface import TransactionInterface


def with_reboot(func):
    """
    在 transaction 执行出现异常并且无法自我恢复的时候的终极处理方案
    打开模拟器的多任务视图，关闭掉所有应用，然后重启启动传奇四叶草，重新登录并重新执行该 transaction

    如何定义异常无法自我恢复：一般是 app 闪退/网络断连/换日
        理论上这些情况都可以分开讨论甚至有单独的检测或者处理方法
        但实际上它们发生的情况是少数，我更需要一个能适应更多情况的/能一定保证解决的处理方式，哪怕它执行效率低，但开发效率高
    不能解决哪些情况：模拟器崩溃/adb 崩溃/网络崩溃等
    仍然存在问题：我无法保证严格意义上它能完全恢复到上一步的动作
        有些 transaction 在游戏重启之后还能不能通过继续从头执行一遍点击操作来顺利完成我是不知道的
        我无法遇见产生的每个细微的变化和隐藏的 bug，一切都等待调试
        reboot 中产生的异常会直接抛出导致程序停止

    这里写这个装饰器是为了写上面的文档，代码中的逻辑我偏向不使用装饰器，有地方可能没办法复用，而且会降低可读性
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            pass

    return wrapper


class LegecloTransaction(TransactionInterface, ABC):

    def __init__(
            self,
            controller: LegecloController,
    ):
        self.ctl = controller


if __name__ == "__main__":
    pass
