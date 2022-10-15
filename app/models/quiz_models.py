from sqlalchemy import String, Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.models.basemodels import BaseModel


class BlockModel(BaseModel):
    __tablename__ = "blocks"

    question = Column(String, nullable=False)
    answers = relationship("AnswerModel")
    right_answer = Column(Integer, nullable=False)
    cost = Column(Integer, nullable=False)
    level = relationship("LevelModel", uselist=False)

    user_id = Column(Integer, ForeignKey("users.id"))


class AnswerModel(BaseModel):
    __tablename__ = "answers"

    answer = Column(String, nullable=False, unique=True)
    block_id = Column(Integer, ForeignKey("blocks.id"))


class UserModel(BaseModel):
    __tablename__ = "users"

    user_id = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False, unique=True)
    money = Column(Float, nullable=True, default=0)
    block = relationship("BlockModel", uselist=False)


class LevelModel(BaseModel):
    __tablename__ = "levels"

    level = Column(Integer, nullable=False, unique=True)
    block_id = Column(Integer, ForeignKey("blocks.id"))
