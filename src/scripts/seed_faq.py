from sqlalchemy import select

from app.database.session import SessionLocal
from app.models.faq import FAQ


# Données d'exemple destinées au développement.
# Elles seront remplacées par les informations officielles de l'établissement.

INITIAL_FAQS = [
    {
        "question": "Quels sont les horaires d’ouverture du cabinet ?",
        "answer": (
            "Le cabinet est ouvert du lundi au vendredi de 08h30 à 18h30 "
            "et le samedi de 09h00 à 13h00. Le cabinet est fermé le dimanche "
            "et les jours fériés."
        ),
        "category": "informations",
        "tags": ["horaires", "ouverture", "fermeture", "cabinet"],
    },
    {
        "question": "Quelle est l’adresse du cabinet ?",
        "answer": (
            "Le cabinet est situé au 25 Avenue Mohammed V, Tanger 90000. "
            "Vous pouvez également consulter notre localisation sur Google Maps."
        ),
        "category": "informations",
        "tags": ["adresse", "localisation", "itinéraire", "cabinet"],
    },
    {
        "question": "Un parking est-il disponible ?",
        "answer": (
            "Oui, un parking gratuit est disponible pour les patients devant "
            "le cabinet, avec plusieurs places réservées."
        ),
        "category": "informations",
        "tags": ["parking", "stationnement", "voiture", "accès"],
    },
    {
        "question": "Quelles spécialités médicales sont proposées ?",
        "answer": (
            "Le cabinet propose des consultations en médecine générale, "
            "cardiologie, dermatologie, pédiatrie et gynécologie."
        ),
        "category": "informations",
        "tags": ["spécialités", "médecins", "consultations", "services"],
    },
    {
        "question": "Comment préparer ma consultation ?",
        "answer": (
            "Veuillez apporter votre pièce d’identité, votre carte d’assurance "
            "maladie, vos ordonnances en cours ainsi que les résultats de vos "
            "examens récents si vous en disposez."
        ),
        "category": "informations",
        "tags": ["préparation", "consultation", "documents", "consignes"],
    },
    {
        "question": "Quels sont les tarifs des consultations ?",
        "answer": (
            "Les consultations de médecine générale débutent à partir de 250 MAD. "
            "Les consultations spécialisées sont comprises entre 350 MAD et 600 MAD "
            "selon la spécialité."
        ),
        "category": "devis",
        "tags": ["tarif", "prix", "consultation", "devis"],
    },
    {
        "question": "Quels moyens de paiement sont acceptés ?",
        "answer": (
            "Le cabinet accepte les paiements en espèces, par carte bancaire "
            "et par virement bancaire."
        ),
        "category": "informations",
        "tags": ["paiement", "carte", "espèces", "virement"],
    },
    {
        "question": "Comment récupérer mes résultats d’examens ?",
        "answer": (
            "Les résultats peuvent être retirés directement à l’accueil du cabinet "
            "ou consultés via votre espace patient lorsqu’ils sont disponibles."
        ),
        "category": "laboratoire",
        "tags": ["résultats", "examens", "laboratoire", "analyse"],
    },
    {
        "question": "Le cabinet propose-t-il la téléconsultation ?",
        "answer": (
            "Oui, des téléconsultations sont proposées sur rendez-vous pour "
            "certaines spécialités médicales."
        ),
        "category": "informations",
        "tags": ["téléconsultation", "consultation", "distance", "vidéo"],
    },
    {
        "question": "Comment obtenir un document administratif ?",
        "answer": (
            "Les certificats médicaux, attestations et autres documents "
            "administratifs peuvent être demandés auprès du secrétariat "
            "ou via votre espace patient."
        ),
        "category": "administratif",
        "tags": ["document", "administratif", "attestation", "certificat"],
    },
    {
        "question": "Comment contacter la pharmacie ?",
        "answer": (
            "Pour toute question concernant vos médicaments ou votre ordonnance, "
            "vous pouvez contacter la pharmacie au 05 39 00 00 00 pendant les "
            "heures d’ouverture."
        ),
        "category": "pharmacie",
        "tags": ["pharmacie", "contact", "médicament", "ordonnance"],
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