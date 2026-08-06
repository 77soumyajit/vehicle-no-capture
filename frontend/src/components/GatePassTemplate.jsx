import Barcode from "react-barcode";

import "../styles/gatePass.css";

function GatePassTemplate({ gatePass }) {

    if (!gatePass) return null;

    return (

        <div
            id="gate-pass-template"
            className="gate-pass-template"
        >

            {/* Header */}

            <div className="gate-pass-header">

                {/* Replace with Company Logo Later */}

                <h2>
                    🚗 Vehicle Gate Pass
                </h2>

                <p className="text-muted mb-0">
                    Vehicle Entry Authorization
                </p>

                <hr />

            </div>

            {/* Top Information */}

            <div className="gate-pass-info">

                <div>

                    <strong>
                        Gate Pass No
                    </strong>

                    <br />

                    {gatePass.gate_pass_no}

                </div>

                <div>

                    <strong>
                        Status
                    </strong>

                    <br />

                    <span className="badge bg-success">
                        {gatePass.status}
                    </span>

                </div>

            </div>

            {/* Vehicle Information */}

            <table className="table table-bordered gate-pass-table">

                <tbody>

                    <tr>

                        <th>
                            Vehicle Number
                        </th>

                        <td>
                            {gatePass.vehicle.vehicle_no}
                        </td>

                    </tr>

                    <tr>

                        <th>
                            Owner Name
                        </th>

                        <td>
                            {gatePass.vehicle.owner_name}
                        </td>

                    </tr>

                    <tr>

                        <th>
                            Driver Name
                        </th>

                        <td>
                            {gatePass.vehicle.driver_name}
                        </td>

                    </tr>

                    <tr>

                        <th>
                            Company
                        </th>

                        <td>
                            {gatePass.vehicle.company_name || "-"}
                        </td>

                    </tr>

                    <tr>

                        <th>
                            Vehicle Type
                        </th>

                        <td>
                            {gatePass.vehicle.vehicle_type || "-"}
                        </td>

                    </tr>

                    <tr>

                        <th>
                            Manufacturer
                        </th>

                        <td>
                            {gatePass.vehicle.manufacturer || "-"}
                        </td>

                    </tr>

                    <tr>

                        <th>
                            Color
                        </th>

                        <td>
                            {gatePass.vehicle.color || "-"}
                        </td>

                    </tr>

                    <tr>

                        <th>
                            Entry Time
                        </th>

                        <td>
                            {new Date(
                                gatePass.entry_time
                            ).toLocaleString()}
                        </td>

                    </tr>

                </tbody>

            </table>

            {/* Barcode */}

            <div className="gate-pass-barcode">

                <Barcode
                    value={`${gatePass.gate_pass_no}|${gatePass.vehicle.vehicle_no}`}
                    format="CODE128"
                    width={1.5}
                    height={65}
                    margin={0}
                    fontSize={14}
                    displayValue={false}
                />

            </div>

            {/* Footer */}

            <div className="gate-pass-footer">

                <div className="signature">

                    <hr />

                    Security Guard

                </div>

                <div className="signature">

                    <hr />

                    Authorized Signatory

                </div>

            </div>

        </div>

    );

}

export default GatePassTemplate;