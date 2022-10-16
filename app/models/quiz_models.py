from sqlalchemy import String, Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.models.basemodels import BaseModel


class BlockModel(BaseModel):
    __tablename__ = "blocks"

    question = Column(String, nullable=False)
    answers = relationship("AnswerModel", lazy="joined")
    right_answer = Column(Integer, nullable=False)
    cost = Column(Integer, nullable=False)
    users = relationship("UserModel", secondary="user_and_block_model", back_populates="blocks", lazy="joined")

    level = relationship("LevelModel", back_populates="blocks", lazy="joined")
    level_id = Column(Integer, ForeignKey("levels.id"))


class AnswerModel(BaseModel):
    __tablename__ = "answers"

    answer = Column(String, nullable=False, unique=True)
    block_id = Column(Integer, ForeignKey("blocks.id"))


class UserBlockModel(BaseModel):
    """
        Промежуточная модель для реализации отношения "много-ко-много"
    """
    __tablename__ = "user_and_block_model"
    user_id = Column(Integer, ForeignKey("users.id"))
    block_id = Column(Integer, ForeignKey("blocks.id"))


class UserModel(BaseModel):
    __tablename__ = "users"

    user_id = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False, unique=True)
    money = Column(Float, nullable=True, default=0)
    number_block = Column(Integer, nullable=False, default=0)

    blocks = relationship("BlockModel", secondary="user_and_block_model", back_populates="users", lazy="joined")


class LevelModel(BaseModel):
    __tablename__ = "levels"

    level = Column(Integer, nullable=False, unique=True)
    blocks = relationship("BlockModel", back_populates="level", lazy="joined")
