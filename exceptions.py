#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from models.template import DevTemplate


class TemplateNotFound(Exception):

    def __init__(
            self,
            template: DevTemplate,
    ):
        self.template = template
        self.message = f"Template not found: {template}"
        super().__init__(self.message)


class TransactionRecoverError(Exception):
    pass


class TransactionRebootError(Exception):
    pass


if __name__ == "__main__":
    pass
