#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Optional

from models.android import DisplayInfo
from models.base import DEVELOP_DISPLAY_INFO


class DevPos(object):

    def __init__(
            self,
            x: float,
            y: float,
            display_info: Optional[DisplayInfo] = None,
            description: str = "",
    ):
        self.x = x
        self.y = y
        if not display_info:
            self.display_info = DEVELOP_DISPLAY_INFO
        else:
            self.display_info = display_info
        self.description = description

    def __str__(self):
        return f"x={self.x}, y={self.y}, description={self.description}"

    def adapt(
            self,
            target: DisplayInfo
    ) -> tuple[float, float]:
        """
        将 DevPos 坐标从当前 display_info 适配到目标 display_info
        返回坐标元组用于 touch

        似乎 density 不影响坐标适配
        """
        # original_width = self.display_info.width
        # original_height = self.display_info.height
        # original_density = self.display_info.density
        #
        # target_width = target.width
        # target_height = target.height
        # target_density = target.density
        #
        # width_ratio = target_width / original_width
        # height_ratio = target_height / original_height
        # density_ratio = target_density / original_density
        #
        # adapted_x = self.x * width_ratio * density_ratio
        # adapted_y = self.y * height_ratio * density_ratio
        #
        # # 精确到小数点后一位
        # adapted_x = round(adapted_x, 1)
        # adapted_y = round(adapted_y, 1)
        #
        # return adapted_x, adapted_y

        # 原始设备分辨率
        original_width = self.display_info.width
        original_height = self.display_info.height

        # 目标设备分辨率
        target_width = target.width
        target_height = target.height

        # 计算宽高比例(不考虑density)
        width_ratio = target_width / original_width
        height_ratio = target_height / original_height

        # 适配坐标
        adapted_x = self.x * width_ratio
        adapted_y = self.y * height_ratio

        # 精确到小数点后一位
        adapted_x = round(adapted_x, 1)
        adapted_y = round(adapted_y, 1)

        return adapted_x, adapted_y


if __name__ == "__main__":
    pass
