const BASE_URL = (() => {
    const host = window.location.hostname;
    if (host === 'localhost' || host === '127.0.0.1') {
        return 'http://localhost:8000';
    }
    return 'http://103.151.63.84:8004';
})();

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

    // ====================================================================
    // ERROR HANDLING: Handle 401 Unauthorized (token expired/invalid)
    // ====================================================================
    if (response.status === 401) {
        // Clear localStorage untuk menghapus token yang sudah tidak valid
        localStorage.clear();

        // Show alert ke user
        alert("Sesi Anda telah habis. Silakan login kembali.");

        // Redirect ke halaman login
        window.location.hash = "#login";

        // Trigger router untuk merender halaman login
        if (typeof router === 'function') {
            router();
        }
    }

    return response;
}
