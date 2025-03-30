#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pydantic import BaseModel


class ErolabsAccount(BaseModel):
    email: str
    password: str

    @property
    def dirname(self):
        return f"{self.email}_{self.password}"


if __name__ == "__main__":
    pass
