function GatePassCard({ gatePass }) {

    if (!gatePass) return null;

    return (

        <div className="card shadow mt-4">

            <div className="card-header bg-success text-white">

                <h4 className="mb-0">
                    Vehicle Gate Pass
                </h4>

            </div>

            <div className="card-body">

                <p>
                    <strong>Gate Pass No :</strong>
                    {" "}
                    {gatePass.gate_pass_no}
                </p>

                <p>
                    <strong>Vehicle No :</strong>
                    {" "}
                    {gatePass.vehicle.vehicle_no}
                </p>

                <p>
                    <strong>Owner :</strong>
                    {" "}
                    {gatePass.vehicle.owner_name}
                </p>

                <p>
                    <strong>Driver :</strong>
                    {" "}
                    {gatePass.vehicle.driver_name}
                </p>

                <p>
                    <strong>Status :</strong>
                    {" "}
                    {gatePass.status}
                </p>

                <p>
                    <strong>Entry Time :</strong>
                    {" "}
                    {new Date(
                        gatePass.entry_time
                    ).toLocaleString()}
                </p>

                <button
                    className="btn btn-primary w-100 mt-3"
                    onClick={() => window.print()}
                >
                    Print Gate Pass
                </button>

            </div>

        </div>

    );

}

export default GatePassCard;