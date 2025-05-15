from sqlalchemy import Boolean, Column, text


class StatusMixin:
    is_deleted = Column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )
