from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect

def index(request):
    user_id = request.user.id
    is_auth = request.user.is_authenticated()
    if(is_auth):
        if request.session.get('has_login',True):
            tipouser = User.objects.get(id=user_id)
            return render_to_response('principal/index.html', {'nombreuser':tipouser.username})
        else:
            return HttpResponseRedirect('/obispado/login/')
    else:
        return HttpResponseRedirect('/obispado/login/')
