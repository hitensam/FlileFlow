from django.db import models


class Verification(models.Model):
    user_email = models.CharField(primary_key = True, max_length = 50)
    otp_sent = models.IntegerField(null=True)
    user_verified  = models.BooleanField(default = False)
    #can also store account creation date.
    
    def __str__(self) -> str:
        return f"""user_email: {self.user_email}
                   user_verified: {self.user_verified}
                   otp_sent: {self.otp_sent}"""

class User(models.Model):
    user_email = models.ForeignKey(Verification, null=False, on_delete=models.CASCADE)
    user_pass = models.CharField(null=False, max_length = 60)
    user_ops_access = models.BooleanField(default = False)

    def __str__(self) -> str:
        return f"""{self.user_email}
                   user_pass: {self.user_pass}
                   user_ops_access: {self.user_ops_access}"""

class File(models.Model):
    user_email = models.ForeignKey(Verification, null=False, on_delete=models.CASCADE)
    file_id = models.CharField(primary_key=True,max_length=60)
    file_stored = models.FileField(upload_to="upload_files", blank=True)

    def __str__(self) -> str:
        return f"""user_email: {self.user_email}
                   file_id: {self.file_id}
                   file_stored: {self.file_stored}"""
    

class Sharing(models.Model):
    user_file = models.ForeignKey(File, null=False, on_delete=models.CASCADE)
    user_access = models.ForeignKey(Verification, null=False, on_delete = models.CASCADE)


    def __str__(self) -> str:
        return f"""user_file: {self.user_email}
                   user_access: {self.user_email.user_ops_access}"""

class Logged(models.Model):
    user_email = models.ForeignKey(Verification, on_delete = models.CASCADE)
    session_id = models.CharField(max_length=50, null=False)
    #can also store login time, etc.

    def __str__(self) -> str:
        return f"""{self.user_email}
                   session_id: {self.session_id}
        """
    
class DownloadFile(models.Model):
    file = models.ForeignKey(File, null=False, on_delete = models.CASCADE)
    download_file_id = models.CharField(primary_key=True,max_length=60)

    def __str__(self) -> str:
        return f"""{self.file}
                    downlod_file_id: {self.download_file_id}
                """