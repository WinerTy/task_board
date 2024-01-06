from allauth.account.views import SignupView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect


class AboutUs:
    def show(request):
        return render(request, 'users/about_us.html')


class UsersInfo:
    def profile(request):
        if request.user.is_authenticated:
            return render(request, 'users/profile.html')
        return redirect('account_login')

class CustomView(SignupView):
    template_name = 'account/signup.html'

class RoleTools:
    def role(request):
        if request.user.is_authenticated:
            group = Group.objects.get(name='Subscriber')
            if group.id in [g.id for g in request.user.groups.all()]:
                request.user.groups.remove(group)
            else:
                request.user.groups.add(group)
            return redirect('/main')
        else:
            return redirect('account_login')