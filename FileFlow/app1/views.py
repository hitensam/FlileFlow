from django.http import FileResponse
from rest_framework.response import Response #rendering JSON
from rest_framework.decorators import api_view #function based views are used.
from  app1.serializers import *
from app1.models import *
from app1 import sendOTP
from app1.functions import *
import bcrypt

import os

@api_view(['POST'])
def shareFile(request):  #requesting to share a file with another user.
    if(request.method == "POST"):
        serializer = ShareFileSerializer(data=request.data)
        serializer.is_valid()
        if(serializer.is_valid() == False):
            return Response({"message" : "INVALID_REQUEST_FORMAT"})
        user_email = serializer.validated_data['user_email']
        user2_email = serializer.validated_data['user2_email']
        
        if(user_email == user2_email):
            return Response({"message" : "BOTH_SAME_EMAIL"})
        
        session_id = serializer.validated_data['session_id']
        file_id = serializer.validated_data['file_id']
        verificationObj = verify(user_email=user_email)
        if verificationObj:
            userObj = userExists(verificationObj)
            
            if userObj:
                if(userObj.user_ops_access == False):
                    return Response({"message": "NO_UPLOAD_ACCESS_SO_CANT_SHARE"})
                loggedObj = Logged.objects.filter(user_email = verificationObj, session_id = session_id).all()
                if len(loggedObj) == 1:
                    verificationObj2 = verify(user_email=user2_email)
                    if verificationObj2:
                        fileObj = File.objects.filter(file_id = file_id).all()
                        if len(fileObj) == 1:
                            shareObj = Sharing.objects.filter(user_file = fileObj[0], user_access = verificationObj2).all()
                            if len(shareObj) > 0:
                                return Response({"message" : "FILE_ALREADY_SHARED"})
                            shareObj = Sharing(user_file = fileObj[0], user_access = verificationObj2)
                            shareObj.save()
                            return Response({"message": "FILE_SHARE_SUCCESSFUL"})


    return Response({'message' : "ERROR"})

@api_view(["POST"]) #all shared file to any user will be visible.
def sharedFiles(request):
    if (request.method == "POST"):
        serializer = VerifiedUserSerializer(data=request.data)
        serializer.is_valid()
        if(serializer.is_valid() == False):
            return Response({"message" : "INVALID_REQUEST_FORMAT"})
        user_email = serializer.validated_data['user_email']
        session_id = serializer.validated_data['session_id']
        
        verificationObj = verify(user_email=user_email)
        if verificationObj and verificationObj.user_verified:
            userObj = userExists(verificationObj)
            if userObj:
                loggedObj = Logged.objects.filter(user_email = verificationObj, session_id = session_id).all()
                if len(loggedObj) == 1:
                    shareObj = Sharing.objects.filter(user_access = verificationObj).all()
                    if len(shareObj) == 0:
                        return Response({'message': 'NO_FILES_SHARED_WITH_YOU'})
                    fileObj = []
                    for x in shareObj: 
                        fileObj.append(x.user_file) #excpected error.
                    serializer = FileSerializer(fileObj, many=True)
                    return Response(serializer.data)

        return Response({"message": "ERROR"})

@api_view(["GET"]) 
def download_file(request,download_file_id=0):
    if(download_file_id==0):
        return Response({"message": "ID_NOT_SPECIFIED"})
    DownloadObj = DownloadFile.objects.filter(download_file_id = download_file_id).all()
    if len(DownloadObj) == 0:
        return Response({"message" : "INVAILD_ID"})
    fileObj = DownloadObj[0].file
    # response = FileResponse(open(f'D:/Desktop/Project-EZ/FileFlow/media/{fileObj.file_stored}', 'rb'))
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media', f'{fileObj.file_stored}')
    print(file_path)
    response = FileResponse(open(file_path, 'rb'))
    DownloadObj[0].delete()
    return response

