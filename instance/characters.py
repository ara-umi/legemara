#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
大多和刷取结果相关，通常需要客制化
为了方便，我们使用 python 特有的功能：中文命名变量
"""

from models.template import CharacterPortrait

####################
# 初音岛二期联动
####################

联动乌列尔 = CharacterPortrait(
    path="images/portrait/联动乌列尔.png",
    character_name="联动乌列尔",
    score=100,
    description="联动乌列尔半身照",
)
联动武尊 = CharacterPortrait(
    path="images/portrait/联动武尊.png",
    character_name="联动武尊",
    score=100,
    description="联动武尊半身照",
)

####################
# 常驻
####################

卑 = CharacterPortrait(
    path="images/portrait/卑.png",
    character_name="卑弥呼",
    score=100,
    description="卑弥呼半身照",
)
女仆 = CharacterPortrait(
    path="images/portrait/女仆.png",
    character_name="赫尔米",
    score=60,
    description="赫尔米半身照",
)
新米 = CharacterPortrait(
    path="images/portrait/新米.png",
    character_name="新米",
    score=80,
    description="新米半身照",
)
枪南丁 = CharacterPortrait(
    path="images/portrait/枪南丁.png",
    character_name="枪南丁",
    score=100,
    description="枪南丁半身照",
)
红神 = CharacterPortrait(
    path="images/portrait/红神.png",
    character_name="红神",
    score=70,
    description="红神半身照",
)
蓝神 = CharacterPortrait(
    path="images/portrait/蓝神.png",
    character_name="蓝神",
    score=100,
    description="蓝神半身照",
)
绿神 = CharacterPortrait(
    path="images/portrait/绿神.png",
    character_name="绿神",
    score=60,
    description="绿神半身照",
)

阿波罗 = CharacterPortrait(
    path="images/portrait/阿波罗.png",
    character_name="阿波罗",
    score=70,
    description="阿波罗半身照",
)
飞索 = CharacterPortrait(
    path="images/portrait/飞索.png",
    character_name="飞索",
    score=70,
    description="飞索半身照",
)
霍恩海姆 = CharacterPortrait(
    path="images/portrait/霍恩海姆.png",
    character_name="霍恩海姆",
    score=50,
    description="霍恩海姆半身照",
)

if __name__ == "__main__":
    pass
