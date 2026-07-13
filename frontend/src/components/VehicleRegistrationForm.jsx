import { useState } from "react";
import api from "../services/api";

function VehicleRegistrationForm({ vehicleNumber, onVehicleCreated }) {

    const [form, setForm] = useState({
        vehicle_no: vehicleNumber || "",
        owner_name: "",
        driver_name: "",
        company_name: "",
        vehicle_type: "",
        manufacturer: "",
        color: "",
    });

    const handleChange = (e) => {

        setForm({
            ...form,
            [e.target.name]: e.target.value,
        });

    };

    const saveVehicle = async () => {

        try {

            const response = await api.post(
                "/vehicle",
                form
            );

            alert("Vehicle Registered Successfully");

            onVehicleCreated(response.data);

        }

        catch (error) {

            console.error(error);

            alert("Unable to save vehicle.");

        }

    };

    return (

        <div className="card mt-4">

            <div className="card-header bg-warning">

                <h5>Vehicle Not Registered</h5>

            </div>

            <div className="card-body">

                <div className="mb-3">

                    <label>Vehicle Number</label>

                    <input
                        className="form-control"
                        name="vehicle_no"
                        value={form.vehicle_no}
                        onChange={handleChange}
                    />

                </div>

                <div className="mb-3">

                    <label>Owner Name</label>

                    <input
                        className="form-control"
                        name="owner_name"
                        onChange={handleChange}
                    />

                </div>

                <div className="mb-3">

                    <label>Driver Name</label>

                    <input
                        className="form-control"
                        name="driver_name"
                        onChange={handleChange}
                    />

                </div>

                <div className="mb-3">

                    <label>Company Name</label>

                    <input
                        className="form-control"
                        name="company_name"
                        onChange={handleChange}
                    />

                </div>

                <div className="mb-3">

                    <label>Vehicle Type</label>

                    <select
                        className="form-control"
                        name="vehicle_type"
                        onChange={handleChange}
                    >

                        <option value="">Select</option>

                        <option>Truck</option>

                        <option>Car</option>

                        <option>Bus</option>

                        <option>Pickup</option>

                    </select>

                </div>

                <div className="mb-3">

                    <label>Manufacturer</label>

                    <input
                        className="form-control"
                        name="manufacturer"
                        onChange={handleChange}
                    />

                </div>

                <div className="mb-3">

                    <label>Color</label>

                    <input
                        className="form-control"
                        name="color"
                        onChange={handleChange}
                    />

                </div>

                <button
                    className="btn btn-success w-100"
                    onClick={saveVehicle}
                >
                    Save Vehicle
                </button>

            </div>

        </div>

    );

}

export default VehicleRegistrationForm;