@api_view(["POST"])
def downloadRequest(request):
    if(request.method == "POST"):
        serializer = DownloadFileSerializer(data = request.data)
        # print(request.data)
        # serializer.is_valid()
        # print(serializer.errors)
        serializer.is_valid()
        if(serializer.is_valid() == False):
            return Response({"message" : "INVALID_REQUEST_FORMAT"})
        user_email = serializer.validated_data['user_email']
        session_id = serializer.validated_data['session_id']
        file_id = serializer.validated_data['file_id']
        verificationObj = verify(user_email=user_email)
        if verificationObj and verificationObj.user_verified:
            userObj = userExists(verificationObj)
            if userObj:
                loggedObj = Logged.objects.filter(user_email = verificationObj, session_id = session_id).all()
                if len(loggedObj) == 1:
                    fileObj = File.objects.filter(file_id = file_id).all()
                    if len(fileObj) == 1:
                        unq_id = uniqueIdGenerator()
                        DownloadObj = DownloadFile.objects.filter(download_file_id=unq_id).all()
                        while len(DownloadObj) != 0:
                            unq_id = uniqueIdGenerator()
                            DownloadObj = DownloadFile.objects.filter(download_file_id=unq_id).all()
                        DownloadObj = DownloadFile(download_file_id = unq_id, file = fileObj[0])
                        DownloadObj.save()
                        return Response({"message" : f"/download-file/{unq_id}"})
        
    return Response({"messaage" : "ERROR_OCCURED"})

@api_view(["POST"])
def getAllFiles(request):
    if (request.method == "POST"):
        serializer = VerifiedUserSerializer(data=request.data)
        serializer.is_valid()
        if(serializer.is_valid() == False):
            return Response({"message" : "INVALID_REQUEST_FORMAT"})
        user_email = serializer.validated_data['user_email']
        session_id = serializer.validated_data['session_id']
        
        verificationObj = verify(user_email=user_email)
        if verificationObj and verificationObj.user_verified:
            userObj = userExists(verificationObj)
            if userObj:
                loggedObj = Logged.objects.filter(user_email = verificationObj, session_id = session_id).all()
                if len(loggedObj) == 1:
                    fileObj = File.objects.filter(user_email = verificationObj).all()
                    serializer = FileSerializer(fileObj, many=True)
                    return Response(serializer.data)

        return Response({"message": "ERROR"})

@api_view(["POST"])
def uploadFile(request):
    allowed_file_types = ['xlsx', 'pptx', 'docx']
    serializer = UploadFilesSerializer(data=request.data)
    
    serializer.is_valid()

    if serializer.is_valid():
        uploaded_file = request.data['file']
        print("upload file: ", uploaded_file.name.split()[0])
        file_extension = uploaded_file.name.lower().split('.')[-1]
        print("file_extension: ",file_extension)
 
        if file_extension not in allowed_file_types:
            return Response(
                {'message': f'Invalid file type. Allowed types: {", ".join(allowed_file_types)}'}
            )

        user_email = serializer.validated_data['user_email']
        session_id = serializer.validated_data['session_id']

        print(user_email, " ", session_id)

        VerificationObj = verify(user_email=user_email)

        if VerificationObj and VerificationObj.user_verified:
            userObj = userExists(VerificationObj=VerificationObj)
            print(userObj)
            if(userObj == False or userObj.user_ops_access == False):
                return Response({"message": "NO_UPLOAD_ACCESS"})
            
            LoggedObj = Logged.objects.filter(user_email = VerificationObj, session_id = session_id).all()
            
            if len(LoggedObj)==1:
                unq_id = uniqueIdGenerator()
                fileObj = File.objects.filter(file_id = unq_id).all()
                while len(fileObj) != 0:
                    unq_id = uniqueIdGenerator()
                    fileObj = File.objects.filter(file_id = unq_id).all()
                    
                fileObj = File(user_email = VerificationObj, file_id = unq_id, file_stored = uploaded_file )
                fileObj.save()
                return Response({"message": "FILE_STORE_SUCCESS"})

        return Response({"message": "FAIL"})
    else:
        return Response({"message" : "INVALID_REQUEST_FORMAT"})
        # return Response(serializer.errors)
    
