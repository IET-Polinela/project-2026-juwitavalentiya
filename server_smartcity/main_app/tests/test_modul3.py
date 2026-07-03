from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from main_app.models import Report

# ─────────────────────────────────────────────────────────────────────────────
# PENJELASAN: get_user_model()
# ─────────────────────────────────────────────────────────────────────────────
# Django mendukung custom user model melalui setting AUTH_USER_MODEL.
# Pada proyek ini, user model kustom didefinisikan di usermanagement.User.
# Menggunakan get_user_model() memastikan kita selalu mereferensikan model
# user yang benar, bukan django.contrib.auth.models.User bawaan.
# ─────────────────────────────────────────────────────────────────────────────
User = get_user_model()

# =============================================================================
# MODUL 3: PENGUJIAN ALUR KERJA & ATURAN BISNIS STATUS LAPORAN
# =============================================================================
# Fokus: Memastikan transisi status laporan mengikuti aturan state machine:
#   DRAFT -> REPORTED -> VERIFIED -> IN_PROGRESS -> RESOLVED
#
# Aturan kunci:
#   - Hanya pemilik draf yang bisa memodifikasi laporan berstatus DRAFT
#   - Laporan yang sudah REPORTED tidak bisa diubah kontennya oleh warga
#   - Laporan RESOLVED bersifat read-only (tidak bisa diubah siapa pun)
#   - Admin hanya bisa melakukan transisi maju, BUKAN lompat status
# =============================================================================

class WorkflowStateTests(APITestCase):
    """
    Kelas pengujian untuk alur kerja dan transisi status laporan via REST API.

    Menguji aturan bisnis terkait kapan laporan boleh dimodifikasi dan
    bagaimana status berubah sesuai alur yang telah ditentukan.
    """

    def setUp(self):
        """
        Persiapan: Buat satu warga dan beberapa laporan dengan status berbeda
        untuk menguji aturan transisi status.
        """
        self.warga = User.objects.create_user(
            username='warga_wf', password='TestPass123!', is_admin=False
        )

        # Laporan berstatus DRAFT — bisa dimodifikasi oleh pemilik
        self.laporan_draft = Report.objects.create(
            title='Lampu Kampus Mati',
            category='Fasilitas Umum',
            description='Lampu di depan gedung rektorat tidak menyala.',
            location='Gedung Rektorat',
            status='DRAFT',
            reporter=self.warga,
        )

        # Laporan berstatus REPORTED — sudah masuk antrean, TIDAK bisa diubah
        self.laporan_reported = Report.objects.create(
            title='Saluran Air Tersumbat',
            category='Infrastruktur',
            description='Saluran air di samping kantin tersumbat.',
            location='Kantin Polinela',
            status='REPORTED',
            reporter=self.warga,
        )

        # Laporan berstatus RESOLVED — sudah selesai, bersifat READ-ONLY
        self.laporan_resolved = Report.objects.create(
            title='AC Rusak di Lab',
            category='Fasilitas Umum',
            description='AC di Lab CPS 1 sudah diperbaiki.',
            location='Lab CPS 1',
            status='RESOLVED',
            reporter=self.warga,
        )

    # ─────────────────────────────────────────────────────────────────────────
    # WF-01: Warga Mengajukan Laporan (DRAFT → REPORTED)
    # ─────────────────────────────────────────────────────────────────────────
    def test_WF_01_warga_mengajukan_draf_menjadi_reported(self):
        """
        [WF-01] Warga menekan tombol ajukan laporan pada data berstatus DRAFT.
        """
        self.client.force_authenticate(user=self.warga)

        url = f'/api/report/{self.laporan_draft.pk}/'
        payload = {
            'title': self.laporan_draft.title,
            'category': self.laporan_draft.category,
            'description': self.laporan_draft.description,
            'location': self.laporan_draft.location,
            'status': 'REPORTED',  # Modifikasi dari DRAFT ke REPORTED
        }

        response = self.client.put(url, payload, format='json')

        # Verifikasi: PUT berhasil dengan HTTP 200
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            "Pengajuan draf ke REPORTED seharusnya berhasil (HTTP 200)"
        )

        # Verifikasi: Status di database benar-benar berubah
        self.laporan_draft.refresh_from_db()
        self.assertEqual(
            self.laporan_draft.status,
            'REPORTED',
            "Status laporan di database harus berubah menjadi 'REPORTED'"
        )

    # ─────────────────────────────────────────────────────────────────────────
    # WF-02: Warga Tidak Bisa Mengubah Konten Laporan yang Sudah REPORTED
    # ─────────────────────────────────────────────────────────────────────────
    def test_WF_02_tidak_bisa_edit_laporan_yang_sudah_reported(self):
        """
        [WF-02] Warga mencoba memperbarui teks konten laporan yang sudah
        berstatus REPORTED via API.
        """
        self.client.force_authenticate(user=self.warga)

        url = f'/api/report/{self.laporan_reported.pk}/'
        payload = {
            'title': 'Judul Diubah Setelah Dikirim',
            'category': self.laporan_reported.category,
            'description': 'Mencoba mengubah deskripsi secara ilegal.',
            'location': self.laporan_reported.location,
            'status': 'REPORTED',
        }

        response = self.client.put(url, payload, format='json')

        # Verifikasi: Harus mengembalikan 403 Forbidden karena status bukan DRAFT lagi
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
            "Warga seharusnya ditolak (403) saat mengedit laporan yang sudah berstatus REPORTED"
        )

    # ─────────────────────────────────────────────────────────────────────────
    # WF-05: Laporan RESOLVED Bersifat Read-Only
    # ─────────────────────────────────────────────────────────────────────────
    def test_WF_05_laporan_resolved_tidak_bisa_diubah(self):
        """
        [WF-05] Pengguna mencoba mengirimkan modifikasi data pada laporan 
        yang sudah berstatus RESOLVED.
        """
        self.client.force_authenticate(user=self.warga)

        url = f'/api/report/{self.laporan_resolved.pk}/'
        payload = {
            'title': 'Mengubah Laporan Selesai',
            'category': self.laporan_resolved.category,
            'description': 'Mencoba membuka kembali atau mengubah data.',
            'location': self.laporan_resolved.location,
            'status': 'RESOLVED',
        }

        response = self.client.put(url, payload, format='json')

        # Verifikasi: Harus mengembalikan status 403 Forbidden karena RESOLVED dikunci
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
            "Laporan berstatus RESOLVED harus bersifat read-only dan mengembalikan 403"
        )


