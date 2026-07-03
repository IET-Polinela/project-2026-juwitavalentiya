function router() {

    const app = document.getElementById("app");

    const hash = window.location.hash;

    // ====================================================================
    // AUTH GUARD: Redirect unauthenticated users to #login
    // ====================================================================
    // Jika user mencoba akses #dashboard tanpa token, redirect ke #login
    const hasToken = localStorage.getItem('access_token');
    if (hash === "#dashboard" && !hasToken) {
        window.location.hash = "#login";
        return;
    }

    // Jika user sudah login dan akses #login atau #register, redirect ke #dashboard
    if (hasToken && (hash === "#login" || hash === "#register" || hash === "")) {
        window.location.hash = "#dashboard";
        return;
    }

    if (hash === "#dashboard") {

        app.innerHTML = `
        <div class="app-shell d-flex">
            <aside class="sidebar">
                <div class="sidebar-logo">
                    <span>SR</span>
                    <div>
                        <div>SmartReport</div>
                        <small style="opacity:0.8;">Citizen Portal</small>
                    </div>
                </div>

                <a class="sidebar-link" id="navMyReports" href="javascript:void(0);" onclick="loadDashboardData('my_reports', 1)">Laporan Saya</a>
                <a class="sidebar-link" id="navFeed" href="javascript:void(0);" onclick="loadDashboardData('feed', 1)">Feed Kota</a>
                <a class="sidebar-link" href="javascript:void(0);" onclick="logout()">Logout</a>

                <div class="sidebar-cta">
                    <button class="btn btn-light btn-lg text-dark fw-semibold" id="btnBukaModal">+ Laporan Baru</button>
                </div>

                <div id="summaryStats" class="status-summary">
                    <h6>Rekap Status</h6>
                    <div class="status-summary-item">
                        <span>Draft</span>
                        <strong class="badge bg-secondary" id="draftCount">0</strong>
                    </div>
                    <div class="status-summary-item">
                        <span>Reported</span>
                        <strong class="badge bg-secondary" id="reportedCount">0</strong>
                    </div>
                    <div class="status-summary-item">
                        <span>Verified</span>
                        <strong class="badge bg-secondary" id="verifiedCount">0</strong>
                    </div>
                    <div class="status-summary-item">
                        <span>In Progress</span>
                        <strong class="badge bg-secondary" id="inProgressCount">0</strong>
                    </div>
                    <div class="status-summary-item">
                        <span>Resolved</span>
                        <strong class="badge bg-secondary" id="resolvedCount">0</strong>
                    </div>
                </div>
            </aside>

            <main class="main-content">
                <div class="page-header">
                    <div>
                        <div class="text-uppercase text-secondary mb-2">Citizen Dashboard</div>
                        <h1 class="page-title">Portal Laporan Warga</h1>
                        <p class="page-subtitle">Kelola laporan dengan cepat, pantau progress real-time, dan tetap terhubung dengan berita kota.</p>
                    </div>
                    <button class="btn btn-outline-danger logout-btn-top" onclick="logout()">Logout</button>
                </div>

                <div class="d-flex align-items-center gap-3 mb-4">
                    <div id="tabMyReports" class="tab-pill" onclick="loadDashboardData('my_reports', 1)">Laporan Saya</div>
                    <div id="tabFeed" class="tab-pill" onclick="loadDashboardData('feed', 1)">Feed Kota</div>
                </div>

                <div class="content-grid">
                    <div>
                        <div class="report-list" id="listContainer"></div>
                        <div id="paginationContainer" class="mt-3"></div>
                    </div>

                    <aside class="announcement-panel">
                        <h5>Pengumuman</h5>
                        <div id="announcementsContainer"></div>
                    </aside>
                </div>
            </main>
        </div>

        <div class="modal fade" id="reportModal" tabindex="-1" aria-labelledby="reportModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="reportModalLabel">Tambah Laporan Baru</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <form id="reportForm">
                            <div class="mb-3">
                                <label class="form-label">Judul</label>
                                <input id="reportTitle" type="text" class="form-control" placeholder="Masukkan judul laporan">
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Kategori</label>
                                <input id="reportCategory" type="text" class="form-control" placeholder="Masukkan kategori">
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Deskripsi</label>
                                <textarea id="reportDescription" class="form-control" rows="3" placeholder="Masukkan deskripsi laporan"></textarea>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Lokasi</label>
                                <input id="reportLocation" type="text" class="form-control" placeholder="Masukkan lokasi laporan">
                            </div>
                            <div class="d-flex justify-content-between">
                                <button type="button" class="btn btn-outline-secondary" id="btnDraft">Simpan Draft</button>
                                <button type="button" class="btn btn-primary" id="btnSubmit">Ajukan</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
        `;

        loadDashboardData('feed', 1);

    } else {

        app.innerHTML = `
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <div class="container-fluid">
                <span class="navbar-brand">Smart Report</span>
            </div>
        </nav>
        
        <div class="row justify-content-center">

            <div class="col-md-6">

                <div class="card shadow">

                    <div class="card-header bg-primary text-white">
                        Login Citizen Portal
                    </div>

                    <div class="card-body">

                        <form id="loginForm" onsubmit="login(event)">

                            <input
                                type="text"
                                id="loginUsername"
                                class="form-control mb-3"
                                placeholder="Username">

                            <input
                                type="password"
                                id="loginPassword"
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