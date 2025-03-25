#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Optional

from airtest.core.cv import Template

from models.android import DisplayInfo
from models.base import DEVELOP_DISPLAY_INFO


class DevTemplate(object):
    """
    构建 Template 时需要指定模板所对应的分辨率大小
    airtest 的方法会自动读取 G 中的 device 信息，底层可以看到有 _resize 方法
    """

    def __init__(
            self,
            path: str,
            display_info: Optional[DisplayInfo] = None,
            threshold: Optional[float] = 0.8,
            description: str = "",
            **kwargs,
    ):
        """
        threshold 可以不传，loop_find 接受的 threshold 会覆盖这个值
        具体参数请查看 airtest Template 类
        """
        if not display_info:
            self.display_info = DEVELOP_DISPLAY_INFO
        else:
            self.display_info = display_info
        self.path = path
        self.threshold = threshold
        self.resolution = (self.display_info.width, self.display_info.height)
        template = Template(
            filename=path,
            threshold=threshold,
            resolution=self.resolution,
            **kwargs,
        )
        self._template = template
        self.description = description

    @property
    def template(self) -> Template:
        return self._template

    def __str__(self):
        return f"path={self.path}, resolution={self.resolution}, description={self.description}"


class CharacterPortrait(DevTemplate):
    """
    需要刷取的角色模板，这里对应角色总览里的半身照
    后续如果需要切换刷取的卡池，可能需要在转蛋结果处检测，就需要小头照，到时候再建一个
    小头像用 thumbnail
    """

    def __init__(
            self,
            path: str,
            character_name: str,
            score: float,  # 角色评分，自己定基准
            display_info: Optional[DisplayInfo] = None,
            threshold: Optional[float] = 0.8,
            description: str = "",
            **kwargs,
    ):
        super().__init__(
            path=path,
            display_info=display_info,
            threshold=threshold,
            description=description,
            **kwargs,
        )
        self._name = character_name
        self._score = score

    @property
    def name(self) -> str:
        """
        角色名字
        """
        return self._name

    @property
    def score(self) -> float:
        """
        角色评分，用于评判刷出的初始号到底好不好，评分越高说明越好
        """
        return self._score


if __name__ == "__main__":
    pass
