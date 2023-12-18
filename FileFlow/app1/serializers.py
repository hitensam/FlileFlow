from rest_framework import serializers #so that reponse can understand.
from app1.models import File

class UserSerializer(serializers.Serializer):
    user_email = serializers.CharField()
    user_pass = serializers.CharField()


class UserVerifySendOTP(serializers.Serializer):
    user_email = serializers.CharField()


class UserVerifyOTPSerializer(serializers.Serializer):
    user_email = serializers.CharField()
    otp_recvd = serializers.IntegerField()


class UploadFilesSerializer(serializers.Serializer):
    user_email = serializers.CharField()
    session_id = serializers.CharField()
    file = serializers.FileField()

class VerifiedUserSerializer(serializers.Serializer):
    user_email = serializers.CharField()
    session_id = serializers.CharField()

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('file_id', 'file_stored')


class ShareFileSerializer(serializers.Serializer):
    user_email = serializers.CharField()
    session_id = serializers.CharField()
    user2_email = serializers.CharField()
    file_id = serializers.CharField()


class DownloadFileSerializer(serializers.Serializer):
    user_email = serializers.CharField()
    session_id = serializers.CharField()
    file_id = serializers.CharField()