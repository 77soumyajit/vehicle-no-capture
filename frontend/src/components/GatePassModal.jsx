import GatePassTemplate from "./GatePassTemplate";

import {
    downloadGatePass,
    printGatePass,
} from "../utils/gatePassPrint";

function GatePassModal({
    gatePass,
    onClose,
    onCompleted,
}) {

    if (!gatePass) return null;

    const handleDownload = async () => {

        try {

            await downloadGatePass();

            if (onCompleted) {
                onCompleted();
            }

        } catch (err) {

            console.error(
                "PDF Download Failed",
                err,
            );

            alert(
                "Unable to download Gate Pass."
            );

        }

    };

    const handlePrint = async () => {

        try {

            await printGatePass();

            if (onCompleted) {
                onCompleted();
            }

        } catch (err) {

            console.error(
                "Print Failed",
                err,
            );

            alert(
                "Unable to print Gate Pass."
            );

        }

    };

    return (

        <div
            className="modal fade show gate-pass-modal"
            style={{
                display: "block",
                backgroundColor: "rgba(0,0,0,.6)",
            }}
        >

            <div className="modal-dialog modal-xl modal-dialog-centered">

                <div className="modal-content">

                    <div className="modal-header">

                        <h4 className="modal-title">
                            Gate Pass Preview
                        </h4>

                        <button
                            className="btn-close"
                            onClick={onClose}
                        />

                    </div>

                    <div className="modal-body gate-pass-body">

                        <GatePassTemplate
                            gatePass={gatePass}
                        />

                    </div>

                    <div className="modal-footer">

                        <button
                            className="btn btn-secondary"
                            onClick={onClose}
                        >
                            Close
                        </button>

                        <button
                            className="btn btn-success"
                            onClick={handleDownload}
                        >
                            📄 Download PDF
                        </button>

                        <button
                            className="btn btn-primary"
                            onClick={handlePrint}
                        >
                            🖨 Print
                        </button>

                    </div>

                </div>

            </div>

        </div>

    );

}

export default GatePassModal;