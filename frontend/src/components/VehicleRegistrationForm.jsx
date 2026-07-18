import { useEffect, useState } from "react";
import api from "../services/api";

function VehicleRegistrationForm({ vehicleNumber, onVehicleCreated }) {

    const [loading, setLoading] = useState(false);

    const [form, setForm] = useState({
        vehicle_no: "",
        owner_name: "",
        driver_name: "",
        company_name: "",
        vehicle_type: "",
        manufacturer: "",
        color: "",
    });

    useEffect(() => {
        setForm((prev) => ({
            ...prev,
            vehicle_no: vehicleNumber || "",
        }));
    }, [vehicleNumber]);

    const handleChange = (e) => {

        setForm({
            ...form,
            [e.target.name]: e.target.value,
        });

    };

    const saveVehicle = async () => {

        if (
            !form.vehicle_no ||
            !form.owner_name ||
            !form.driver_name
        ) {
            alert("Please fill all required fields.");
            return;
        }

        try {

            setLoading(true);

            const response = await api.post(
                "/vehicle",
                form
            );

            onVehicleCreated(response.data);

        }

        catch (error) {

            console.error(error);

            if (error.response?.data?.detail) {

                alert(error.response.data.detail);

            }

            else {

                alert("Unable to register vehicle.");

            }

        }

        finally {

            setLoading(false);

        }

    };

    return (

        <div className="card border-0 shadow-sm">

            <div className="card-header bg-warning">

                <h4 className="mb-0">

                    🚘 Register New Vehicle

                </h4>

            </div>

            <div className="card-body">

                <div className="row">

                    <div className="col-md-6 mb-3">

                        <label className="form-label">

                            Vehicle Number *

                        </label>

                        <input
                            className="form-control"
                            name="vehicle_no"
                            value={form.vehicle_no}
                            onChange={handleChange}
                        />

                    </div>

                    <div className="col-md-6 mb-3">

                        <label className="form-label">

                            Owner Name *

                        </label>

                        <input
                            className="form-control"
                            name="owner_name"
                            value={form.owner_name}
                            onChange={handleChange}
                        />

                    </div>

                    <div className="col-md-6 mb-3">

                        <label className="form-label">

                            Driver Name *

                        </label>

                        <input
                            className="form-control"
                            name="driver_name"
                            value={form.driver_name}
                            onChange={handleChange}
                        />

                    </div>

                    <div className="col-md-6 mb-3">

                        <label className="form-label">

                            Company Name

                        </label>

                        <input
                            className="form-control"
                            name="company_name"
                            value={form.company_name}
                            onChange={handleChange}
                        />

                    </div>

                    <div className="col-md-6 mb-3">

                        <label className="form-label">

                            Vehicle Type

                        </label>

                        <select
                            className="form-select"
                            name="vehicle_type"
                            value={form.vehicle_type}
                            onChange={handleChange}
                        >

                            <option value="">Select Vehicle Type</option>
                            <option value="Truck">Truck</option>
                            <option value="Car">Car</option>
                            <option value="Bus">Bus</option>
                            <option value="Pickup">Pickup</option>
                            <option value="Bike">Bike</option>

                        </select>

                    </div>

                    <div className="col-md-6 mb-3">

                        <label className="form-label">

                            Manufacturer

                        </label>

                        <input
                            className="form-control"
                            name="manufacturer"
                            value={form.manufacturer}
                            onChange={handleChange}
                        />

                    </div>

                    <div className="col-md-6 mb-3">

                        <label className="form-label">

                            Color

                        </label>

                        <input
                            className="form-control"
                            name="color"
                            value={form.color}
                            onChange={handleChange}
                        />

                    </div>

                </div>

                <div className="d-grid mt-3">

                    <button
                        className="btn btn-success btn-lg"
                        onClick={saveVehicle}
                        disabled={loading}
                    >

                        {
                            loading
                                ? "Registering Vehicle..."
                                : "Register Vehicle"
                        }

                    </button>

                </div>

            </div>

        </div>

    );

}

export default VehicleRegistrationForm;