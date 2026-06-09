console.log("SPA Lab 11 Berjalan");

let editingReportId = null;
let currentTab = 'feed';
let currentPage = 1;

async function loadDashboardData(tab = 'feed', page = 1) {
    currentTab = tab;
    currentPage = page;

    const response = await requestAPI(`/api/reports/?tab=${tab}&page=${page}`, 'GET');

    if (response && response.status === 200) {
        const data = await response.json();
        const allReports = data.results || [];
        const totalCount = data.count || 0;
        const pageSize = 10;
        const totalPages = Math.max(1, Math.ceil(totalCount / pageSize));

        renderList(allReports, tab);
        renderPagination(page, totalPages, tab);
        setActiveTabButton(tab);
        renderAnnouncements();
        await loadSummaryStats();
        attachDashboardEventListeners();
        return;
    }

    renderList([], tab);
    renderPagination(1, 0, tab);
    setActiveTabButton(tab);
    renderAnnouncements();
    await loadSummaryStats();
}

async function loadSummaryStats() {
    const response = await requestAPI('/api/reports/?tab=my_reports&page_size=1000', 'GET');
    if (!(response && response.status === 200)) return;

    const data = await response.json();
    const reports = data.results || [];

    const draftCount = reports.filter(report => report.status === 'DRAFT').length;
    const reportedCount = reports.filter(report => report.status === 'REPORTED').length;
    const verifiedCount = reports.filter(report => report.status === 'VERIFIED').length;
    const resolvedCount = reports.filter(report => report.status === 'RESOLVED').length;

    document.getElementById('reportedCount').textContent = draftCount;
    document.getElementById('verifiedCount').textContent = reportedCount;
    document.getElementById('inProgressCount').textContent = verifiedCount;
    document.getElementById('resolvedCount').textContent = resolvedCount;
}

function attachDashboardEventListeners() {
    const addReportBtn = document.getElementById('addReportBtn');
    const btnDraft = document.getElementById('btnDraft');
    const btnSubmit = document.getElementById('btnSubmit');

    if (addReportBtn) addReportBtn.onclick = openNewReportModal;
    if (btnDraft) btnDraft.onclick = () => submitReport(false);
    if (btnSubmit) btnSubmit.onclick = () => submitReport(true);
}

function setActiveTabButton(tab) {
    const feedButton = document.getElementById('tabFeed');
    const myReportsButton = document.getElementById('tabMyReports');
    const navFeed = document.getElementById('navFeed');
    const navMyReports = document.getElementById('navMyReports');

    if (feedButton) feedButton.classList.toggle('active', tab === 'feed');
    if (myReportsButton) myReportsButton.classList.toggle('active', tab === 'my_reports');
    if (navFeed) navFeed.classList.toggle('active', tab === 'feed');
    if (navMyReports) navMyReports.classList.toggle('active', tab === 'my_reports');
}

function renderAnnouncements() {
    const announcements = [
        {
            title: 'Update: Banjir Sudirman',
            note: 'Tim respons sudah melakukan verifikasi dan sedang memetakan penanganan lanjutan.',
            status: 'TERVERIFIKASI',
            category: 'Lingkungan & Kebersihan',
            date: '20 Mei'
        },
        {
            title: 'Laporan Keamanan Terbaru',
            note: 'Kasus sedang ditindaklanjuti oleh tim keamanan kota secara real-time.',
            status: 'DILAPORKAN',
            category: 'Keamanan',
            date: '13 Mei'
        },
        {
            title: 'Perbaikan Halte Bus',
            note: 'Akses publik sedang diperbaharui dengan prioritas tinggi.',
            status: 'DIPROSES',
            category: 'Fasilitas Publik',
            date: '13 Mei'
        }
    ];

    const container = document.getElementById('announcementsContainer');
    if (!container) return;

    container.innerHTML = announcements.map(item => `
        <div class="announcement-card">
            <div class="announcement-title">${item.title}</div>
            <div class="announcement-note">${item.note}</div>
            <div class="announcement-meta">
                <div class="announcement-tag">${item.category}</div>
                <span class="announcement-badge">${item.status}</span>
                <span>${item.date}</span>
            </div>
        </div>
    `).join('');
}

function openNewReportModal() {
    editingReportId = null;
    document.getElementById('reportModalLabel').textContent = 'Tambah Laporan Baru';
    document.getElementById('reportForm')?.reset();
    const modalEl = document.getElementById('reportModal');
    if (modalEl) {
        const modal = new bootstrap.Modal(modalEl);
        modal.show();
    }
}

async function editDraft(id) {
    const response = await requestAPI(`/api/reports/${id}/`, 'GET');
    if (!(response && response.status === 200)) return;

    const report = await response.json();
    document.getElementById('reportTitle').value = report.title || '';
    document.getElementById('reportCategory').value = report.category || '';
    document.getElementById('reportDescription').value = report.description || '';
    document.getElementById('reportLocation').value = report.location || '';

    editingReportId = id;
    document.getElementById('reportModalLabel').textContent = 'Edit Draft Laporan';

    const modalEl = document.getElementById('reportModal');
    if (modalEl) {
        const modal = new bootstrap.Modal(modalEl);
        modal.show();
    }
}

