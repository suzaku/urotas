#-*-coding=utf-8-*-
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.cache import never_cache
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

from django.contrib.sites.models import RequestSite, Site
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from forms import AuthenticationRememberMeForm

# 将logout函数引入到views模块中, 方便urls设置时统一设定python路径前缀
from django.contrib.auth.views import logout 

def register(request):
    if not request.user.is_authenticated():
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/note')
        else:
            form = UserCreationForm()
        # TODO 实现people/register.html
        return render_to_response('people/register.html',
                                  {'form':form},
                                  context_instance=RequestContext(request))
    else:
        # TODO 提醒已经登录的用户(建议: 使用messages框架http://docs.djangoproject.com/en/dev/ref/contrib/messages/#ref-contrib-messages)
        return HttpResponse('')

def login(request, template_name='people/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME):
    """基于django.contrib.auth.views.login加入`记住登录`的选择
    """
    redirect_to = request.REQUEST.get(redirect_field_name, '')
    if request.method == "POST":
        form = AuthenticationRememberMeForm(data=request.POST)
        if form.is_valid():
            # Light security check -- make sure redirect_to isn't garbage.
            if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL
            if not form.cleaned_data['remember_me']:
                request.session.set_expiry(0)
            from django.contrib.auth import login
            login(request, form.get_user())
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            return HttpResponseRedirect(redirect_to)
    else:
        form = AuthenticationRememberMeForm(request)
    request.session.set_test_cookie()
    if Site._meta.installed:
        current_site = Site.objects.get_current()
    else:
        current_site = RequestSite(request)
    return render_to_response(template_name, {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }, context_instance=RequestContext(request))
login = never_cache(login)

@login_required
def profile(request):
    # TODO user profile setting
    return render_to_response('people/profile.html', 
                              context_instance=RequestContext(request))
