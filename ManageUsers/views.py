# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages

from ManageUsers.models import CustomUser
from ManageUsers.forms import EditProfileForm, EditCustomProfileForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm

import pyrebase


config = {
  "apiKey": "AIzaSyC93lHUOdfHA3Rqh4QcqmPRv_pmIXgICQE",
  "authDomain": "armygraphgt.firebaseapp.com",
  "databaseURL": "https://armygraphgt.firebaseio.com",
  "storageBucket": "armygraphgt.appspot.com",
  "serviceAccount": "armygraphgt-firebase-adminsdk-x421y-5d8adb2fec.json"
}



firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database=firebase.database()



def signup(request):
    if(request.method=="POST"):
        username = request.POST["username"]
        password1 = request.POST["password"]
        password2 = request.POST["password2"]
        first_name = request.POST["fname"]
        last_name = request.POST["lname"]
        email = request.POST["email"]
        address = request.POST["address"]
        university = request.POST["university"]
        regiment = request.POST["regiment"]
        attended = {}

        try:      
            user = authe.create_user_with_email_and_password(email, password1)
            uid = user['localId']



        except: 
            message="Unable to create account"
            return render(request, 'signup.html', {'message':message})

        
        data = {"email":email, "username":username, "first_name":first_name, "last_name":last_name, "address":address, "university":university, "regiment":regiment}
        database.child("users").child(uid).child("details").set(data)


        
        return render(request, 'home.html', {"e":"Welcome: "+email})

    else:
        return render(request, "signup.html")




def login(request):
    if(request.method=="POST"):
        email=request.POST['email']
        password=request.POST['password']

        try:
            user = authe.sign_in_with_email_and_password(email, password)

            user = authe.refresh(user['refreshToken'])
        except:
            return render(request, "login.html", {"message": "Incorrect Information"})

        print("Success!")
        session_id = user['idToken']
        request.session['uid'] = str(session_id)
        print(authe.get_account_info(session_id))



        return render(request, 'home.html',)
    else:
        return render(request, 'login.html')

def logout(request):
    if(request.method=="POST"):
        
        try: 
            del request.session['uid']
           #del request.session['username']
        except KeyError:
            print("error")
            pass

        return render(request, "login.html")
    else:
        return render(request, 'logout.html')


def edit_profile(request):
    if(request.method=="POST"):
           
        try:
            address = request.POST.get('address')
            phone = request.POST.get('phone')
            university = request.POST.get('university')

            print(request.session['uid'])
            idtoken = request.session['uid']
            
            a = authe.get_account_info(idtoken)
            a = a['users']
            a = a[0]
            a = a['localId']
            print("info" + str(a))

            database.child("users").child(a).child('details').update({'address':address, 'phone':phone, 'university':university})
            print("\nFinished Updating")
            
            #user = adminauth.update_user(idtoken, email=email) #https://firebase.google.com/docs/auth/admin/manage-users#update_a_user
            #print('Successfully updated user: {0}'.format(user.uid))
            
            return render(request, "home.html")
        except KeyError:
            return render(request, "login.html", {"message": "Please Sign In Again!"})

    else:
        return render(request, 'edit_profile.html') 

def create_event(request):
    if(request.method == "POST"):
        try:
            eventname = request.POST.get('eventname')
            city = request.POST.get('city')
            events = database.child("events").get()

            exists = False
            for eventid, items in events.val().items():
                existingName = database.child("events").child(eventid).child("eventname").get().val()
                existingCity = database.child("events").child(eventid).child("city").get().val()
                
                if(existingName==eventname and existingCity==city):
                    exists = True
                
            if not exists:
                data = {'eventname':eventname, "city": city}
                database.child("events").push(data)
                return render(request, "new_event.html", {"message": "Event Added!"})
                
            else:
                return render(request, "new_event.html", {"message": "Event already exists!"})

        except KeyError:
            return render(request, "new_event.html", {"message": "Enter proper values for event fields!"})
    else:
        return render(request, 'new_event.html')

def join_event(request):


    #Get all events
    print( database.child("events").get())  ##Weird error if you take this out!!  StackOverflow?
    events = database.child("events").get()

    eventList = []
    print(events.val().items)
    for eventID, eventDetails in events.val().items():
        eventName = database.child("events").child(eventID).child("eventname").get().val()
        eventCity = database.child("events").child(eventID).child("city").get().val()
        eventList.append((eventName, eventCity, eventID))
    print(eventList)


    if (request.method == "POST"):
        print("In Post")
        try:
            IDToJoin = request.POST.get("event", None)
            #Get User's first and last name
            idtoken = request.session['uid']
            
            a = authe.get_account_info(idtoken)
            a = a['users']
            a = a[0]
            a = a['localId']

            userFirstName = database.child("users").child(a).child("details").child("first_name").get().val()

            userLastName = database.child("users").child(a).child("details").child("last_name").get().val() 
            nameToAdd = (userFirstName, userLastName)


            if IDToJoin is not None:

                try:
                    print("Id to join:" + IDToJoin)
                    attended = database.child("events").child(IDToJoin).child("attended").get()
                    attended = attended.val()
                    if nameToAdd not in attended:
                        attended.append(nameToAdd)
                        database.child("events").child(IDToJoin).update({'attended': attended})
                except Exception as e:
                    print(e)
                    database.child("events").child(IDToJoin).update({'attended': [nameToAdd]})


            #Render Page
            return render(request, "join_event.html", {"events":eventList})

        except KeyError:
            return render(request, "login.html", {"message" : "Please Log In!"})
    else:    
        #Render page
        return render(request, "join_event.html", {"events":eventList})

