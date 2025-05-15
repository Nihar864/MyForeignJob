from datetime import datetime, UTC

from sqlalchemy import Column, DateTime, func


class TimestampMixin:
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(UTC),  # Generate at runtime
        nullable=False,
        server_default=func.now(),
    )
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(UTC),  # Generate at runtime
        onupdate=lambda: datetime.now(UTC),  # Also dynamic
        nullable=False,
        server_default=func.now(),
        server_onupdate=func.now(),
    )
