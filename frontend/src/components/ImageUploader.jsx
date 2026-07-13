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

    const uploadImage = async () => {

        if (!file) {
            alert("Please choose an image.");
            return;
        }

        const formData = new FormData();

        formData.append("file", file);

        try {

            setUploading(true);

            const response = await api.post(
                "/upload/image",
                formData,
                {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    },
                }
            );

            onUploadSuccess(response.data);

        } catch (err) {

            console.error(err);

            alert("Upload failed.");

        } finally {

            setUploading(false);

        }
    };

    return (
        <div className="card mt-4">

            <div className="card-header">

                <h5>Upload Vehicle Image</h5>

            </div>

            <div className="card-body">

                <input
                    type="file"
                    accept="image/*"
                    onChange={handleFileChange}
                    className="form-control"
                />

                {preview && (

                    <img
                        src={preview}
                        alt="Preview"
                        className="img-fluid mt-3 rounded"
                        style={{ maxHeight: "300px" }}
                    />

                )}

                <button
                    className="btn btn-primary mt-3 w-100"
                    onClick={uploadImage}
                    disabled={uploading}
                >
                    {uploading ? "Uploading..." : "Upload Image"}
                </button>

            </div>

        </div>
    );
}

export default ImageUploader;