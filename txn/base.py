#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC

from controller.legeclo import LegecloController
from txn.interface import TransactionInterface


class LegecloTransaction(TransactionInterface, ABC):

    def __init__(
            self,
            controller: LegecloController,
    ):
        self.ctl = controller


if __name__ == "__main__":
    pass
