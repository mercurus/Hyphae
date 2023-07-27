from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user
from django.http import JsonResponse


# @login_required
# def profile(request):
#     queryset = Topic.objects.filter(morph_id=2).select_related('morph')
#     folk = get_object_or_404(queryset, user=request.user)
#     context = {'folk': folk}
#     return render(request, 'conduct/profile.html', context)


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
    return redirect('gnosis:spa_entrance')


def spa_entrance(request):
    return render(request, 'hyphae_spa.html')


def catchall(request, url):
    if request.method == 'GET':
        return redirect('gnosis:spa_entrance')
    return JsonResponse({'message':'no'}, status=404)

