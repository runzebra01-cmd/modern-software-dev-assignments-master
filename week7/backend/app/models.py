from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class Note(Base, TimestampMixin):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    
    # 关系: 一个笔记可以有多个行动项
    action_items = relationship("ActionItem", back_populates="note", cascade="all, delete-orphan")


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


