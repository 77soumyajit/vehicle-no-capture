from datetime import datetime


def generate_gate_pass_number(next_id: int):

    today = datetime.now().strftime("%Y%m%d")

    return f"GP-{today}-{next_id:04d}"