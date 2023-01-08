from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user
from gnosis.models import Topic

@login_required
def profile(request):
    queryset = Topic.objects.filter(morph_id=2).select_related('morph')
    folk = get_object_or_404(queryset, user=request.user)
    context = {'folk': folk}
    return render(request, 'conduct/profile.html', context)


def login_user(request):
    if request.user.is_authenticated:
        next_path = request.GET.get('next', '')
        if next_path:
            return redirect(next_path)
        else:
            return redirect('gnosis:topic_search')
            
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('gnosis:topic_search')

    return render(request, 'conduct/login.html')


def logout_user(request):
    logout(request)
    return redirect('foyer:entrance')
