import { useState } from "react";

function SearchBox({ onSearch }) {
    const [vehicleNo, setVehicleNo] = useState("");

    const handleSubmit = (e) => {
        e.preventDefault();

        if (!vehicleNo.trim()) {
            alert("Please enter a vehicle number");
            return;
        }

        onSearch(vehicleNo.toUpperCase());
    };

    return (
        <form onSubmit={handleSubmit}>
            <div className="mb-3">
                <label className="form-label fw-bold">
                    Vehicle Number
                </label>

                <input
                    type="text"
                    className="form-control form-control-lg"
                    placeholder="Enter Vehicle Number"
                    value={vehicleNo}
                    onChange={(e) => setVehicleNo(e.target.value)}
                />
            </div>

            <button className="btn btn-primary w-100">
                Search Vehicle
            </button>
        </form>
    );
}

export default SearchBox;