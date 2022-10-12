from sqlalchemy import String, Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.models.basemodels import BaseModel


class BlockModel(BaseModel):
    __tablename__ = "blocks"

    question = Column(String, nullable=False)
    answers = relationship("AnswerModel")
    right_answer = Column(Integer, nullable=False)


class AnswerModel(BaseModel):
    __tablename__ = "answers"

    answer = Column(String, nullable=False, unique=True)
    level_model_id = Column(Integer, ForeignKey("blocks.id"))


class UserModel(BaseModel):
    __tablename__ = "users"

    user_id = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False, unique=True)
    money = Column(Float, nullable=True, default=0)
    selected_block = relationship("BlockModel", uselist=False)
