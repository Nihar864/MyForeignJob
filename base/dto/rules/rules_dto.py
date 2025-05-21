from typing import Optional

from pydantic import BaseModel


class RuleDTO(BaseModel):
    country_id: int
    rule_title: str
    rule_description: str

    class Config:
        from_attributes = True


class UpdateRuleDTO(BaseModel):
    rule_id: int
    country_id: Optional[int] = None
    rule_title: Optional[str] = None
    rule_description: Optional[str] = None
