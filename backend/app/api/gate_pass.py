from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.gate_pass import (
    GatePassCreate,
    GatePassResponse
)

from app.services.gate_pass_service import GatePassService
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/gate-pass",
    tags=["Gate Pass"]
)


@router.post(
    "/generate",
    response_model=GatePassResponse
)
def generate_gate_pass(
    data: GatePassCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    gate_pass = GatePassService.generate(
        db,
        data.vehicle_id
    )

    if not gate_pass:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found"
        )

    return gate_pass