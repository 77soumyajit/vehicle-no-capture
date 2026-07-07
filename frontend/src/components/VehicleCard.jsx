function VehicleCard({ vehicle }) {

    if (!vehicle) return null;

    return (

        <div className="card shadow mt-4">

            <div className="card-header bg-success text-white">

                Vehicle Details

            </div>

            <div className="card-body">

                <p>
                    <strong>Vehicle Number :</strong>
                    {" "}
                    {vehicle.vehicle_no}
                </p>

                <p>
                    <strong>Owner Name :</strong>
                    {" "}
                    {vehicle.owner_name}
                </p>

                <p>
                    <strong>Driver Name :</strong>
                    {" "}
                    {vehicle.driver_name}
                </p>

                <button
                    className="btn btn-success w-100 mt-3"
                >
                    Generate Gate Pass
                </button>

            </div>

        </div>

    );
}

export default VehicleCard;