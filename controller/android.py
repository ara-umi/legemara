#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import time
from typing import Any, Optional

import cv2
from airtest.core.android import Android
from airtest.core.api import G
from airtest.core.api import auto_setup
from airtest.core.cv import loop_find
from airtest.core.error import TargetNotFoundError, AdbError
from loguru import logger

from exceptions import TemplateNotFound
from models.android import DisplayInfo
from models.pos import DevPos
from models.template import DevTemplate
from settings import Settings


class AndroidController(object):

    def __init__(
            self,
            settings: Settings,
    ):
        airtest_logger = logging.getLogger("airtest")
        airtest_logger.setLevel(logging.ERROR)

        self.settings = settings
        self._setup_cli()
        self._device: Android = self._connect_device()
        self._display_info: DisplayInfo = self._get_display_info()
        logger.info(f"Display info: {self._display_info}")

    def _setup_cli(self) -> None:
        root: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        logger.info(f"Airtest root: {root}")
        auto_setup(root, logdir=self.settings.LOG_DIR)
        logger.info("Airtest CLI setup completed")

    def _connect_device(self) -> Android:
        try:
            device = Android(self.settings.DEVICE)
            device.cap_method = "Javacap"
            G.DEVICE = device
            logger.info(f"Connected to device {self.settings.DEVICE} successfully")
            return device
        except Exception as e:
            logger.error(f"Failed to connect to device {self.settings.DEVICE}, error: {e}")
            raise

    def _get_display_info(self) -> DisplayInfo:
        result: dict = self._device.get_display_info()
        display_info: DisplayInfo = DisplayInfo.model_validate(result)
        return display_info

    @property
    def device(self) -> Android:
        return self._device

    @property
    def display_info(self) -> DisplayInfo:
        return self._display_info

    def touch(
            self,
            pos: Any,
            duration: float = 0.1,
    ):
        """
        原生点击方法
        """
        self._device.touch(pos=pos, duration=duration)
        logger.info(f"Touch: {pos}")

    def touch_multiple(
            self,
            pos: Any,
            duration: float = 0.1,
            interval: float = 1.0,
            times: int = 1,
    ):
        for i in range(times):
            self._device.touch(pos=pos, duration=duration)
            time.sleep(interval)
        logger.info(f"Touch: {pos} {times} times, interval: {interval}")

    def touch_pos(
            self,
            pos: DevPos,
    ):
        """
        点击坐标
        做了分辨率适应，需要传入 DevPos 对象，一般会在 instance 下明确定义
        """
        real_pos = pos.adapt(self._display_info)
        self._device.touch(real_pos)
        logger.info(f"Touch pos: {pos}, real pos: {real_pos}")

    def touch_pos_multiple(
            self,
            pos: DevPos,
            interval: float = 1.0,
            times: int = 1,
    ):
        real_pos = pos.adapt(self._display_info)
        for i in range(times):
            self._device.touch(real_pos)
            time.sleep(interval)
        logger.info(f"Touch pos: {real_pos} {times} times, interval: {interval}")

    def loop_find_template(
            self,
            template: DevTemplate,
            threshold: float = 0.8,
            waiting: int = 1,
            interval: float = 1.0,
            timeout: int = 10,
    ) -> tuple:
        """
        循环查找模板
        如果查找到会返回原生坐标，如果没找到会抛出异常
        """
        time.sleep(waiting)
        try:
            pos = loop_find(
                query=template.template,
                timeout=timeout,
                threshold=threshold,
                interval=interval,
            )
            logger.info(f"Loop find template: {template}, pos: {pos}")
            return pos
        except TargetNotFoundError:
            logger.error(f"Loop find template: {template} failed")
            raise TemplateNotFound(template)

    def loop_find_template_no_exception(
            self,
            template: DevTemplate,
            threshold: float = 0.8,
            waiting: float = 1,
            interval: float = 1.0,
            timeout: float = 10,
    ) -> tuple[bool, Optional[tuple]]:
        """
        循环查找模板
        返回是否找到和原生坐标，不会抛出异常
        """
        time.sleep(waiting)
        try:
            pos = loop_find(
                query=template.template,
                timeout=timeout,
                threshold=threshold,
                interval=interval,
            )
            return True, pos
        except TargetNotFoundError:
            return False, None

    def type_text(self, text: str):
        """
        键盘键入方法
        """
        self._device.text(text)
        logger.info(f"Type text: {text}")

    def take_screenshot(
            self,
            save_path: str,
    ) -> bool:
        """
        截图并保存到指定路径
        不会抛出异常，失败时返回 False
        """
        try:
            # 获取当前屏幕截图
            screen = self._device.snapshot()
            # 确保保存路径的目录存在
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            # 保存截图到指定路径
            cv2.imwrite(save_path, screen)
            # 返回成功状态和文件路径
            return True
        except AdbError as e:
            logger.error(f"Failed to take screenshot: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error while taking screenshot: {e}")
            return False


if __name__ == "__main__":
    pass
