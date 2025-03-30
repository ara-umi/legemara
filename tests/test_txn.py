#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from controller.legeclo import LegecloController
from settings import get_settings


@pytest.fixture
def settings():
    return get_settings()


@pytest.fixture
def legeclo_controller(settings):
    return LegecloController(settings)


def test_erolabs_register(legeclo_controller):
    from txn.login_to_homepage import LoginToHomepage
    txn = LoginToHomepage(legeclo_controller)
    txn._create_account()


if __name__ == "__main__":
    pass
