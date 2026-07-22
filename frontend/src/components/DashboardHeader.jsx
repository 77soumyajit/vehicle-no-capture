import {
    FaCarSide,
    FaCircle
} from "react-icons/fa";

function DashboardHeader() {
    return (
        <div className="dashboard-header">

            <div className="header-left">

                <div className="header-icon">
                    <FaCarSide />
                </div>

                <div>

                    <h1>
                        Vehicle Gate Management System
                    </h1>

                    <p>
                        AI Powered Vehicle Recognition &
                        Smart Gate Pass Generation
                    </p>

                </div>

            </div>

            <div className="system-status">

                <FaCircle className="status-dot"/>

                System Online

            </div>

        </div>
    );
}

export default DashboardHeader;