const BASE_URL = "http://103.151.63.84:8004";

async function requestAPI(endpoint, method = "GET", data = null) {

    const token = localStorage.getItem("access_token");

    const options = {
        method: method,
        headers: {
            "Content-Type": "application/json"
        }
    };

    if (token) {
        options.headers["Authorization"] = `Bearer ${token}`;
    }

    if (data) {
        options.body = JSON.stringify(data);
    }

    const response = await fetch(
        `${BASE_URL}${endpoint}`,
        options
    );

    return response;
}