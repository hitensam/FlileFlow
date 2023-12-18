import random
import smtplib
from app1.models import Verification

def sendEmail(email): 
   server=smtplib.SMTP('smtp.gmail.com',587)
   password = "some_pass";  
   sender_email = "youremail@domain.com"
   #adding TLS security 
   server.starttls()
   server.login(sender_email,password)
   #generate OTP using random.randint() function
   otp=''.join([str(random.randint(0,9)) for i in range(4)])
   VerificationObj = Verification.objects.filter(user_email = email).get()
   VerificationObj.otp_sent = int(otp)
   VerificationObj.save()
   msg='Hello, Your OTP is '+str(otp)
   msg = 'Subject: {}\n\n{}'.format("FileFlow Email Verification", msg)
   receiver=email #write email of receiver
   #sendi
   server.sendmail(sender_email,receiver,msg)
   server.quit()