async function deleteDraft(id) {
    const confirmed = window.confirm('Yakin ingin menghapus laporan draft ini?');
    if (!confirmed) return;

    const response = await requestAPI(`/api/reports/${id}/`, 'DELETE');
    if (response && response.status === 204) {
        loadDashboardData(currentTab, currentPage);
    }
}

async function submitReport(isSubmit) {
    const title = document.getElementById('reportTitle')?.value || '';
    const category = document.getElementById('reportCategory')?.value || '';
    const description = document.getElementById('reportDescription')?.value || '';
    const location = document.getElementById('reportLocation')?.value || '';
    const status = isSubmit ? 'REPORTED' : 'DRAFT';

    const payload = {
        title,
        category,
        description,
        location,
        status
    };

    const endpoint = editingReportId ? `/api/reports/${editingReportId}/` : '/api/reports/';
    const method = editingReportId ? 'PUT' : 'POST';

    const response = await requestAPI(endpoint, method, payload);
    if (response && (response.status === 200 || response.status === 201)) {
        const modalEl = document.getElementById('reportModal');
        if (modalEl) {
            const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
            modal.hide();
        }
        document.getElementById('reportForm')?.reset();
        editingReportId = null;
        loadDashboardData(currentTab, currentPage);
    }
}

function renderList(reports, tab) {
    const listContainer = document.getElementById('dashboardList');
    if (!listContainer) return;

    if (!reports.length) {
        listContainer.innerHTML = `
            <div class="text-center py-5 text-muted">
                Tidak ada laporan pada tab <strong>${tab}</strong>.
            </div>
        `;
        return;
    }

    listContainer.innerHTML = reports.map(report => {
        const statusText = report.status.replace('_', ' ');
        const statusClass = report.status === 'REPORTED'
            ? 'badge-reported'
            : report.status === 'VERIFIED'
                ? 'badge-verified'
                : report.status === 'IN_PROGRESS'
                    ? 'badge-inprogress'
                    : report.status === 'RESOLVED'
                        ? 'badge-resolved'
                        : 'badge-draft';

        return `
            <div class="report-card">
                <div class="report-card-header">
                    <div>
                        <h5 class="report-card-title">${report.title}</h5>
                        <div class="report-card-meta">
                            <span>📌 ${report.category}</span>
                            <span>📍 ${report.location || 'Lokasi tidak tersedia'}</span>
                        </div>
                    </div>
                    <span class="status-badge ${statusClass}">${statusText}</span>
                </div>
                <div class="report-card-body">${report.description || 'Tidak ada deskripsi tambahan.'}</div>
                <div class="report-card-footer">
                    <div class="text-muted small">Pelapor: ${report.reporter || 'Warga Anonim'}</div>
                    <div class="action-buttons">
                        ${report.status === 'DRAFT' ? `<button type="button" class="btn btn-sm btn-outline-warning" onclick="editDraft(${report.id})">Edit</button>` : ''}
                        ${report.status === 'DRAFT' ? `<button type="button" class="btn btn-sm btn-outline-danger" onclick="deleteDraft(${report.id})">Hapus</button>` : ''}
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

function renderPagination(currentPage, totalPages, tab) {
    const paginationContainer = document.getElementById('paginationContainer');
    if (!paginationContainer) return;

    if (totalPages <= 1) {
        paginationContainer.innerHTML = '';
        return;
    }

    const pages = [];
    const delta = 2;

    for (let page = 1; page <= totalPages; page += 1) {
        if (page === 1 || page === totalPages || (page >= currentPage - delta && page <= currentPage + delta)) {
            pages.push(page);
        } else if (pages[pages.length - 1] !== '...') {
            pages.push('...');
        }
    }

    const buttons = pages.map(page => {
        if (page === '...') {
            return `<span class="pagination-pill disabled">…</span>`;
        }

        const activeClass = page === currentPage ? 'active' : '';
        return `
            <button class="pagination-pill ${activeClass}"
                    type="button"
                    onclick="loadDashboardData('${tab}', ${page})">
                ${page}
            </button>
        `;
    }).join('');

    paginationContainer.innerHTML = `
        <div class="pagination-bar">
            ${currentPage > 1 ? `<button class="pagination-pill" type="button" onclick="loadDashboardData('${tab}', ${currentPage - 1})">Prev</button>` : `<span class="pagination-pill disabled">Prev</span>`}
            ${buttons}
            ${currentPage < totalPages ? `<button class="pagination-pill" type="button" onclick="loadDashboardData('${tab}', ${currentPage + 1})">Next</button>` : `<span class="pagination-pill disabled">Next</span>`}
        </div>
    `;
}
