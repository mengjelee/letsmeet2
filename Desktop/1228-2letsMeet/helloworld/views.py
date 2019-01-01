from django.shortcuts import render,redirect   # 加入 redirect 套件
from django.contrib.auth import authenticate
from django.contrib import auth
from django.http import HttpResponse
from django.contrib.auth.models import User
from event.models import Event, Response

def index(request):
	return render(request, 'welnew.html',locals())
"""
def home(request):
	user = User.objects.get(username=username)
	event = Event.objects.filter(owner=user.username)
	eventName = event.eventName
	return  render(request, 'home.html',locals())

	
def login(request):
    # if request.user.is_authenticated: 
    #     #print("t1")
    #     return render(request, 'index.html',locals())
    if request.method == 'POST':
        if 'name' in request.POST:
            #print("t2")
            username = request.POST['name']
            if 'pass' in request.POST:
                password = request.POST['pass']
                user = auth.authenticate(username=username, password=password)
                auth.login(request,user)
                #print("8")
                if user is not None:
                    if user.is_active:
                        auth.login(request,user)
                        print("成功登入")
                    else:
                       return HttpResponse('尚未登入')
                else:
                   return HttpResponse('登入失敗!')
    return redirect('/home/')
 """
def login(request):
    # if request.user.is_authenticated: 
    #     #print("t1")
    #     return render(request, 'index.html',locals())
    if request.method == 'POST':
        if 'name' in request.POST:
            #print("t2")
            username = request.POST['name']
            if 'pass' in request.POST:
                password = request.POST['pass']
                user = auth.authenticate(username=username, password=password)
                auth.login(request,user)
                #print("8")
                if user is not None:
                    if user.is_active:
                        auth.login(request,user)
                        print("成功登入")
                        events = Event.objects.filter(owner=user.username)
                        eventName = []
                        for i in range(len(events)):
                        	name = events[i].eventName
                        	eventName.append(name)

                    else:
                       return HttpResponse('尚未登入')
                else:
                   return HttpResponse('登入失敗!')
    return render(request, 'home.html', locals())

def logout(request):
    auth.logout(request)
    #return redirect('/')
    return render(request, 'welnew.html',locals())

def signup(request):
    if request.method == 'POST':
        print("註冊有post")
        if 'regname' in request.POST:
            username = request.POST['regname']
            if 'regpass' in request.POST:
                password = request.POST['regpass']
                # if 'email' in request.POST:
                #     email = request.POST['email']
                email = ""
                    #form = UserCreationForm(request.POST)
                print("0")
                try:
                    user = User.objects.get(username=username)
                except:
                    user = None
                    print("user is None")
                """
                if user is None:
                    user = User.objects.create_user(username,email, password)
                    user.save()
                    messages.add_message(request, messages.INFO, '註冊成功')
                    print('註冊成功')
                else:
                    messages.add_message(request, messages.INFO, '此使用者已經有人使用')
                    print("此使用者已經有人使用") 
                """               
        return redirect('/')


def createEvent(request):
	#error = False
	if request.GET:
		eventName = request.GET.get('eventName')
		owner = request.GET.get('owner')
		dayChosen = request.GET.get('dayChosen')
		timeChosen = request.GET.get('timeChosen')
		randUrl = '/' + request.GET.get('randUrl') + '/'
		#if not eventName or not dayChosen:
		#	error = True
		#if not error:
		Event.objects.create(eventName=eventName, owner=owner, dayChosen=dayChosen, timeChosen=timeChosen, randUrl=randUrl)
		return redirect(randUrl)
	return render(request, 'week.html')



def newEvent(request):
	current = request.get_full_path()
	event = Event.objects.get(randUrl=current)
	eventName = event.eventName
	dC = event.dayChosen
	dayChosen = dC.split(",",dC.count(","))
	tC = event.timeChosen
	timeChosen = tC.split(",",tC.count(","))
	if request.method == 'POST':
		yourName = request.POST.get('yourName')
		freeDay = request.POST.get('freeDay')
		Response.objects.create(yourName=yourName, freeDay=freeDay, event=event)
		return redirect(current+'result')
	return render(request, 'user.html',locals())


def resultpage(request):
	copy = request.build_absolute_uri()[0:-6]
	current = request.get_full_path()
	current = current[0:-6]
	event = Event.objects.get(randUrl=current)
	eventName = event.eventName
	dC = event.dayChosen
	dayChosen = dC.split(",",dC.count(","))
	tC = event.timeChosen
	timeChosen = tC.split(",",tC.count(","))
	results = Response.objects.filter(event=event)
	fD = []
	for i in range(len(results)):
		yourName = results[i].yourName
		freeDay = results[i].freeDay
		f = freeDay.split(",",freeDay.count(","))
		fD.append({yourName:f})
		#fD.extend(f)

	# 計算星期幾出現幾次：
	days = []
	for d in fD:
		a = list(d.values())
		days.extend(a[0])
	
	counting = []
	for i in dC:
		counting.append(days.count(i))
	
	maxNum = max(counting)
	scaleRange = range(maxNum)
	reply = len(results)






	#顯示每一天有多少人選：


	#show = tuple()
	#for d in fD:
	#	show.insert(d,fD.count(d))
	#	show[d] = show.get(d,0) + 1

	#show = dict()
	#for d in fD:
	#	show[d] = show.get(d,0) + 1

	#--------  我是笨蛋啦繞一圈回來做一樣的事ＱＱ --------#
	# results = Response.objects.filter(event=event) #
	# freeDay = []                                   #
	# for i in range(len(results)):                  #
	# 	free = results[i].freeDay                    #
	# 	f = free.split(",",dayChosen.count(","))     #
	# 	freeDay.extend(f)                            #
	# freeDay.sort()                                 #
	# setFreeDay = list(set(freeDay))                #
	# setFreeDay.sort(key=freeDay.index)             #
	#----------------- 笨蛋紀念區ＱＱ -----------------#

	#return HttpResponse(reply)
	return render(request, 'result.html',locals())

