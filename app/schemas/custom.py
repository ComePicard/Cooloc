from datetime import datetime

from pydantic import BaseModel
from pydantic_extra_types.ulid import ULID as PydanticUlid
from ulid import ULID as RawUlid


class BaseModelCustom(BaseModel):
    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
            PydanticUlid: lambda u: str(u),
            RawUlid: lambda u: str(u)
        }

    def to_json(self, **kwargs) -> str:
        """
        Sérialise le modèle en JSON, en gérant les datetime et ULID.
        Utilise isoformat pour datetime et str pour ULID.
        """
        return self.model_dump_json(**kwargs)
