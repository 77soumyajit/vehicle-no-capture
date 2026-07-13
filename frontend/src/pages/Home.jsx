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

    const [uploadedImage, setUploadedImage] = useState(null);

    // -------------------------
    // Upload Success
    // -------------------------

    const handleUploadSuccess = (data) => {

        setUploadedImage(data);

        console.log(data);

    };

    // -------------------------
    // Search Vehicle
    // -------------------------

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

    // -------------------------
    // Vehicle Created
    // -------------------------

    const handleVehicleCreated = (vehicle) => {

        setVehicle(vehicle);

        setShowRegistration(false);

        setError("");

    };

    // -------------------------
    // Generate Gate Pass
    // -------------------------

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

            {/* ================= HEADER ================= */}

            <div className="header-card">

                <h1 className="page-title">
                    🚗 Vehicle Gate Management System
                </h1>

                <p className="page-subtitle">
                    AI Powered Vehicle Recognition & Gate Pass Generation
                </p>

            </div>

            {/* ================= STEP 1 ================= */}

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

            {/* ================= STEP 2 ================= */}

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

                {

                    uploadedImage && (

                        <div className="alert alert-success mt-4">

                            <h5>
                                Image Uploaded Successfully
                            </h5>

                            <hr />

                            <p>
                                <strong>Image ID :</strong>{" "}
                                {uploadedImage.id}
                            </p>

                            <p>
                                <strong>Original Name :</strong>{" "}
                                {uploadedImage.original_name}
                            </p>

                            <p>
                                <strong>Stored Name :</strong>{" "}
                                {uploadedImage.stored_name}
                            </p>

                            <p>
                                <strong>OCR Status :</strong>{" "}
                                {uploadedImage.ocr_status}
                            </p>

                        </div>

                    )

                }

            </div>

            {/* ================= ERROR ================= */}

            {

                error && (

                    <div className="alert alert-danger">

                        {error}

                    </div>

                )

            }

            {/* ================= REGISTRATION ================= */}

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

            {/* ================= VEHICLE ================= */}

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

            {/* ================= LOADING ================= */}

            {

                loading && (

                    <div className="alert alert-info">

                        Generating Gate Pass...

                    </div>

                )

            }

            {/* ================= GATE PASS ================= */}

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