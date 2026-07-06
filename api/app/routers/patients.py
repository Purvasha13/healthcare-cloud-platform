from fastapi import APIRouter

router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)


@router.get("/")
def get_patients():
    return {
        "patients": [
            {
                "patient_id": 1,
                "full_name": "Test Patient One",
                "email": "patient1@example.com",
                "phone": "0400000001"
            },
            {
                "patient_id": 2,
                "full_name": "Test Patient Two",
                "email": "patient2@example.com",
                "phone": "0400000002"
            }
        ]
    }