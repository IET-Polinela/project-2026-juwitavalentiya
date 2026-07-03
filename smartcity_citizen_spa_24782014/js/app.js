console.log("SPA Lab 11 Berjalan");

let editingReportId = null;
let currentTab = 'feed';
let currentPage = 1;

async function loadDashboardData(tab = 'feed', page = 1) {
    currentTab = tab;
    currentPage = page;

    const response = await requestAPI(`/api/report/?tab=${tab}&page=${page}`, 'GET');

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
    const response = await requestAPI('/api/report/?tab=my_reports&page_size=1000', 'GET');
    if (!(response && response.status === 200)) return;

    const data = await response.json();
    const reports = data.results || [];

    const draftCount = reports.filter(report => report.status === 'DRAFT').length;
    const reportedCount = reports.filter(report => report.status === 'REPORTED').length;
    const verifiedCount = reports.filter(report => report.status === 'VERIFIED').length;
    const inProgressCount = reports.filter(report => report.status === 'IN_PROGRESS').length;
    const resolvedCount = reports.filter(report => report.status === 'RESOLVED').length;

    document.getElementById('draftCount').textContent = draftCount;
    document.getElementById('reportedCount').textContent = reportedCount;
    document.getElementById('verifiedCount').textContent = verifiedCount;
    document.getElementById('inProgressCount').textContent = inProgressCount;
    document.getElementById('resolvedCount').textContent = resolvedCount;
}

function attachDashboardEventListeners() {
    const btnBukaModal = document.getElementById('btnBukaModal');
    const btnDraft = document.getElementById('btnDraft');
    const btnSubmit = document.getElementById('btnSubmit');

    if (btnBukaModal) btnBukaModal.onclick = openNewReportModal;
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

function showModal(modalEl) {
    if (!modalEl) return;

    if (window.bootstrap && window.bootstrap.Modal) {
        const modal = window.bootstrap.Modal.getOrCreateInstance(modalEl);
        modal.show();
        return;
    }

    modalEl.classList.add('show');
    modalEl.setAttribute('aria-hidden', 'false');
    modalEl.style.display = 'block';
    document.body.classList.add('modal-open');

    if (!document.querySelector('.modal-backdrop')) {
        const backdrop = document.createElement('div');
        backdrop.className = 'modal-backdrop fade show';
        document.body.appendChild(backdrop);
    }
}

function hideModal(modalEl) {
    if (!modalEl) return;

    if (window.bootstrap && window.bootstrap.Modal) {
        const modal = window.bootstrap.Modal.getInstance(modalEl) || window.bootstrap.Modal.getOrCreateInstance(modalEl);
        modal.hide();
        return;
    }

    modalEl.classList.remove('show');
    modalEl.setAttribute('aria-hidden', 'true');
    modalEl.style.display = 'none';
    document.body.classList.remove('modal-open');

    const backdrop = document.querySelector('.modal-backdrop');
    if (backdrop) backdrop.remove();
}

function openNewReportModal() {
    editingReportId = null;
    document.getElementById('reportModalLabel').textContent = 'Buat Laporan Baru';
    document.getElementById('reportForm')?.reset();
    const modalEl = document.getElementById('reportModal');
    showModal(modalEl);
}

async function editDraft(id) {
    const response = await requestAPI(`/api/report/${id}/`, 'GET');
    if (!(response && response.status === 200)) return;

    const report = await response.json();
    document.getElementById('reportTitle').value = report.title || '';
    document.getElementById('reportCategory').value = report.category || '';
    document.getElementById('reportDescription').value = report.description || '';
    document.getElementById('reportLocation').value = report.location || '';

    editingReportId = id;
    document.getElementById('reportModalLabel').textContent = 'Edit Draft Laporan';

    const modalEl = document.getElementById('reportModal');
    showModal(modalEl);
}

async function deleteDraft(id) {
    const confirmed = window.confirm('Yakin ingin menghapus laporan draft ini?');
    if (!confirmed) return;

    const response = await requestAPI(`/api/report/${id}/`, 'DELETE');
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

    const endpoint = editingReportId ? `/api/report/${editingReportId}/` : '/api/report/';
    const method = editingReportId ? 'PUT' : 'POST';

    const response = await requestAPI(endpoint, method, payload);
    if (response && (response.status === 200 || response.status === 201)) {
        const modalEl = document.getElementById('reportModal');
        hideModal(modalEl);
        document.getElementById('reportForm')?.reset();
        editingReportId = null;
        alert(isSubmit ? 'Laporan berhasil diajukan.' : 'Laporan berhasil disimpan sebagai DRAFT');
        loadDashboardData(currentTab, currentPage);
    }
}

function renderList(reports, tab) {
    const listContainer = document.getElementById('listContainer') || document.getElementById('dashboardList');
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
        const statusText = (report.status || 'DRAFT').replace('_', ' ');
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
            <div class="col">
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
                        <div class="text-muted small">Pelapor: ${report.reporter_name || report.reporter || 'Warga Anonim'}</div>
                        <div class="action-buttons">
                            ${report.status === 'DRAFT' ? `<button type="button" class="btn btn-sm btn-outline-warning" onclick="editDraft(${report.id})">Edit</button>` : ''}
                            ${report.status === 'DRAFT' ? `<button type="button" class="btn btn-sm btn-outline-danger" onclick="deleteDraft(${report.id})">Hapus</button>` : ''}
                        </div>
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

    const buildPageItem = (page, label, isDisabled = false, isActive = false) => {
        const disabledClass = isDisabled ? 'disabled' : '';
        const activeClass = isActive ? 'active' : '';
        return `
            <li class="page-item ${disabledClass} ${activeClass}">
                <button class="page-link" type="button" ${isDisabled ? 'disabled' : ''} onclick="loadDashboardData('${tab}', ${page})">
                    ${label}
                </button>
            </li>
        `;
    };

    const buttons = pages.map(page => {
        if (page === '...') {
            return `<li class="page-item disabled"><span class="page-link">…</span></li>`;
        }

        return buildPageItem(page, page, false, page === currentPage);
    }).join('');

    const prevButton = currentPage > 1
        ? buildPageItem(currentPage - 1, 'Sebelumnya')
        : buildPageItem(1, 'Sebelumnya', true);

    const nextButton = currentPage < totalPages
        ? buildPageItem(currentPage + 1, 'Selanjutnya')
        : buildPageItem(totalPages, 'Selanjutnya', true);

    paginationContainer.innerHTML = `
        <nav aria-label="Pagination">
            <ul class="pagination justify-content-center">
                ${prevButton}
                ${buttons}
                ${nextButton}
            </ul>
        </nav>
    `;
}
