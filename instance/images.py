#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from models.template import DevTemplate

LEGECLO_APP_ICON = DevTemplate(
    path="images/legeclo_app_icon.png",
    description="传奇四叶草桌面图标",
)
VISITOR_LOGIN = DevTemplate(
    path="images/visitor_login.png",
    description="erolabs黑端访客登录",
)
NO_EROLABS_ACCOUNT = DevTemplate(
    path="images/no_erolabs_account.png",
    description="没有erolabs账号（下面的注册新账号）",
)
EROLABS_CAN_REGISTER = DevTemplate(
    path="images/erolabs_can_register.png",
    description="EROLABS注册新账号，粉色，表示通过了滑条验证",
)
LOGIN_PAGE_SYMBOL = DevTemplate(
    path="images/login_page_symbol.png",
    description="传草登录界面标识，即左上角游戏图标",
)
NAME_RULE = DevTemplate(
    path="images/name_rule.png",
    description="传草取名规则",
)
INPUT_INVITE_CODE = DevTemplate(
    path="images/input_invite_code.png",
    description="传草输入邀请码",
)
IF_SKIP_BEGINNER = DevTemplate(
    path="images/if_skip_beginner.png",
    description="传草是否跳过新手引导",
)
BEGINNER_CONVERSATION = DevTemplate(
    path="images/beginner_conversation.png",
    description="新手引导对话框，黎德莉问这是哪里",
)
GUILD_LOCKED = DevTemplate(
    path="images/guild_shadow.png",
    description="上锁的公会标志",
)
BEGINNER_HERE_GACHA = DevTemplate(
    path="images/beginner_here_gacha.png",
    description="新手指引，黎德莉告诉你这里可以着急伙伴",
)
BEGINNER_10X = DevTemplate(
    path="images/beginner_10x.png",
    description="新手10连",
)
BEGINNER_10X_OVER_OK = DevTemplate(
    path="images/beginner_10x_over_ok.png",
    description="新手10连结束确认OK，让你去强化",
)
# 如果要弹公告它会没有高光，需要降低阈值
# 检测到它不一定说明停留在主页，但一定进了游戏
HOMEPAGE_FREE = DevTemplate(
    path="images/homepage_free.png",
    description="主页下方栏目，用来判断是否进入了游戏且可以操",
)
JEANNE_SKIRT = DevTemplate(
    path="images/jeanne_skirt.png",
    description="贞德主页裙子，注意如果触发对话则会被遮挡",
)
LIMITED_TIME_STORE = DevTemplate(
    path="images/limited_time_store.png",
    description="新手主页限定商店按钮，只有完成新手引导并且点完公告才会出现",
)
CHAR_OVERVIEW_MAIN_SUP_SHADOW = DevTemplate(
    path="images/char_overview_main_sup_shadow.png",
    description="角色一榄界面主站后援按钮，用于是否进入新手强化界面",
)
JEANNE_BIG_FACE = DevTemplate(
    path="images/jeanne_big_face.png",
    description="贞德主页大脸",
)
GACHA_10X = DevTemplate(
    path="images/gacha_10x.png",
    description="免费钻十连按钮",
)
GACHA_RESULT_10X = DevTemplate(
    path="images/gacha_result_10x.png",
    description="抽取结果界面的抽10次按钮，用来判断出了结果，同时用来继续抽",
)
INSUFFICIENT_FUNDS = DevTemplate(
    path="images/insufficient_funds.png",
    description="魔晶石不足提示，用于判断是否退出转蛋",
)
FILTER_BY_RARE_SSR_ACTIVE = DevTemplate(
    path="images/filter_by_rare_ssr_active.png",
    description="角色总览：显示条件：SSR：已勾选，需要很高阈值",
)



if __name__ == "__main__":
    pass
