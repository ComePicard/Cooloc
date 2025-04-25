from datetime import datetime
from pathlib import WindowsPath

from pydantic import BaseModel, Field
from pydantic_extra_types.ulid import ULID


class BaseModelCustom(BaseModel):
    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
            ULID: lambda u: str(u),
            WindowsPath: lambda p: p.as_posix()
        }

    def to_json(self, **kwargs) -> str:
        """
        Sérialise le modèle en JSON, en gérant les datetime et ULID.
        Utilise isoformat pour datetime et str pour ULID.
        """
        return self.model_dump_json(**kwargs)
