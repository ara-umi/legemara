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


def test_close_all_apps(legeclo_controller):
    legeclo_controller.close_all_apps()


def test_start_legeclo(legeclo_controller):
    legeclo_controller.start_legeclo()


if __name__ == "__main__":
    pass
