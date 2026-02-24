from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


# Association table for many-to-many relationship between notes and tags
note_tags = Table(
    "note_tags",
    Base.metadata,
    Column("note_id", Integer, ForeignKey("notes.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)


class Note(Base, TimestampMixin):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    
    # 关系: 一个笔记可以有多个行动项
    action_items = relationship("ActionItem", back_populates="note", cascade="all, delete-orphan")
    
    # 关系: 一个笔记可以有多个标签 (many-to-many)
    tags = relationship("Tag", secondary=note_tags, back_populates="notes")


class ActionItem(Base, TimestampMixin):
    __tablename__ = "action_items"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=False)
    completed = Column(Boolean, default=False, nullable=False)
    
    # 关联字段
    note_id = Column(Integer, ForeignKey("notes.id"), nullable=True)  # 关联到笔记
    
    # Task 2 增强字段
    priority = Column(String(20), nullable=True)  # high, medium, low
    category = Column(String(50), nullable=True)  # task, reminder, decision, general
    assignee = Column(String(100), nullable=True)  # 负责人
    due_date = Column(String(50), nullable=True)  # 截止日期
    
    # 关系: 行动项属于一个笔记
    note = relationship("Note", back_populates="action_items")


class Tag(Base, TimestampMixin):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    color = Column(String(20), nullable=True)  # 标签颜色，如 "#FF5733"
    
    # 关系: 一个标签可以应用于多个笔记 (many-to-many)
    notes = relationship("Note", secondary=note_tags, back_populates="tags")

