function router() {

    const app = document.getElementById("app");

    const hash = window.location.hash;

    if (hash === "#dashboard") {

        app.innerHTML = `
        <div class="card shadow">

            <div class="card-header bg-success text-white">
                Dashboard Citizen Portal
            </div>

            <div class="card-body">

                <h4>Selamat Datang</h4>

                <p>Login JWT berhasil.</p>

                <button
                    class="btn btn-danger"
                    onclick="logout()">

                    Logout

                </button>

            </div>

        </div>
        `;

    } else {

        app.innerHTML = `
        <div class="row justify-content-center">

            <div class="col-md-6">

                <div class="card shadow">

                    <div class="card-header bg-primary text-white">
                        Login Citizen Portal
                    </div>

                    <div class="card-body">

                        <form onsubmit="login(event)">

                            <input
                                type="text"
                                id="username"
                                class="form-control mb-3"
                                placeholder="Username">

                            <input
                                type="password"
                                id="password"
                                class="form-control mb-3"
                                placeholder="Password">

                            <button
                                type="submit"
                                class="btn btn-primary w-100">

                                Login

                            </button>

                        </form>

                    </div>

                </div>

            </div>

        </div>
        `;
    }
}

window.addEventListener("load", router);
window.addEventListener("hashchange", router);

function logout() {

    localStorage.clear();

    window.location.hash = "";

    router();
}