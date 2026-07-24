from sqlalchemy import select

from app.database.session import SessionLocal
from app.models.faq import FAQ


INITIAL_FAQS = [
    {
        "question": "Quels sont les horaires d’ouverture du cabinet ?",
        "answer": (
            "Les horaires d’ouverture doivent être configurés "
            "par l’établissement."
        ),
        "category": "informations",
        "tags": [
            "horaires",
            "ouverture",
            "fermeture",
            "cabinet",
        ],
    },
    {
        "question": "Quelle est l’adresse du cabinet ?",
        "answer": (
            "L’adresse du cabinet doit être renseignée "
            "par l’établissement."
        ),
        "category": "informations",
        "tags": [
            "adresse",
            "localisation",
            "itinéraire",
            "cabinet",
        ],
    },
    {
        "question": "Un parking est-il disponible ?",
        "answer": (
            "Les informations concernant le stationnement "
            "doivent être configurées par l’établissement."
        ),
        "category": "informations",
        "tags": [
            "parking",
            "stationnement",
            "voiture",
            "accès",
        ],
    },
    {
        "question": "Quelles spécialités médicales sont proposées ?",
        "answer": (
            "La liste des spécialités doit être configurée "
            "par l’établissement."
        ),
        "category": "informations",
        "tags": [
            "spécialités",
            "médecins",
            "consultations",
            "services",
        ],
    },
    {
        "question": "Comment préparer ma consultation ?",
        "answer": (
            "Les consignes de préparation dépendent du type "
            "de consultation. La demande doit être transmise "
            "au service concerné lorsque les consignes ne sont "
            "pas disponibles dans une FAQ validée."
        ),
        "category": "informations",
        "tags": [
            "préparation",
            "consultation",
            "documents",
            "consignes",
        ],
    },
    {
        "question": "Quels sont les tarifs des consultations ?",
        "answer": (
            "Les tarifs doivent être configurés et validés "
            "par l’établissement."
        ),
        "category": "devis",
        "tags": [
            "tarif",
            "prix",
            "consultation",
            "devis",
        ],
    },
    {
        "question": "Quels moyens de paiement sont acceptés ?",
        "answer": (
            "Les moyens de paiement acceptés doivent être "
            "renseignés par l’établissement."
        ),
        "category": "informations",
        "tags": [
            "paiement",
            "carte",
            "espèces",
            "chèque",
        ],
    },
    {
        "question": "Comment récupérer mes résultats d’examens ?",
        "answer": (
            "Les modalités de récupération des résultats "
            "doivent être définies par l’établissement. "
            "Le Module 4 ne doit pas interpréter les résultats."
        ),
        "category": "laboratoire",
        "tags": [
            "résultats",
            "examens",
            "laboratoire",
            "analyse",
        ],
    },
    {
        "question": "Le cabinet propose-t-il la téléconsultation ?",
        "answer": (
            "La disponibilité et les modalités de téléconsultation "
            "doivent être configurées par l’établissement."
        ),
        "category": "informations",
        "tags": [
            "téléconsultation",
            "consultation",
            "distance",
            "vidéo",
        ],
    },
    {
        "question": "Comment obtenir un document administratif ?",
        "answer": (
            "La demande de document doit être transmise "
            "au service administratif compétent."
        ),
        "category": "administratif",
        "tags": [
            "document",
            "administratif",
            "attestation",
            "dossier",
        ],
    },
    {
        "question": "Comment contacter la pharmacie ?",
        "answer": (
            "Les coordonnées et les modalités de contact "
            "de la pharmacie doivent être configurées "
            "par l’établissement."
        ),
        "category": "pharmacie",
        "tags": [
            "pharmacie",
            "contact",
            "médicament",
            "coordonnées",
        ],
    },
]


def seed_faqs() -> None:
    with SessionLocal() as db:
        inserted = 0
        skipped = 0

        for faq_data in INITIAL_FAQS:
            statement = select(FAQ).where(
                FAQ.question == faq_data["question"]
            )

            existing_faq = db.scalar(statement)

            if existing_faq is not None:
                skipped += 1
                continue

            faq = FAQ(
                question=faq_data["question"],
                answer=faq_data["answer"],
                category=faq_data["category"],
                tags=faq_data["tags"],
                active=True,
            )

            db.add(faq)
            inserted += 1

        db.commit()

        print(f"FAQ insérées : {inserted}")
        print(f"FAQ ignorées car déjà présentes : {skipped}")


if __name__ == "__main__":
    seed_faqs()