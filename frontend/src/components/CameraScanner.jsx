import { useEffect, useRef, useState } from "react";
// import api from "../services/api";
import api from "../api/axios";

function CameraScanner({ onUploadSuccess }) {

    const videoRef = useRef(null);
    const canvasRef = useRef(null);
    const streamRef = useRef(null);
    const intervalRef = useRef(null);

    const [cameraOn, setCameraOn] = useState(false);
    const [status, setStatus] = useState("Camera Off");
    const [confidence, setConfidence] = useState(null);
    const [processing, setProcessing] = useState(false);

    const isScanning = useRef(false);

    // -----------------------------
    // Open Camera
    // -----------------------------
    const startCamera = async () => {

        try {

            stopCamera();

            const stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    facingMode: "environment",
                    width: { ideal: 1280 },
                    height: { ideal: 720 }
                },
                audio: false
            });

            streamRef.current = stream;

            setCameraOn(true);

            setStatus("Starting Camera...");

        } catch (err) {

            console.error(err);

            alert("Unable to access camera.");

        }

    };

    // -----------------------------
    // Stop Camera
    // -----------------------------
    const stopCamera = () => {

        if (intervalRef.current) {

            clearInterval(intervalRef.current);

            intervalRef.current = null;

        }

        if (streamRef.current) {

            streamRef.current.getTracks().forEach(track => track.stop());

            streamRef.current = null;

        }

        setCameraOn(false);

        setProcessing(false);

        setConfidence(null);

        setStatus("Camera Off");

        isScanning.current = false;

    };

    // -----------------------------
    // Attach Camera
    // -----------------------------
    useEffect(() => {

        if (!cameraOn) return;

        if (!videoRef.current) return;

        if (!streamRef.current) return;

        videoRef.current.srcObject = streamRef.current;

        videoRef.current.onloadedmetadata = () => {

            videoRef.current.play();

            setStatus("Looking for Vehicle...");

            if (!intervalRef.current) {

                intervalRef.current = setInterval(() => {

                    scanFrame();

                }, 700);

            }

        };

    }, [cameraOn]);

    // -----------------------------
    // Scan Frame
    // -----------------------------
    const scanFrame = async () => {

        if (processing) return;

        if (isScanning.current) return;

        if (!videoRef.current) return;

        if (!canvasRef.current) return;

        if (videoRef.current.videoWidth === 0) return;

        isScanning.current = true;

        const canvas = canvasRef.current;

        canvas.width = videoRef.current.videoWidth;
        canvas.height = videoRef.current.videoHeight;

        const ctx = canvas.getContext("2d");

        ctx.drawImage(
            videoRef.current,
            0,
            0,
            canvas.width,
            canvas.height
        );

        const blob = await new Promise(resolve =>
            canvas.toBlob(resolve, "image/jpeg", 0.9)
        );

        if (!blob) {

            isScanning.current = false;

            return;

        }

        const formData = new FormData();

        formData.append("image", blob, "frame.jpg");

        try {

            const response = await api.post(
                "/live-detect/",
                formData,
                {
                    headers: {
                        "Content-Type": "multipart/form-data"
                    }
                }
            );

            const data = response.data;

            if (data.plate_detected) {

                clearInterval(intervalRef.current);
                intervalRef.current = null;

                setProcessing(true);

                setStatus("Plate Detected");

                setConfidence(data.confidence);

                // Send same frame for OCR + Database search

                const processForm = new FormData();

                processForm.append("image", blob, "frame.jpg");

                try {

                    const processResponse = await api.post(
                        "/process-vehicle/",
                        processForm,
                        {
                            headers: {
                                "Content-Type": "multipart/form-data",
                            },
                        }
                    );

                    console.log(processResponse.data);

                    onUploadSuccess(processResponse.data);

                } catch (err) {

                    console.error(err);

                    setStatus("Processing Failed");

                } finally {

                    setProcessing(false);

                    stopCamera();

                }

            } else {

                setStatus("Looking for Vehicle...");

            }

        } catch (err) {

            console.error(err);

        } finally {

            isScanning.current = false;

        }

    };
        // -----------------------------
    // Cleanup
    // -----------------------------
    useEffect(() => {

        return () => {

            stopCamera();

        };

    }, []);

    // -----------------------------
    // UI
    // -----------------------------
    return (

        <div>

            {

                !cameraOn && (

                    <button
                        className="btn btn-primary w-100"
                        onClick={startCamera}
                    >
                        📷 Open Camera
                    </button>

                )

            }

            {

                cameraOn && (

                    <>

                        <div
                            className="position-relative"
                            style={{
                                borderRadius: "10px",
                                overflow: "hidden"
                            }}
                        >

                            <video
                                ref={videoRef}
                                autoPlay
                                muted
                                playsInline
                                className="img-fluid"
                                style={{
                                    width: "100%",
                                    borderRadius: "10px"
                                }}
                            />

                            <div
                                style={{
                                    position: "absolute",
                                    top: 10,
                                    left: 10,
                                    background: "rgba(0,0,0,.6)",
                                    color: "#fff",
                                    padding: "6px 12px",
                                    borderRadius: "6px",
                                    fontSize: "14px"
                                }}
                            >
                                {status}
                            </div>

                        </div>

                        {

                            confidence && (

                                <div className="alert alert-success mt-3">

                                    <strong>

                                        Plate Confidence :

                                    </strong>

                                    {" "}

                                    {Number(confidence).toFixed(2)} %

                                </div>

                            )

                        }

                        {

                            processing && (

                                <div className="alert alert-warning mt-3">

                                    <strong>

                                        Plate detected.

                                    </strong>

                                    <br />

                                    Waiting for OCR...

                                </div>

                            )

                        }

                        <canvas

                            ref={canvasRef}

                            style={{
                                display: "none"
                            }}

                        />

                        <div className="d-grid mt-3">

                            <button

                                className="btn btn-danger"

                                onClick={stopCamera}

                            >

                                Close Camera

                            </button>

                        </div>

                    </>

                )

            }

        </div>

    );

}

export default CameraScanner;