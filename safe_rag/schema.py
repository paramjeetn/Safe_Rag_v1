from sqlalchemy import Column, Integer, String, MetaData, Table, Text, Boolean, JSON, DateTime, func
from typing import TypedDict

metadata = MetaData()

file_status = Table(
    "file_status",
    metadata,
    Column("file_id", String, nullable=False),
    Column("file_etags", String, nullable=False),
    Column("added_by_user_id", String, nullable=False),
    Column("created_at", DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp()),
    Column("chrome_index_made", Boolean, nullable=False),
    Column("process_status", Boolean, nullable=False),
)
