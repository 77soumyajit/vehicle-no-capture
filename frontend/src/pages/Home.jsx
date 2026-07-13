import { useState } from "react";

import api from "../services/api";

import SearchBox from "../components/SearchBox";
import ImageUploader from "../components/ImageUploader";
import VehicleCard from "../components/VehicleCard";
import GatePassCard from "../components/GatePassCard";

function Home() {
    const [vehicle, setVehicle] = useState(null);
    const [error, setError] = useState("");

    const [gatePass, setGatePass] = useState(null);
    const [loading, setLoading] = useState(false);

    const [uploadedImage, setUploadedImage] = useState(null);

    // Called after successful image upload
    const handleUploadSuccess = (data) => {
        setUploadedImage(data);
        console.log(data);
    };

    // Search vehicle manually
    const searchVehicle = async (vehicleNo) => {
        try {
            const response = await api.get(`/vehicle/${vehicleNo}`);

            setVehicle(response.data);
            setError("");

        } catch {
            setVehicle(null);
            setError("Vehicle not found.");
        }
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

        } catch (error) {
            console.error(error);
            alert("Unable to generate gate pass.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container mt-5">

            <div className="card shadow">

                <div className="card-header bg-primary text-white">
                    <h2 className="text-center">
                        Vehicle Gate Management System
                    </h2>
                </div>

                <div className="card-body">

                    {/* Manual Search */}

                    <SearchBox
                        onSearch={searchVehicle}
                    />

                    <hr className="my-4" />

                    {/* Image Upload */}

                    <ImageUploader
                        onUploadSuccess={handleUploadSuccess}
                    />

                    {/* Upload Status */}

                    {uploadedImage && (

                        <div className="alert alert-success mt-4">

                            <h5>Image Uploaded Successfully</h5>

                            <p>
                                <strong>Image ID:</strong>{" "}
                                {uploadedImage.id}
                            </p>

                            <p>
                                <strong>Original File:</strong>{" "}
                                {uploadedImage.original_name}
                            </p>

                            <p>
                                <strong>OCR Status:</strong>{" "}
                                {uploadedImage.ocr_status}
                            </p>

                            <p>
                                <strong>Stored Image:</strong>{" "}
                                {uploadedImage.stored_name}
                            </p>

                        </div>

                    )}

                    {/* Search Error */}

                    {error && (
                        <div className="alert alert-danger mt-4">
                            {error}
                        </div>
                    )}

                    {/* Vehicle Details */}

                    <VehicleCard
                        vehicle={vehicle}
                        onGenerate={generateGatePass}
                    />

                    {/* Gate Pass Loading */}

                    {loading && (
                        <div className="alert alert-info mt-4">
                            Generating Gate Pass...
                        </div>
                    )}

                    {/* Gate Pass */}

                    <GatePassCard
                        gatePass={gatePass}
                    />

                </div>

            </div>

        </div>
    );
}

export default Home;