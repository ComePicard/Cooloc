from datetime import datetime
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field
from pydantic_extra_types import ulid


class DocumentsCreate(BaseModel):
    name: str = Field(..., title="Name", max_length=50, description="Name of the document", examples=["Lease Agreement"])
    description: Optional[str] = Field(None, title="Description", max_length=255, description="Description of the document", examples=["Lease agreement for the apartment"])
    file_path: Path = Field(..., title="File Path", description="Path to the document file", examples=["/path/to/document.pdf"])
    owner_id: ulid = Field(..., title="Owner ID", description="ID of the user who owns the document", examples=["01F8MECHZX3TBDSZ7XK4F8G5J6"])
    group_id: Optional[ulid] = Field(None, title="Group ID", description="ID of the group associated with the document", examples=["01F8MECHZX3TBDSZ7XK4F8G5J6"])

class Documents(DocumentsCreate):
    id: ulid
    updated_at: datetime
