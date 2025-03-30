#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import string

from models.erolabs import ErolabsAccount


def create_erolabs_account() -> ErolabsAccount:
    """
    创建一个新的 erolabs 账号
    """
    email_characters = string.ascii_lowercase + string.digits
    email_length = 10
    email_suffix = "@legeclo.com"
    email: str = ''.join(random.choice(email_characters) for _ in range(email_length)) + email_suffix

    password_characters = string.ascii_letters + string.digits
    password_length = 10
    password: str = ''.join(random.choice(password_characters) for _ in range(password_length))

    return ErolabsAccount(
        email=email,
        password=password,
    )


if __name__ == "__main__":
    account = create_erolabs_account()
    print(account)
    print(account.dirname)
