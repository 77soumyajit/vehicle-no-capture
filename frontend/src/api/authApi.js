import api from "./axios";

export const loginUser = async (data) => {
    const response = await api.post(
        "/auth/login",
        data
    );

    return response.data;
};

export const getCurrentUser = async () => {
    const response = await api.get(
        "/auth/me"
    );

    return response.data;
};

export const refreshAccessToken = async (
    refreshToken
) => {

    const response = await api.post(
        "/auth/refresh",
        {
            refresh_token: refreshToken,
        }
    );

    return response.data;
};