from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
# Create your views here
from .forms import MovieForm
from .forms import SignUpForm
import requests

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request,user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required(login_url = 'login')
def main(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie_name = form.cleaned_data['movie_name']
            response = requests.get('https://www.omdbapi.com/?t=%s&apikey=767da9db' % movie_name)
            data = response.json()
            print(data)
            return render(request, template_name = 'display.html', context = {
                'movie_name':data['Title'],
                'poster':data['Poster'],
                'plot': data['Plot'],
                'imdbrating': data['imdbRating'],
            })
    else:
        form = MovieForm()
        return render(request,template_name = 'main.html', context = {'form': form})