import { useState } from "react";

import api from "../services/api";

import SearchBox from "../components/SearchBox";
import VehicleCard from "../components/VehicleCard";

function Home() {

    const [vehicle, setVehicle] = useState(null);
    const [error, setError] = useState("");

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
                    />

                </div>

            </div>

        </div>

    );

}

export default Home;