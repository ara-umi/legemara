#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import time

from loguru import logger

from controller.legeclo import LegecloController
from instance import characters
from settings import get_settings
from txn import (
    LoginToHomepage,
    SkipBeginnerGuide,
    DeleteAccount,
    SkipStage,
    CollectGifts,
    CollectTasks,
    InspectCharacters,
)
from txn.gacha_dc2 import GachaDC2

airtest_logger = logging.getLogger("airtest")
airtest_logger.setLevel(logging.DEBUG)

settings = get_settings()
controller = LegecloController(
    settings=settings,
)

"""
一些配置要做到 settings 里，这里没敲定，就先代码里搓
"""

login_to_homepage_txn = LoginToHomepage(controller)
skip_beginner_guide_txn = SkipBeginnerGuide(controller)
skip_stage_txn = SkipStage(controller)
collect_gifts_txn = CollectGifts(controller)
collect_tasks_txn = CollectTasks(controller)
gacha_txn = GachaDC2(
    controller,
)
inspect_characters_txn = InspectCharacters(
    controller,
    required_main_char=[
        characters.联动武尊,

        characters.卑,
        characters.新米,
        characters.枪南丁,
        characters.红神,
        characters.蓝神,
        characters.绿神,
        characters.阿波罗,
        characters.飞索,
        characters.霍恩海姆,
    ],
    required_sub_char=[
        characters.联动乌列尔,

        characters.女仆,
    ],
    must_have_main_char=[
        characters.联动武尊,
    ],
    must_have_sub_char=[
        characters.联动乌列尔,
    ],
    # 目前评分标准是按满分 100 来算，联动限定 100 分，重要常驻 100 分，其他低于 100
    target_score=320,
)
delete_account_txn = DeleteAccount(controller)


def once():
    start_time = time.time()
    login_to_homepage_txn.execute()
    skip_beginner_guide_txn.execute()
    skip_stage_txn.execute()
    collect_gifts_txn.execute()
    collect_tasks_txn.execute()
    gacha_txn.execute()

    success = inspect_characters_txn.execute()
    if success:  # 刷取成功的逻辑
        end_time = time.time()
        logger.success(f"Once end, cost {end_time - start_time:.2f} seconds")
        return

    delete_account_txn.execute()
    end_time = time.time()
    logger.success(f"Once end, cost {end_time - start_time:.2f} seconds")


def marathon():
    loop: int = 1
    while True:
        start_time = time.time()
        logger.success(f"Marathon loop {loop} start")
        login_to_homepage_txn.execute()
        skip_beginner_guide_txn.execute()
        skip_stage_txn.execute()
        collect_gifts_txn.execute()
        collect_tasks_txn.execute()
        gacha_txn.execute()

        success = inspect_characters_txn.execute()
        if success:  # 刷取成功的逻辑
            pass

        delete_account_txn.execute()
        end_time = time.time()
        logger.success(f"Marathon loop {loop} end, cost {end_time - start_time:.2f} seconds")
        loop += 1
        time.sleep(10)


if __name__ == "__main__":
    # once()
    marathon()
