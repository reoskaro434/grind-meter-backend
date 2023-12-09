import os

from pydantic import BaseModel


class GlobalSettings(BaseModel):
    REFRESH_TOKEN_EXP_MIN: int = 60 * 24 * 30
    ACCESS_TOKEN_EXP_MIN: int = 5
    REGION: str = os.environ.get("REGION", "eu-central-1")
    STAGE: str = os.environ.get("STAGE", "dev")
    POOL_CLIENT_DATA_SECRET_NAME: str = f"GRIND_METER_COGNITO_POOL_CLIENT_DATA_{STAGE.upper()}_{REGION.upper()}"


global_settings = GlobalSettings()
