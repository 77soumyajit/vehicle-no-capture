import { useState } from "react";
import { FaSearch, FaUpload, FaCarSide, FaIdCard } from "react-icons/fa";

import api from "../services/api";

import SearchBox from "../components/SearchBox";
import ImageUploader from "../components/ImageUploader";
import VehicleCard from "../components/VehicleCard";
import GatePassCard from "../components/GatePassCard";
import VehicleRegistrationForm from "../components/VehicleRegistrationForm";

function Home() {

    const [vehicle, setVehicle] = useState(null);
    const [error, setError] = useState("");

    const [showRegistration, setShowRegistration] = useState(false);
    const [searchedVehicleNo, setSearchedVehicleNo] = useState("");

    const [gatePass, setGatePass] = useState(null);
    const [loading, setLoading] = useState(false);


    // Upload Success

    const handleUploadSuccess = (data) => {

        console.log("AI Result:", data);

        // Clear previous state
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

            case "PLATE_NOT_FOUND":

                setError("No license plate detected in the uploaded image.");

                break;

            case "OCR_FAILED":

                setError("Unable to read the vehicle number from the image.");

                break;

            default:

                setError("Unknown response from AI.");

        }

    };

    // Search Vehicle


    const searchVehicle = async (vehicleNo) => {

        try {

            const response = await api.get(`/vehicle/${vehicleNo}`);

            setVehicle(response.data);

            setError("");

            setShowRegistration(false);

            setSearchedVehicleNo("");

            setGatePass(null);

        }

        catch (error) {

            console.error(error);

            setVehicle(null);

            setGatePass(null);

            setError("Vehicle not found in database.");

            setShowRegistration(true);

            setSearchedVehicleNo(vehicleNo);

        }

    };

    // Vehicle Created

    const handleVehicleCreated = (vehicle) => {
        setVehicle(vehicle);
        setShowRegistration(false);
        setError("");
        setSearchedVehicleNo("");
    };

    // Generate Gate Pass

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

        }

        catch (error) {

            console.error(error);

            alert("Unable to generate gate pass.");

        }

        finally {

            setLoading(false);

        }

    };

    return (

        <div className="main-container">

            <div className="header-card">

                <h1 className="page-title">
                    Vehicle Gate Management System
                </h1>

                <p className="page-subtitle">
                    AI Powered Vehicle Recognition & Gate Pass Generation
                </p>

            </div>

            <div className="section-card">

                <div className="section-heading">

                    <div className="step">
                        1
                    </div>

                    <div>

                        <h3 className="section-title mb-0">
                            Search Vehicle
                        </h3>

                        <small className="text-muted">
                            Search using Vehicle Number
                        </small>

                    </div>

                </div>

                <SearchBox
                    onSearch={searchVehicle}
                />

            </div>

            <div className="section-card">

                <div className="section-heading">

                    <div className="step">
                        2
                    </div>

                    <div>

                        <h3 className="section-title mb-0">
                            Upload Vehicle Image
                        </h3>

                        <small className="text-muted">
                            Upload a number plate image for OCR
                        </small>

                    </div>

                </div>

                <ImageUploader
                    onUploadSuccess={handleUploadSuccess}
                />

            </div>

            {

                error && (

                    <div className="alert alert-danger">

                        {error}

                    </div>

                )

            }

            {

                showRegistration && (

                    <div className="section-card">

                        <div className="section-heading">

                            <div className="step">

                                3

                            </div>

                            <div>

                                <h3 className="section-title mb-0">

                                    Register Vehicle

                                </h3>

                                <small className="text-muted">

                                    Vehicle not found. Please register it.

                                </small>

                            </div>

                        </div>

                        <VehicleRegistrationForm

                            vehicleNumber={searchedVehicleNo}

                            onVehicleCreated={handleVehicleCreated}

                        />

                    </div>

                )

            }

            {

                vehicle && (

                    <div className="section-card">

                        <div className="section-heading">

                            <div className="step">

                                3

                            </div>

                            <div>

                                <h3 className="section-title mb-0">

                                    Vehicle Information

                                </h3>

                                <small className="text-muted">

                                    Registered Vehicle Details

                                </small>

                            </div>

                        </div>

                        <VehicleCard

                            vehicle={vehicle}

                            onGenerate={generateGatePass}

                        />

                    </div>

                )

            }

            {

                loading && (

                    <div className="alert alert-info">

                        Generating Gate Pass...

                    </div>

                )

            }

            {

                gatePass && (

                    <div className="section-card">

                        <div className="section-heading">

                            <div className="step">

                                4

                            </div>

                            <div>

                                <h3 className="section-title mb-0">

                                    Gate Pass

                                </h3>

                                <small className="text-muted">

                                    Generated Successfully

                                </small>

                            </div>

                        </div>

                        <GatePassCard

                            gatePass={gatePass}

                        />

                    </div>

                )

            }

        </div>

    );

}

export default Home;