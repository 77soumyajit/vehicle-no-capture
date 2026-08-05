import axios from "axios";

const api = axios.create({
    baseURL: "http://127.0.0.1:8000",
    headers: {
        "Content-Type": "application/json",
    },
});

api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem("access_token");

        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }

        return config;
    },
    (error) => Promise.reject(error)
);

api.interceptors.response.use(

    (response) => response,

    async (error) => {

        const originalRequest = error.config;

        // Already retried once?
        if (originalRequest._retry) {
            return Promise.reject(error);
        }

        if (
            error.response &&
            error.response.status === 401
        ) {

            originalRequest._retry = true;

            const refreshToken =
                localStorage.getItem(
                    "refresh_token"
                );

            if (!refreshToken) {

                localStorage.removeItem(
                    "access_token"
                );

                localStorage.removeItem(
                    "refresh_token"
                );

                window.location.href = "/login";

                return Promise.reject(error);
            }

            try {

                console.log(
                    "Refreshing Access Token..."
                );

                const response = await axios.post(
                    "http://127.0.0.1:8000/auth/refresh",
                    {
                        refresh_token:
                            refreshToken,
                    }
                );

                const newAccessToken =
                    response.data.access_token;

                localStorage.setItem(
                    "access_token",
                    newAccessToken
                );

                originalRequest.headers.Authorization =
                    `Bearer ${newAccessToken}`;

                console.log(
                    "Access Token Refreshed"
                );

                return api(originalRequest);

            } catch (refreshError) {

                console.log(
                    "Refresh Token Expired"
                );

                localStorage.removeItem(
                    "access_token"
                );

                localStorage.removeItem(
                    "refresh_token"
                );

                window.location.href = "/login";

                return Promise.reject(
                    refreshError
                );
            }
        }

        return Promise.reject(error);
    }
);

export default api;