# =============================================================================
# MODUL 3b: PENGUJIAN ADMIN PORTAL — TRANSISI STATUS
# =============================================================================

class AdminWorkflowTests(TestCase):
    """
    Kelas pengujian untuk portal admin (Django monolithic views).
    """

    def setUp(self):
        """
        Persiapan: Buat admin user dan beberapa laporan untuk menguji
        transisi status di portal admin.
        """
        self.admin = User.objects.create_user(
            username='admin_portal',
            password='AdminPass123!',
            is_admin=True,
            is_staff=True,
        )

        # Laporan REPORTED — menunggu verifikasi oleh admin
        self.laporan_reported = Report.objects.create(
            title='Jalan Rusak di Blok C',
            category='Infrastruktur',
            description='Jalan berlubang parah di area parkir Blok C.',
            location='Blok C Polinela',
            status='REPORTED',
            reporter=self.admin,
        )

    # ─────────────────────────────────────────────────────────────────────────
    # WF-03: Admin Mengubah Status REPORTED menjadi VERIFIED
    # ─────────────────────────────────────────────────────────────────────────
    def test_WF_03_admin_mengubah_status_reported_ke_verified(self):
        """
        [WF-03] Admin mengubah status laporan dari REPORTED menjadi VERIFIED
        melalui UI Portal Admin.
        """
        # Melakukan login ke session auth Django Monolitik
        self.client.login(username='admin_portal', password='AdminPass123!')

        # Mengakses view atau endpoint update status di admin portal
        # Menggunakan format URL reverse jika nama rutenya ada, atau hardcoded path view
        url = reverse('update_report_status', kwargs={'pk': self.laporan_reported.pk})
        
        response = self.client.post(url, {'new_status': 'VERIFIED'})

        # Verifikasi redirect (302 Found) kembali ke halaman dashboard atau detail setelah sukses
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        # Verifikasi perubahan tersimpan dengan sukses ke basis data
        self.laporan_reported.refresh_from_db()
        self.assertEqual(
            self.laporan_reported.status,
            'VERIFIED',
            "Admin seharusnya berhasil mengubah status laporan dari REPORTED menjadi VERIFIED"
        )

    # ─────────────────────────────────────────────────────────────────────────
    # WF-04: Tidak Ada Tombol Langsung ke RESOLVED dari REPORTED
    # ─────────────────────────────────────────────────────────────────────────
    def test_WF_04_tidak_ada_transisi_langsung_ke_resolved_dari_reported(self):
        """
        [WF-04] Memeriksa pembatasan transisi status agar tidak bisa melompat.
        """
        self.client.login(username='admin_portal', password='AdminPass123!')

        # Mencoba memaksa melompat status langsung dari REPORTED ke RESOLVED via POST request
        url = reverse('update_report_status', kwargs={'pk': self.laporan_reported.pk})
        
        # Pengiriman transisi ilegal (lompat status)
        response = self.client.post(url, {'new_status': 'RESOLVED'})

        # Verifikasi: Sistem menolak transisi ilegal dengan mengembalikan status kode error (misal 400 Bad Request)
        # atau mengabaikan dan mempertahankan status lama (bergantung pada implementasi view)
        self.laporan_reported.refresh_from_db()
        self.assertNotEqual(
            self.laporan_reported.status,
            'RESOLVED',
            "Sistem tidak boleh mengizinkan transisi status melompat langsung dari REPORTED ke RESOLVED"
        )