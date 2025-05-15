from sqlalchemy import Boolean, Column, text


class StatusMixin:
    isDeleted = Column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )
