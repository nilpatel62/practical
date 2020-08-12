from django.shortcuts import render, redirect
from rest_framework.views import APIView
from django.http import JsonResponse
from bson import ObjectId
import requests
from datetime import datetime
from .models import UsersData, UsersOTP
import random
import json
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session

s = SessionStore() # create the session Object

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


def logout_up_page(request):
    '''
        API for the redirect on the logout page
    '''
    del request.session['token']
    del request.session['number']
    return redirect("/login/")

# render the user on home page
def home_page(request):
    '''
        API for the redirect on the sign up page
    '''
    try:
        user_name = "Guest User"
        token = request.session['token']
        number = request.session['number']
        session = Session.objects.get(pk=token)
        user_details = UsersData.objects.filter(number=number)
        for user in user_details:
            user_name = user.username
            country_flag = user.country
            number = user.number
            email = user.email
        return render(request, 'files/homepage.html', context={"username": user_name, "country_flag": country_flag, "number": number, "email": email})
    except:
        return redirect("/login/")


'''
    API for register the user
    request:
    email, password, number and username
    response:
    200 - successfully registered
'''
class UserSignUp(APIView):
    def post(self,request):
        try:
            emailId = request.data['email']
            username = request.data['username']
            password = request.data['password']
            number = request.data['number']
            ip_address = request.data['ipAddress']
            BODY_HTML = "<h4>Hello User,</h4><br><div><p style='margin:0px'>Thank You for signup.</p></div><br><br><p style='margin:0px'></p><br><br><br>"
            print("here your email body", BODY_HTML)

            cursordata = UsersData.objects.filter(email=emailId)
            if cursordata.count() == 0:
                user_details = UsersData(email=emailId, number=number,password=password,username=username, country=ip_address['country'])
                user_details.save()
                # create the session inside database and store token in cookies
                s['number'] = number
                s.create()
                session_key = s.session_key
                SessionStore(session_key=session_key)
                request.session['token'] = session_key
                request.session['number'] = number
                response = {
                    "message": "successfully registered"
                }
                return JsonResponse(response, safe=False, status=200)
            else:
                response = {
                    "message": "already register"
                }
                return JsonResponse(response, safe=False, status=409)
        except:
            response = {
                "message": "Internal Server Error"
            }
            return JsonResponse(response, safe=False, status=500)


'''
    API for send the OTP
'''
class SendOtp(APIView):
    def post(self,request):
        try:
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
        except:
            response = {
                "message": "Internal Server Error"
            }
            return JsonResponse(response, safe=False, status=500)


'''
    API for get and validate the OTP
'''
class ValidateOtp(APIView):
    def post(self,request):
        try:
            number = request.data['number']
            otp = request.data['otp']
            ip_address = json.loads(request.data['ipAddress'])
            cursordata = UsersOTP.objects.filter(number=number, otp=otp)
            otp_details = UsersOTP.objects.filter(number=number)
            current_time_stamp_otp_block = int(datetime.now().timestamp())-300
            timestamp = int(datetime.now().timestamp())
            user_details = UsersData.objects.filter(number=number)
            if user_details.count() > 0:
                for user in otp_details:
                    if user.incorrect_attempt > 2 and current_time_stamp_otp_block < user.timestamp and timestamp > user.timestamp:
                        response = {
                            "message": "Please After 5 Min"
                        }
                        return JsonResponse(response, safe=False, status=403)
                if cursordata.count() > 0:
                    current_time_stamp = int(datetime.now().timestamp())-60
                    update_time_stamp = int(datetime.now().timestamp())
                    for otp_data in cursordata:
                        if otp_data.timestamp > current_time_stamp:
                            for u in user_details:
                                s['number'] = u.number
                                s.create()
                                session_key = s.session_key
                                SessionStore(session_key=session_key)
                                request.session['token'] = session_key
                                request.session['number'] = u.number
                            UsersOTP.objects.filter(number=number).update(incorrect_attempt=0, timestamp=update_time_stamp)
                            UsersData.objects.filter(number=number).update(country=ip_address['country'])
                            response = {
                                "message": "successfully"
                            }
                            return JsonResponse(response, safe=False, status=200)
                        else:
                            UsersOTP.objects.filter(number=number).update(incorrect_attempt=0, timestamp=update_time_stamp)
                            response = {
                                "message": "OTP Expired"
                            }
                            return JsonResponse(response, safe=False, status=404)
                else:
                    total_attempts = 0
                    cursordata = UsersOTP.objects.filter(number=number)
                    if cursordata.count() > 0:
                        for otp_data in cursordata:
                            total_attempts = otp_data.incorrect_attempt
                    else:
                        total_attempts = 0
                    timestamp = int(datetime.now().timestamp())
                    UsersOTP.objects.filter(number=number).update(incorrect_attempt=int(total_attempts)+1, timestamp=timestamp)
                    response = {
                        "message": "Please Enter Correct OTP"
                    }
                    return JsonResponse(response, safe=False, status=422)
            else:
                response = {
                    "message": "User Not Found With this Number"
                }
                return JsonResponse(response, safe=False, status=404)
        except:
            response = {
                "message": "Internal Server Error"
            }
            return JsonResponse(response, safe=False, status=500)