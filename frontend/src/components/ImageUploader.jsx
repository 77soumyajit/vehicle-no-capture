import { useState } from "react";
import api from "../services/api";

function ImageUploader({ onUploadSuccess }) {
    const [file, setFile] = useState(null);
    const [preview, setPreview] = useState(null);
    const [uploading, setUploading] = useState(false);

    const handleFileChange = (e) => {
        const selected = e.target.files[0];

        if (!selected) return;

        setFile(selected);
        setPreview(URL.createObjectURL(selected));
    };

    const processVehicle = async () => {
        if (!file) {
            alert("Please choose an image.");
            return;
        }

        const formData = new FormData();

        // FastAPI expects "image"
        formData.append("image", file);

        try {
            setUploading(true);

            const response = await api.post(
                "/process-vehicle/",
                formData,
                {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    },
                }
            );

            console.log("AI Response:", response.data);

            // Send complete backend response to Home.jsx
            onUploadSuccess(response.data);

        } catch (err) {
            console.error(err);

            if (err.response) {
                console.error(err.response.data);
            }

            alert("Unable to process vehicle image.");

        } finally {
            setUploading(false);
        }
    };

    return (
        <div className="card mt-4 shadow-sm">

            <div className="card-header bg-primary text-white">
                <h5 className="mb-0">
                    AI Vehicle Scanner
                </h5>
            </div>

            <div className="card-body">

                <input
                    type="file"
                    accept="image/*"
                    className="form-control"
                    onChange={handleFileChange}
                />

                {preview && (
                    <div className="text-center mt-4">

                        <img
                            src={preview}
                            alt="Vehicle Preview"
                            className="img-fluid rounded shadow"
                            style={{
                                maxHeight: "320px",
                                objectFit: "contain",
                            }}
                        />

                    </div>
                )}

                <button
                    className="btn btn-success w-100 mt-4"
                    onClick={processVehicle}
                    disabled={uploading}
                >
                    {uploading
                        ? "🔍 Analyzing Vehicle..."
                        : "🚗 Scan Vehicle"}
                </button>

            </div>

        </div>
    );
}

export default ImageUploader;