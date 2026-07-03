from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):

    reporter = serializers.SerializerMethodField()
    reporter_name = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = '__all__'

    def get_reporter(self, obj):
        return 'Warga Anonim'

    def get_reporter_name(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            if obj.reporter == request.user:
                return obj.reporter.username
        return 'Warga Anonim'

    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            return obj.reporter == request.user
        return False