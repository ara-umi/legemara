#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from controller.android import AndroidController
from settings import get_settings


@pytest.fixture
def settings():
    return get_settings()


@pytest.fixture
def android_controller(settings):
    return AndroidController(settings)


def test_get_display_info(android_controller):
    result = android_controller.get_display_info()
    print(result)


def test_debug_position(android_controller):
    android_controller.debug_position()


if __name__ == "__main__":
    pass
