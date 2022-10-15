from sqlalchemy.orm import Session

from app.core.quiz_utils import get_quiz
from app.database.session import SessionLocal
from app.models.quiz_models import LevelModel, AnswerModel, BlockModel


def create_level_model(session: Session, _level: int) -> LevelModel:
    found_level_model = get_level_model_by_level(session, _level)
    if found_level_model is None:
        new_level_model = LevelModel(level=_level)
        session.add(new_level_model)
        session.commit()
        return new_level_model
    return found_level_model


def create_answer_model(session: Session, _answer: str) -> AnswerModel:
    found_answer_model = get_answer_model_by_answer(session, _answer)
    if found_answer_model is None:
        new_answer_model = AnswerModel(answer=_answer)
        session.add(new_answer_model)
        session.commit()
        return new_answer_model
    return found_answer_model


def get_level_model_by_level(session: Session, _level: int) -> LevelModel | None:
    return session.query(LevelModel).filter(LevelModel.level == _level).first()


def get_answer_model_by_answer(session: Session, _answer: str) -> AnswerModel | None:
    return session.query(AnswerModel).filter(AnswerModel.answer == _answer).first()


def create_blocks_model() -> None:
    quiz = get_quiz()
    with SessionLocal() as session:
        for block in quiz.blocks:
            level_model = create_level_model(session, block.level)
            answers_model = []
            for answer in block.answers:
                answer_model = create_answer_model(session, answer)
                answers_model.append(answer_model)

            new_block_model = BlockModel(
                question=block.question,
                answers=answers_model,
                right_answer=block.right_answer,
                cost=block.cost,
                level=level_model
            )
            session.add(new_block_model)
            session.commit()


def main() -> None:
    create_blocks_model()


if __name__ == "__main__":
    main()
