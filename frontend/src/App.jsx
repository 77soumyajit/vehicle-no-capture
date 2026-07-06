import { useEffect, useState } from "react";
import api from "./services/api";

function App() {
  const [vehicle, setVehicle] = useState(null);

  useEffect(() => {
    api.get("/vehicle/")
      .then((response) => {
        setVehicle(response.data.vehicle);
      })
      .catch((error) => {
        console.error(error);
      });
  }, []);

  return (
    <div style={{ padding: "40px" }}>
      <h1>Vehicle Gate Pass System</h1>

      {vehicle && (
        <>
          <h2>Vehicle Details</h2>

          <p>
            <strong>Vehicle No:</strong> {vehicle.vehicle_no}
          </p>

          <p>
            <strong>Owner:</strong> {vehicle.owner_name}
          </p>

          <p>
            <strong>Driver:</strong> {vehicle.driver_name}
          </p>
        </>
      )}
    </div>
  );
}

export default App;