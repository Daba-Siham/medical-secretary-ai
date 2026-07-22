from src.schemas import CallEntry, CallCategory, QualificationAction


def test_call_entry_creation():
    call = CallEntry(
        call_id="CALL-0001",
        text="Je souhaite annuler mon rendez-vous.",
    )

    assert call.call_id == "CALL-0001"
    assert call.language == "fr"


def test_categories():
    assert CallCategory.EMERGENCY.value == "urgence"
    assert (
        QualificationAction.TRANSFER_IMMEDIATELY.value
        == "TRANSFER_IMMEDIATELY"
    )