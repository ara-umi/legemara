#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


class TransactionInterface(ABC):

    @abstractmethod
    def assert_start(self) -> bool:
        """
        判断一个执行阶段在开始执行时是否处于正确的执行位置
        """
        pass

    @abstractmethod
    def assert_end(self) -> bool:
        """
        判断一个执行阶段在结束执行时是否达到正确的执行效果
        """
        pass

    @abstractmethod
    def operate(self) -> None:
        """
        需要执行的操作
        我不希望在执行过程中非控件问题抛出任何异常，这会增大 recover 的难度
        """
        pass

    @abstractmethod
    def execute(self) -> None:
        """
        整个执行流程
        """
        pass


if __name__ == "__main__":
    pass
