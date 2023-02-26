from typing import Any, Dict, List

from pydantic import BaseModel, EmailStr


class EmailSchema(BaseModel):
    recipients_email: List[EmailStr]
    body: Dict[str, Any]
