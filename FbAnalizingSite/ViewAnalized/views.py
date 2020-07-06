from django.shortcuts import render, redirect, HttpResponse
from django.utils import http
from django.views.decorators.csrf import csrf_protect

from .core import crawler, friends, nlp
import jwt
import json
import base64
import zlib
driver = crawler.make_driver()
user_dict = []
@csrf_protect
def index(request):
    f_id = request.GET.get('id', None)
    if f_id:
        posts = friends.Friend(f_id, "asdf").GET_post(driver)    
        
        return render(request, 'home/posts.html', {'posts': posts })
    return render(request, 'home/index.html', {})

def login(request):
    if request.method == "POST":
        driver.get('https://www.facebook.com')
        print(request.POST)
        friends = crawler.GET_friends(request.POST['id'], request.POST['pw'], driver)
        if friends != []:
            response = HttpResponse('돈까스 모임')
            json_str = str(json.dumps(friends))            
            b = base64.b64encode(json_str.encode('utf-8'))
            c=zlib.compress(b)
            user_dict.append(c)
            return response
        else : 
            return HttpResponse(401)
        
def loginPage(request):
    fr_json = base64.b64decode(zlib.decompress(user_dict[0]))
    return render(request, 'home/friends.html', {'fr_json' : json.loads(fr_json.decode("utf-8").replace("'", "\""))})

# Create your views here.