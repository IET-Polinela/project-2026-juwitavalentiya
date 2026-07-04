from django.contrib import admin
from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    # Field 'reporter' sengaja TIDAK dimasukkan ke list_display maupun form,
    # supaya identitas pelapor tetap anonim bahkan untuk staff yang mengakses
    # halaman Django admin bawaan (/admin/).
    list_display = ('title', 'category', 'status', 'location', 'created_at')
    list_filter = ('status', 'category')
    search_fields = ('title', 'location', 'description')
    readonly_fields = ('created_at', 'updated_at')

    # Sembunyikan field reporter sepenuhnya dari form tambah/edit di admin
    exclude = ('reporter',)