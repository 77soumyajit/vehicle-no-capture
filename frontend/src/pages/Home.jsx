import { useState } from "react";

import api from "../services/api";

import SearchBox from "../components/SearchBox";
import VehicleCard from "../components/VehicleCard";
import GatePassCard from "../components/GatePassCard";

function Home() {

    const [vehicle, setVehicle] = useState(null);
    const [error, setError] = useState("");
    const [gatePass, setGatePass] = useState(null);

    const [loading, setLoading] = useState(false);

    const searchVehicle = async (vehicleNo) => {

        try {

            const response = await api.get(`/vehicle/${vehicleNo}`);

            setVehicle(response.data);
            setError("");

        }

        catch {

            setVehicle(null);
            setError("Vehicle not found.");

        }

    };
    const generateGatePass = async (vehicleId) => {

        try {

            setLoading(true);

            const response = await api.post(
                "/gate-pass/generate",
                {
                    vehicle_id: vehicleId
                }
            );

            setGatePass(
                response.data
            );

        }

        catch (error) {

            alert(
                "Unable to generate gate pass."
            );

        }

        finally {

            setLoading(false);

        }

    };

    return (

        <div className="container mt-5">

            <div className="card shadow">

                <div className="card-header bg-primary text-white">

                    <h2 className="text-center">
                        Vehicle Gate Pass System
                    </h2>

                </div>

                <div className="card-body">

                    <SearchBox
                        onSearch={searchVehicle}
                    />

                    {
                        error &&
                        <div className="alert alert-danger mt-4">
                            {error}
                        </div>
                    }

                    <VehicleCard
                        vehicle={vehicle}
                        onGenerate={generateGatePass}
                    />
                    {
                        loading &&
                        <div className="alert alert-info mt-3">
                            Generating Gate Pass...
                        </div>
                    }

                    <GatePassCard
                        gatePass={gatePass}
                    />

                </div>

            </div>

        </div>

    );

}

export default Home;