from app.models.gate_pass import GatePass
from app.repositories.vehicle_repository import VehicleRepository
from app.repositories.gate_pass_repository import GatePassRepository
from app.utils.gate_pass_generator import generate_gate_pass_number


class GatePassService:

    @staticmethod
    def generate(db, vehicle_id):

        vehicle = VehicleRepository.get_by_id(
            db,
            vehicle_id
        )

        if not vehicle:
            return None

        last_gate_pass = GatePassRepository.get_last_gate_pass(db)

        next_id = 1

        if last_gate_pass:
            next_id = last_gate_pass.id + 1

        gate_pass = GatePass(
            gate_pass_no=generate_gate_pass_number(next_id),
            vehicle_id=vehicle.id,
            status="ACTIVE"
        )

        return GatePassRepository.create(
            db,
            gate_pass
        )