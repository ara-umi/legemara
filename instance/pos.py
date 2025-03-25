#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from models.pos import DevPos

GAME_START = DevPos(
    x=802,
    y=789,
    description="GAME START"
)
NAME_INPUT = DevPos(
    x=808,
    y=382,
    description="输入玩家名空白框"
)
NAME_INPUT_OK = DevPos(
    x=906,
    y=600,
    description="输入玩家名确认"
)
SKIP_BEGINNER = DevPos(
    x=674,
    y=593,
    description="跳过新手引导"
)
HOMEPAGE_GACHA = DevPos(
    x=1032,
    y=853,
    description="主页转蛋按钮"
)
BEGINNER_10X = DevPos(
    x=1217,
    y=679,
    description="黎德莉提示：新手十连",
)
# 应该是所有只有单一也给长条状抽取键的池子布局都一样
FREE_10X = DevPos(
    x=1217,
    y=679,
    description="免费十连，和新手十连是一样的",
)
BEGINNER_10X_CONFIRM_OK = DevPos(
    x=909,
    y=597,
    description="新手十连确认OK",
)
BEGINNER_10X_OVER_OK = DevPos(
    x=801,
    y=662,
    description="新手十连结束，黎德莉让你去强化",
)
HOMEPAGE_CHARACTER = DevPos(
    x=341,
    y=858,
    description="主页角色按钮"
)
CHARACTER_MAIN = DevPos(
    x=550,
    y=268,
    description="角色界面：主战角色"
)
THIRD_CHARACTER = DevPos(
    x=1305,
    y=317,
    description="第三个主站角色，新手教程默认强化她，因为第一是主角，第二是贞德",
)
CHAR_OVERVIEW_UPGRADE = DevPos(
    x=550,
    y=734,
    description="角色总览界面：强化按钮"
)
RECOMMENDED_MATERIALS = DevPos(
    x=1471,
    y=716,
    description="推荐素材，就是一件强化按键"
)
RECOMMENDED_MATERIALS_CONFIRM = DevPos(
    x=1273,
    y=714,
    description="推荐素材确认的强化按键"
)
LEVEL_UP_OK = DevPos(
    x=802,
    y=752,
    description="强化后升级确认的OK"
)
HOMEPAGE_SAFE = DevPos(
    x=1465,
    y=458,
    description="主页安全位置，公会按钮的上方，一般没东西，主要用来跳过公告"
)
HOMEPAGE_MENU = DevPos(
    x=1493,
    y=856,
    description="主页选单按钮"
)
MENU_DELETE_ACCOUNT = DevPos(
    x=820,
    y=693,
    description="选单删除账号，带个垃圾桶的那个"
)
DELETE_ATTENTION_CONFIRM1 = DevPos(
    x=908,
    y=773,
    description="删除账号确认，第一次消除键"
)
DELETE_ATTENTION_CONFIRM2 = DevPos(
    x=908,
    y=671,
    description="删除账号确认，第二次消除键"
)
DELETE_SUCCESS_OK = DevPos(
    x=800,
    y=605,
    description="删除账号成功确认OK键"
)
GACHA_POOL1 = DevPos(
    x=145,
    y=204,
    description="转蛋池列表第一个"
)
GACHA_POOL2 = DevPos(
    x=145,
    y=326,
    description="转蛋池列表第二个"
)
GACHA_POOL3 = DevPos(
    x=145,
    y=446,
    description="转蛋池列表第三个"
)
GACHA_SELECT_CHARACTERS = DevPos(
    x=1088,
    y=663,
    description="转蛋：选择精选角色，通用"
)
GACHA_SELECT_CHARACTERS_1_1 = DevPos(
    x=450,
    y=245,
    description="转蛋：选择精选角色：第一行第一个"
)
GACHA_SELECT_CHARACTERS_1_3 = DevPos(
    x=795,
    y=241,
    description="转蛋：选择精选角色：第一行第三个"
)
GACHA_SELECT_CHARACTERS_CONFIRM_SELECT = DevPos(
    x=1427,
    y=850,
    description="转蛋：选择精选角色：点击角色后：选择"
)
GACHA_SELECT_CHARACTERS_OK = DevPos(
    x=902,
    y=821,
    description="转蛋：选择精选角色：OK"
)
GACHA_SELECT_CHARACTERS_CONFIRM_OK = DevPos(
    x=903,
    y=663,
    description="转蛋：选择精选角色：选好点击OK后：二度确认OK"
)
GACHA_SELECTED_10X = DevPos(
    x=1342,
    y=682,
    description="转蛋免费钻抽10次，用于自选池，右边会有重新选的标记挤占空间导致位置稍稍有变化"
)
GACHA_10X = DevPos(
    x=1378,
    y=682,
    description="转蛋免费钻抽10次，应该是通用的"
)
GACHA_CONFIRM_OK = DevPos(
    x=907,
    y=595,
    description="转蛋确认抽取OK，应该是通用的"
)
GACHA_SKIP = DevPos(
    x=1517,
    y=43,
    description="转蛋skip按钮，同时也是转蛋的安全位置"
)
# 白嫖池会稍稍不一样，能继续抽就只有返回和抽 10 次，不能继续抽就只有返回
GACHA_FREE_RESULT_10X = DevPos(
    x=930,
    y=663,
    description="白嫖池转蛋结果处的抽10次"
)
GACHA_RESULT_10X = DevPos(
    x=1188,
    y=663,
    description="转蛋结果处的抽10次"
)
HOMEPAGE_HOMEPAGE = DevPos(
    x=117,
    y=860,
    description="主页主页按钮，最左下角那个"
)
CHARACTER_OVERVIEW_SUP = DevPos(
    x=1112,
    y=147,
    description="角色总览：支援角色"
)
CHARACTER_FILTER_BY = DevPos(
    x=1488,
    y=150,
    description="角色总览：显示条件"
)
CHARACTER_FILTER_BY_RARE_SSR = DevPos(
    x=530,
    y=216,
    description="角色总览：显示条件：稀有度：SSR"
)
CHARACTER_FILTER_BY_CONFIRM_OK = DevPos(
    x=910,
    y=760,
    description="角色总览：显示条件：OK"
)
CHARACTER_FILTER_BY_CLOSE = DevPos(
    x=1414,
    y=68,
    description="角色总览：显示条件：关闭，不是真的在关闭位置上，偏上避免和显示条件重合，理论上点无关位置也会自动关闭"
)
HOMEPAGE_STAGE = DevPos(
    x=801,
    y=849,
    description="主页：关卡按钮"
)
STAGE_MAIN = DevPos(
    x=532,
    y=235,
    description="关卡界面：主线关卡"
)
STAGE_SKIP = DevPos(
    x=90,
    y=574,
    description="主线关卡界面：跳过关卡"
)
STAGE_SKIP_DECIDE = DevPos(
    x=913,
    y=757,
    description="主线关卡界面：跳过关卡：决定"
)
STAGE_SKIP_DECIDE_CONFIRM = DevPos(
    x=691,
    y=604,
    description="主线关卡界面：跳过关卡：决定：跳过"
)
STAGE_SKIP_SUCCESS_OK = DevPos(
    x=801,
    y=606,
    description="主线关卡界面：跳过关卡成功后：OK"
)
HOMEPAGE_GIFTS = DevPos(
    x=140,
    y=148,
    description="主页：礼物箱"
)
GIFTS_RECEIVE_ALL = DevPos(
    x=1268,
    y=788,
    description="礼物箱：全部领取"
)
HOMEPAGE_TASK = DevPos(
    x=232,
    y=149,
    description="主页：任务"
)
TASK_ACHIEVEMENT = DevPos(
    x=634,
    y=124,
    description="任务：实绩"
)
TASK_RECEIVE_ALL = DevPos(
    x=1293,
    y=703,
    description="任务：一键领取（通用）"
)
GET_SIGN_IN_REWARD_OK = DevPos(
    x=800,
    y=665,
    description="签到：已获得今天的登入奖励：OK（得有签到活动）"
)

if __name__ == "__main__":
    pass
