import { useState, useEffect } from "react";

import api from "../services/api";

import DashboardHeader from "../components/DashboardHeader";
import StatsCards from "../components/StatsCards";

import SearchBox from "../components/SearchBox";
import ImageUploader from "../components/ImageUploader";
import VehicleCard from "../components/VehicleCard";
import VehicleRegistrationForm from "../components/VehicleRegistrationForm";
import GatePassCard from "../components/GatePassCard";

import "../styles/dashboard.css";

function Home() {

    const [dashboard, setDashboard] = useState(null);

    const [vehicle, setVehicle] = useState(null);
    const [gatePass, setGatePass] = useState(null);

    const [error, setError] = useState("");

    const [loading, setLoading] = useState(false);

    const [showRegistration, setShowRegistration] = useState(false);

    const [searchedVehicleNo, setSearchedVehicleNo] = useState("");

    useEffect(() => {
        loadDashboard();
    }, []);

    const loadDashboard = async () => {

        try {

            const response = await api.get("/dashboard");

            setDashboard(response.data.summary);

        } catch (err) {

            console.log(err);

        }

    };

    // -----------------------------
    // AI Upload
    // -----------------------------

    const handleUploadSuccess = (data) => {

        setVehicle(null);
        setGatePass(null);
        setError("");
        setShowRegistration(false);

        switch (data.status) {

            case "FOUND":

                setVehicle(data.vehicle);

                break;

            case "NOT_FOUND":

                setSearchedVehicleNo(data.vehicle_no);

                setShowRegistration(true);

                setError(
                    `Vehicle ${data.vehicle_no} not found. Please register it.`
                );

                break;

            case "OCR_FAILED":

                setError("Unable to read vehicle number.");

                break;

            case "PLATE_NOT_FOUND":

                setError("No number plate detected.");

                break;

            default:

                setError("Unknown response.");

        }

        loadDashboard();

    };

    // -----------------------------
    // Search
    // -----------------------------

    const searchVehicle = async (vehicleNo) => {

        try {

            const response = await api.get(`/vehicle/${vehicleNo}`);

            setVehicle(response.data);

            setGatePass(null);

            setShowRegistration(false);

            setError("");

        }

        catch {

            setVehicle(null);

            setGatePass(null);

            setShowRegistration(true);

            setSearchedVehicleNo(vehicleNo);

            setError("Vehicle not found.");

        }

    };

    // -----------------------------
    // Register
    // -----------------------------

    const handleVehicleCreated = (vehicle) => {

        setVehicle(vehicle);

        setShowRegistration(false);

        setError("");

        loadDashboard();

    };

    // -----------------------------
    // Gate Pass
    // -----------------------------

    const generateGatePass = async (vehicleId) => {

        try {

            setLoading(true);

            const response = await api.post(
                "/gate-pass/generate",
                {
                    vehicle_id: vehicleId,
                }
            );

            setGatePass(response.data);

            loadDashboard();

        }

        catch {

            alert("Unable to generate gate pass.");

        }

        finally {

            setLoading(false);

        }

    };

    return (

        <div className="main-container">

            <DashboardHeader />

            <StatsCards dashboard={dashboard} />

            <div className="row g-4">

                {/* LEFT PANEL */}

                <div className="col-lg-4">

                    <div className="section-card mb-4">

                        <h4 className="mb-3">

                            🔍 Search Vehicle

                        </h4>

                        <SearchBox
                            onSearch={searchVehicle}
                        />

                    </div>

                    <div className="section-card">

                        <h4 className="mb-3">

                            🤖 AI Scanner

                        </h4>

                        <ImageUploader
                            onUploadSuccess={handleUploadSuccess}
                        />

                    </div>

                </div>

                {/* RIGHT PANEL */}

                <div className="col-lg-8">

                    {error && (

                        <div className="alert alert-danger">

                            {error}

                        </div>

                    )}

                    {showRegistration && (

                        <div className="section-card mb-4">

                            <h4>

                                Register Vehicle

                            </h4>

                            <VehicleRegistrationForm

                                vehicleNumber={searchedVehicleNo}

                                onVehicleCreated={handleVehicleCreated}

                            />

                        </div>

                    )}

                    {vehicle && (

                        <div className="section-card mb-4">

                            <VehicleCard

                                vehicle={vehicle}

                                onGenerate={generateGatePass}

                            />

                        </div>

                    )}

                    {loading && (

                        <div className="alert alert-info">

                            Generating Gate Pass...

                        </div>

                    )}

                    {gatePass && (

                        <div className="section-card">

                            <GatePassCard

                                gatePass={gatePass}

                            />

                        </div>

                    )}

                </div>

            </div>

        </div>

    );

}

export default Home;