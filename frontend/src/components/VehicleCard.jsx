import {
    FaCarSide,
    FaUser,
    FaIdBadge,
    FaBuilding,
    FaPalette,
    FaIndustry
} from "react-icons/fa";

function VehicleCard({ vehicle, onGenerate }) {

    if (!vehicle) return null;

    return (

        <div className="card shadow-sm border-0">

            <div className="card-header bg-success text-white">

                <h4 className="mb-0">

                    <FaCarSide className="me-2"/>

                    Vehicle Information

                </h4>

            </div>

            <div className="card-body">

                <div className="row">

                    <div className="col-md-6 mb-3">

                        <strong>Vehicle Number</strong>

                        <p>{vehicle.vehicle_no}</p>

                    </div>

                    <div className="col-md-6 mb-3">

                        <strong>

                            <FaUser className="me-2"/>

                            Owner

                        </strong>

                        <p>{vehicle.owner_name}</p>

                    </div>

                    <div className="col-md-6 mb-3">

                        <strong>

                            <FaIdBadge className="me-2"/>

                            Driver

                        </strong>

                        <p>{vehicle.driver_name}</p>

                    </div>

                    <div className="col-md-6 mb-3">

                        <strong>

                            <FaBuilding className="me-2"/>

                            Company

                        </strong>

                        <p>

                            {vehicle.company_name || "-"}

                        </p>

                    </div>

                    <div className="col-md-6 mb-3">

                        <strong>Vehicle Type</strong>

                        <p>

                            {vehicle.vehicle_type || "-"}

                        </p>

                    </div>

                    <div className="col-md-6 mb-3">

                        <strong>

                            <FaIndustry className="me-2"/>

                            Manufacturer

                        </strong>

                        <p>

                            {vehicle.manufacturer || "-"}

                        </p>

                    </div>

                    <div className="col-md-6">

                        <strong>

                            <FaPalette className="me-2"/>

                            Color

                        </strong>

                        <p>

                            {vehicle.color || "-"}

                        </p>

                    </div>

                </div>

                <hr />

                <div className="d-grid">

                    <button
                        className="btn btn-primary btn-lg"
                        onClick={() => onGenerate(vehicle.id)}
                    >

                        Generate Gate Pass

                    </button>

                </div>

            </div>

        </div>

    );

}

export default VehicleCard;