from django.shortcuts import render, redirect
from rest_framework.views import APIView
from django.http import JsonResponse
from bson import ObjectId
import requests
from datetime import datetime
from .models import UsersData, UsersOTP
import random

# redirect on the sign up page
def sign_up_page(request):
    '''
        API for the redirect on the sign up page
    '''
    return render(request, 'files/signup.html')


# redirect on the login page
def login_up_page(request):
    '''
        API for the redirect on the login page
    '''
    return render(request, 'files/login.html')

# render the user on home page
def home_page(request):
    '''
        API for the redirect on the sign up page
    '''
    return render(request, 'files/homepage.html')


'''
    API for register the user
    request:
    email, password, number and username
    response:
    200 - successfully registered
'''
class UserSignUp(APIView):
    def post(self,request):
        emailId = request.data['email']
        username = request.data['username']
        password = request.data['password']
        number = request.data['number']
        BODY_HTML = "<h4>Hello User,</h4><br><div><p style='margin:0px'>Thank You for signup.</p></div><br><br><p style='margin:0px'></p><br><br><br>"
        print("here your email body", BODY_HTML)

        cursordata = UsersData.objects.filter(email=emailId)
        if cursordata.count() == 0:
            user_details = UsersData(email=emailId, number=number,password=password,username=username)
            user_details.save()
            response = {
                "message": "successfully registered"
            }
            return JsonResponse(response, safe=False, status=200)
        else:
            response = {
                "message": "already register"
            }
            return JsonResponse(response, safe=False, status=409)


'''
    API for send the OTP
'''
class SendOtp(APIView):
    def post(self,request):
        number = request.data['number']
        current_time_stamp = int(datetime.now().timestamp())
        otp = ''.join(random.choice('0123456789') for _ in range(4))
        print("your otp", otp)
        user_details = UsersOTP(number=number, otp=otp,timestamp=current_time_stamp)
        user_details.save()
        response = {
            "message": "successfully registered",
            "otp": otp
        }
        return JsonResponse(response, safe=False, status=200)

'''
    API for get and validate the OTP
'''
class ValidateOtp(APIView):
    def post(self,request):
        number = request.data['number']
        otp = request.data['otp']
        print("your otp", otp)
        cursordata = UsersOTP.objects.filter(number=number, otp=otp)
        if cursordata.count() > 0:
            current_time_stamp = int(datetime.now().timestamp())-60
            for otp_data in cursordata:
                if otp_data.timestamp > current_time_stamp:
                    response = {
                        "message": "successfully"
                    }
                    return JsonResponse(response, safe=False, status=200)
                else:
                    response = {
                        "message": "OTP Expired"
                    }
                    return JsonResponse(response, safe=False, status=404)
        else:
            response = {
                "message": "Please Enter Correct OTP"
            }
            return JsonResponse(response, safe=False, status=422)
