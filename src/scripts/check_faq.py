from sqlalchemy import select

from app.database.session import SessionLocal
from app.models.faq import FAQ


def display_faqs() -> None:
    with SessionLocal() as db:
        faqs = db.scalars(
            select(FAQ).order_by(FAQ.id)
        ).all()

        for faq in faqs:
            print(
                faq.id,
                faq.category,
                faq.question,
                faq.active,
            )


if __name__ == "__main__":
    display_faqs()