def find_university(request):
    studentsAttending = []
    if (request.method == "POST"):
        try:
            searchFor = request.POST.get("uniName")
            
            users = database.child("users").get()
            for userid, items in users.val().items():

                universityResponse = database.child("users").child(userid).child("details").child("university").get()
                universityName = universityResponse.val()

                if(universityName == searchFor):

                    matchedFirstName = database.child("users").child(userid).child("details").child("first_name").get().val()
                    matchedLastName = database.child("users").child(userid).child("details").child("last_name").get().val()
                    
                    nameofAttendee = (matchedFirstName, matchedLastName)
                    studentsAttending.append(nameofAttendee)

        except:
            return render(request, 'find_university.html', {"message":"An error occured!  Please try again."} )

        if(len(studentsAttending) <= 0):
            return render(request, "find_university.html", {"message": "No users are attending this university!"})
        else:
            return render(request, "find_university.html", {"message": studentsAttending})
            
    else:
        return render(request, "find_university.html")
            


def get_relations(request):
    if (request.method == "POST"):
        try:
            idtoken = request.session['uid']
            a = authe.get_account_info(idtoken)
            a = a['users']
            a = a[0]
            a = a['localId'] 
            email = request.POST.get("email")
            print(database.child("users").child(a).child("details").child("email").get().val() != email) ##Weird error if you take this out!!  StackOverflow?
            if (database.child("users").child(a).child("details").child("email").get().val() != email):
                raise KeyError
            #First get all matches with universities
            name = database.child("users").child(a).child("details").child("first_name").get().val() + " " + database.child("users").child(a).child("details").child("last_name").get().val()

            uni_matches = []
            uni = database.child("users").child(a).child("details").child("university").get().val()
            users = database.child("users").get()
            for userid, items in users.val().items():
                uniResponse = database.child("users").child(userid).child("details").child("university").get()
                uniName = uniResponse.val()
                if (uni == uniName):
                    matchedFirstName = database.child("users").child(userid).child("details").child("first_name").get().val()
                    matchedLastName = database.child("users").child(userid).child("details").child("last_name").get().val()
                    if(matchedFirstName + " " + matchedLastName != name):
                        uni_matches.append((matchedFirstName, matchedLastName, uni))
            #All matches for events
            event_matches = []
            events = database.child("events").get()
            for eventId, eventDetails in events.val().items():
                try:
                    if (not(database.child("events").child(eventid).child("attended").get() is None)):
                        contains = False
                        for n in database.child("events").child(eventid).child("attended").get().val():
                            if (n[0] + " " + n[1] == name):
                                contains = True
                                break
                        if contains:
                            for n in database.child("events").child(eventid).child("attended").get().val():
                                if (n[0] + " " + n[1] != name):
                                    event_matches.append((n[0], n[1], database.child("events").child(eventid).child("eventname").get().val()))
                except Exception:
                    pass
            out = uni_matches + event_matches
            print(uni_matches)
            print(event_matches)
            if (len(out) <= 0):
                return render(request, "get_relations.html", {"message": "No users are attending your university!"})
            else:
                return render(request, "get_relations.html", {"message": out})  
        except KeyError as e:

            return render(request, "login.html", {"message" : "Please Log In!"})            
    else:
        return render(request, "get_relations.html",)


def find_info(request):
    if (request.method == "POST"):
        try:

            idtoken = request.session['uid']
            a = authe.get_account_info(idtoken)
            a = a['users']
            a = a[0]
            a = a['localId']
            email = request.POST.get("email")
            if (database.child("users").child(a).child("details").child("email").get().val() != email):
                raise KeyError
            users = database.child("users").get()

            first = ""
            for userid, items in users.val().items():
                emailResponse = database.child("users").child(userid).child("details").child("email").get()
                emailName = emailResponse.val()
                if (emailName == email):
                    first = database.child("users").child(userid).child("details").child("first_name").get().val()
                    last = database.child("users").child(userid).child("details").child("last_name").get().val()
                    uni = database.child("users").child(userid).child("details").child("university").get().val()
                    #events = database.child("users").child(userid).child("details").child("university").get().val()

            if (first != ""):
                return render(request, "find_info.html", {"message" : "Information - " + first + " " + last + ": " + uni})
            else:
                return render(request, "find_info.html", {"message" : "Not found"})

        except KeyError as e:
            print("Testing" + e)
            return render(request, "login.html", {"message" : "Please Log In!"})
            
    else:
        return render(request, "find_info.html",)