@api_view(["POST"])
def logIn(request):
    if(request.method == "POST"):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid()
        if(serializer.is_valid() == False):
            return Response({"message" : "INVALID_REQUEST_FORMAT"})
        user_email = serializer.validated_data["user_email"]
        user_pass = serializer.validated_data["user_pass"]

        VerificationObj = verify(user_email=user_email)
        if VerificationObj == False:
            return Response({"message": "USER_DOES_NOT_EXIST"})

        UserObj = userExists(VerificationObj=VerificationObj)
        if UserObj:
            if bcrypt.checkpw(user_pass.encode('utf-8'), UserObj.user_pass[2:62].encode('utf-8')):
                LoggedObj = Logged.objects.filter(user_email = VerificationObj).all()
                if len(LoggedObj)>0:
                    LoggedObj.delete()
                session_id = uniqueIdGenerator()
                while len(Logged.objects.filter(session_id = session_id).all()) != 0:
                    session_id = uniqueIdGenerator()
                    LoggedObj = Logged.objects.filter(session_id = session_id).all()
                LoggedObj = Logged(user_email = VerificationObj)
                LoggedObj.session_id = session_id
                LoggedObj.save();
                return Response({"message" : "VERIFICATION_SUCCESS"
                    ,"session_id": f"{session_id}"})
            else:
                return Response({"message":"VERIFICATION_FAILED"})
        else:
            return Response({"message":"ERROR_OCCURED"})
    else:
        return Response({"message": "POST_REQ_ONLY"})
    
@api_view(["POST"])
def signUp(request):
    if(request.method == "POST"):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid()
        if(serializer.is_valid() == False):
            return Response({"message" : "INVALID_REQUEST_FORMAT"})
        user_email = serializer.validated_data["user_email"]
        verificationObj = verify(user_email=user_email)
        userObj = userExists(verificationObj)
        if(verificationObj and userObj == False):
            user_pass = serializer.validated_data["user_pass"]
            encoding = "utf-8"  # The target encoding
            hashed = bcrypt.hashpw(user_pass.encode(encoding), bcrypt.gensalt())
            userObj = User(user_email = verificationObj, user_pass = hashed)
            userObj.save()
            return Response({"message": f"{user_email}_SIGNUP_SUCCESS"})

        else:
            return Response({"message": "FAIL"})


@api_view(["POST"])
def userVerifySendOTP(request):
    if(request.method == "POST"):
        serializer = UserVerifySendOTP(data=request.data)
        serializer.is_valid()
        if(serializer.is_valid() == False):
            return Response({"message" : "INVALID_REQUEST_FORMAT"})
        user_email = serializer.validated_data['user_email']
        VerificationObj = verify(user_email=user_email)
        if VerificationObj:
            if(VerificationObj.user_verified):
                return Response({"message" : "EMAIL_ALREADY_VERIFIED"})
            sendOTP.sendEmail(user_email)
        else:
            sendVerification = Verification(user_email = user_email)
            sendVerification.save()
            sendOTP.sendEmail(user_email)

        return Response({"message":"OTP_SENT"})


@api_view(["POST"])
def userVerifyOTP(request):
    if(request.method == "POST"):
        serializer = UserVerifyOTPSerializer(data=request.data)
        serializer.is_valid()
        if(serializer.is_valid() == False):
            return Response({"message" : "INVALID_REQUEST_FORMAT"})
        user_email = serializer.validated_data["user_email"]
        otp_recvd = serializer.validated_data["otp_recvd"]
        VerificationObj = Verification.objects.filter(user_email = user_email, otp_sent = otp_recvd).all()
        if(len(VerificationObj) == 1):
            VerificationObj = Verification.objects.filter(user_email = user_email, otp_sent = otp_recvd).get()
            VerificationObj.user_verified = True
            VerificationObj.save()

            return Response ({"message":f"{user_email}_VERIFIED"})

        else:
            return Response({"message": "VERIFICATION_FAILED"})
