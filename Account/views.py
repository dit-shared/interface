from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import HashPassword, User, Feedback, ExtendedUser
from Frontend import settings
from Frontend.TelegramBot import send as telegram_send
from Slicer.models import ImageSeries
import os, json, time, subprocess, datetime

def runCommand(commands):
    subprocess.run(commands)

def runShell(path, sh_input = ''):
    shellscript = subprocess.Popen([settings.BASE_DIR + '/' + path], stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = shellscript.communicate(sh_input)
    returncode = shellscript.returncode
    return returncode, stdout, stderr

def buildJSONResponse(responseData):
	return HttpResponse(json.dumps(responseData), content_type="application/json")

def getResearchView(request):
    if 'id' not in request.GET:
        return buildJSONResponse({"ok": False, "error": "Invalid request"})
    if not ImageSeries.objects.filter(id=request.GET['id']):
        return buildJSONResponse({"ok": False, "error": "This research doesn`t exists"})
    series = ImageSeries.objects.get(id=request.GET['id'])
    return buildJSONResponse({"ok": True, "dirname": series.media_path})

def account(request):
    if 'id' not in request.session:
        return HttpResponseRedirect('/')
    id = request.session['id']
    user = User.objects.get(id=id)
    extUser = ExtendedUser.objects.get(userID=id)
    return render(request, "Account/index.html", {"user": user, "extUser": extUser})

def view(request):
    if 'id' not in request.session:
        return HttpResponseRedirect('/')
    id = request.session['id']
    user = User.objects.filter(id=id)[0]
    extUser = ExtendedUser.objects.get(userID=id)

    data = list()

    series = ImageSeries.objects.all()
    for i, s in enumerate(series):
        data.append({"id": i + 1, "series": s, "voxels": s.voxels})

    return render(request, "Account/view.html", {"user": user, "data": data, "extUser": extUser})

def upload(request):
    if 'id' not in request.session:
        return HttpResponseRedirect('/')
    id = request.session['id']
    user = User.objects.filter(id=id)[0]
    extUser = ExtendedUser.objects.get(userID=id)

    return render(request, "Account/upload.html", {"user": user, "extUser": extUser})

def predict_view(request):
    if 'id' not in request.session:
        return HttpResponseRedirect('/')
    id = request.session['id']
    user = User.objects.filter(id=id)[0]
    extUser = ExtendedUser.objects.get(userID=id)

    return render(request, "Account/predict.html", {"user": user, "extUser": extUser})

def predict(request):
    runCommand(["docker", "exec", "-i", "-t", "root_jupyter_1_826396f9a729", "/bin/bash", "/radio/temp/for_npcmr/run.sh"])
    #runCommand(["/radio/temp/for_npcmr/run.sh"])
    return buildJSONResponse({"message": "", "success": True})

def encPasswd(request):
    if 'passwd' not in request.GET:
        return HttpResponse("Incorrect GET request")
    return HttpResponse(HashPassword(request.GET['passwd']))

def feedback(request):
    if 'id' not in request.session:
        return buildJSONResponse({"message": 'Error: you are not authorized', "success": True})
    if 'title' not in request.POST or 'text' not in request.POST:
        return buildJSONResponse({"message": 'Error: invalid request data', "success": True})
    
    feedback = Feedback.objects.create(user_id=request.session['id'], title=request.POST['title'],
                text=request.POST['text'], time=datetime.datetime.now())
    feedback.save()

    if settings.TELEGRAM_FEEDBACK:
        user = User.objects.filter(id=request.session['id'])[0]
        telegram_msg = 'Title: ' + feedback.title + '\nText: ' + feedback.text +\
            '\nMail: ' + user.mail  + '\nFrom: ' + str(user)
        telegram_send(settings.FeedbackTelegramChannelToken, settings.FeedbackTelegramChatId, telegram_msg)

    return buildJSONResponse({"message": "", "success": True})

def changeAccount(request):
    if "id" not in request.session:
        return HttpResponseRedirect("/")
    print(request.POST)
    return HttpResponse("OK")

def uploadAva(request):
    if "id" not in request.session:
        return HttpResponseRedirect("/")
    if "file" not in request.FILES:
        return buildJSONResponse({"ok": False, "message": "Неправильный запрос"})
    
    id = request.session['id']
    extUser = ExtendedUser.objects.get(userID=id)

    extUser.ava = request.FILES["file"]
    extUser.save()

    return buildJSONResponse({"ok": True})

def statistics(request):
    if "id" not in request.session:
        return HttpResponseRedirect("/")
    return render(request, "Account/statistics.html")
