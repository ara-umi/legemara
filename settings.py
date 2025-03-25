#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from typing import Optional

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# .env 文件路径
ROOT = os.path.dirname(__file__)
DOTENV = os.path.join(ROOT, ".env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # 从环境变量和 .env 文件加载
        env_file=(DOTENV,),
        # # 环境变量前缀
        # env_prefix="",
        # 大小写敏感
        case_sensitive=True,
        # # 额外的json序列化配置
        # json_schema_extra={
        #     "examples": [{"database_url": "postgresql://user:pass@localhost/db"}]
        # }
        frozen=True
    )

    LOG_DIR: str
    DEVICE: str

    @field_validator("LOG_DIR")
    def validate_log_dir(cls, v: str) -> Optional[str]:
        if not v:
            return None
        return v

    # 派生属性示例
    # @property
    # def async_database_url(self) -> str:
    #     """Convert DATABASE_URL to async version."""
    #     if self.DATABASE_URL.startswith("postgresql://"):
    #         return self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
    #     return self.DATABASE_URL


def get_settings() -> Settings:
    return Settings()


if __name__ == "__main__":
    config = get_settings()
    print(config.model_dump())
