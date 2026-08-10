import {
    FaCar,
    FaTicketAlt,
    FaImages,
} from "react-icons/fa";

function StatsCards({ dashboard }) {

    const cards = [

        {
            title: "Registered Today",
            value: dashboard?.registered_today ?? "--",
            icon: <FaCar />,
            bg: "#2563eb",
        },

        {
            title: "Today's Gate Passes",
            value: dashboard?.gate_pass_today ?? "--",
            icon: <FaTicketAlt />,
            bg: "#16a34a",
        },

        {
            title: "AI Scans Today",
            value: dashboard?.images_processed_today ?? "--",
            icon: <FaImages />,
            bg: "#06b6d4",
        },

        {
            title: "Total Vehicles",
            value: dashboard?.total_vehicles ?? "--",
            icon: <FaCar />,
            bg: "#7c3aed",
        },

        {
            title: "Total Gate Passes",
            value: dashboard?.total_gate_passes ?? "--",
            icon: <FaTicketAlt />,
            bg: "#f59e0b",
        },

    ];

    return (

        <div className="row g-4 mb-4">

            {cards.map((card, index) => (

                <div
                    key={index}
                    className="col-xl col-lg col-md-6 col-sm-6"
                >

                    <div className="stats-card">

                        <div
                            className="stats-icon"
                            style={{
                                background: card.bg,
                            }}
                        >

                            {card.icon}

                        </div>

                        <div className="stats-content">

                            <small>
                                {card.title}
                            </small>

                            <h2>
                                {card.value}
                            </h2>

                        </div>

                    </div>

                </div>

            ))}

        </div>

    );

}

export default StatsCards;