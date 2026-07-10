from sqlalchemy.orm import Session, joinedload

from app.models.gate_pass import GatePass


class GatePassRepository:

    @staticmethod
    def get_last_gate_pass(db: Session):
        return (
            db.query(GatePass)
            .order_by(GatePass.id.desc())
            .first()
        )

    @staticmethod
    def create(db: Session, gate_pass: GatePass):

        db.add(gate_pass)

        db.commit()

        db.refresh(gate_pass)

        return (
            db.query(GatePass)
            .options(joinedload(GatePass.vehicle))
            .filter(GatePass.id == gate_pass.id)
            .first()
        )