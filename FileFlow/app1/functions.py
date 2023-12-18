from app1.models import User, Verification
import random, string

def verify(user_email):
    if(type(user_email) != str):
        return False
    VerificationObj = Verification.objects.filter(user_email = user_email).all()
    if len(VerificationObj) == 1:
        return VerificationObj[0]
    return False

def userExists(VerificationObj):
    if(Verification != type(VerificationObj)):
        return False
    UserObj = User.objects.filter(user_email = VerificationObj).all()
    if len(UserObj) == 1:
        return UserObj[0]
    return False

def uniqueIdGenerator():
    id = ''.join(random.choices(string.ascii_letters  + string.digits + string.ascii_uppercase, k =50))
    return id
