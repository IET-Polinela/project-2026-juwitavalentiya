async function login(event) {

    event.preventDefault();

    const username =
        document.getElementById("username").value;

    const password =
        document.getElementById("password").value;

    const response = await requestAPI(
        "/api/token/",
        "POST",
        {
            username,
            password
        }
    );

    const data = await response.json();

    if (response.status === 200) {

        localStorage.setItem(
            "access_token",
            data.access
        );

        localStorage.setItem(
            "refresh_token",
            data.refresh
        );

        alert("Login Berhasil");

        window.location.hash = "#dashboard";

        router();

    } else {

        alert("Username atau Password Salah");

    }
}