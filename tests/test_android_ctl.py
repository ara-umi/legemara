#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from controller.android import AndroidController
from settings import get_settings
from models.pos import DevPos


@pytest.fixture
def settings():
    return get_settings()


@pytest.fixture
def android_controller(settings):
    return AndroidController(settings)


def test_get_display_info(android_controller):
    print(android_controller.display_info)


def test_home(android_controller):
    android_controller.home()


def test_app_switch(android_controller):
    android_controller.app_switch()


def test_scroll(android_controller):
    from instance.pos import EROLABS_REGISTER_SCROLL_START, EROLABS_REGISTER_SCROLL_END
    android_controller.scroll(
        start_pos=EROLABS_REGISTER_SCROLL_START,
        end_pos=EROLABS_REGISTER_SCROLL_END,
        steps=50,
    )


def test_capture_region(android_controller):
    from instance.pos import EROLABS_REGISTER_SLIDER_TOP_LEFT, EROLABS_REGISTER_SLIDER_BOTTOM_RIGHT
    image = android_controller.capture_region(
        top_left=EROLABS_REGISTER_SLIDER_TOP_LEFT,
        bottom_right=EROLABS_REGISTER_SLIDER_BOTTOM_RIGHT,
    )
    import cv2
    cv2.imshow("test_capture_region", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def test_erolabs_slider(android_controller):
    from instance.pos import EROLABS_REGISTER_SLIDER_TOP_LEFT, EROLABS_REGISTER_SLIDER_BOTTOM_RIGHT
    image = android_controller.capture_region(
        top_left=EROLABS_REGISTER_SLIDER_TOP_LEFT,
        bottom_right=EROLABS_REGISTER_SLIDER_BOTTOM_RIGHT,
    )
    from utils.slider import process_erolabs_slider
    x = process_erolabs_slider(image)
    print(f"{x=}")
    if not x:
        # 检测不出来就拖到死，让它自动刷新
        x = 300
    start_pos = DevPos(
        x=671,
        y=496,
    )
    end_pos = DevPos(
        x=671 + x,
        y=496,
    )
    android_controller.scroll(
        start_pos=start_pos,
        end_pos=end_pos,
        duration=1,
        steps=300,
    )


if __name__ == "__main__":
    pass
