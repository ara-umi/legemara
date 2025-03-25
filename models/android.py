#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pydantic import BaseModel


class DisplayInfo(BaseModel):
    width: int
    height: int
    density: float
    orientation: int
    rotation: int
    max_x: int
    max_y: int


if __name__ == "__main__":
    pass
