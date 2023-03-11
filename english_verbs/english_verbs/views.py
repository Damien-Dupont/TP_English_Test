from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponseRedirect
from . forms import SignUpForm, ConjugaisonForm
from . models import Player, Verb, Town

# Create your views here.
def index(request):
    return render(request, 'english_verbs/index.html')


def verbs(request):
    return render(request, 'english_verbs/verbs.html')


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.joined_date = timezone.now()
            player.save()
            return redirect('english_verbs/play.html')
        else:
            towns = Town.objects.all()
            form = SignUpForm()
        return render(request, 'english_verbs/index.html', {'form': form, 'towns': towns})


def log_in(request):
    if request.method == 'POST':
        user = Player()
        user.email = request.POST.get['email']
        user.password = request.POST.get['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'english_verbs/play.html')
        else:
            return render(request, 'english_verbs/inscription.html', {'error': 'Invalid username or password.'})
    user.save()
    return HttpResponseRedirect("/")

@login_required
def log_out(request):
    logout(request)
    return render(request, 'english_verbs/play.html')

@login_required
def game(request):
    return render(request, 'english_verbs/play.html')


def play(request):
    # Check if user is authenticated
    # if not request.user.is_authenticated:
        # return redirect('login')

    # Get a random verb
    base_verbale = Verb.objects.order_by('?').first()

    # Check if user has already played this verb
    if Player.objects.filter(user=request.user, base_verbale=base_verbale).exists():
        messages.warning(request, "Vous avez déjà conjugué ce verbe.")

    # form init
    form = ConjugaisonForm()

    # Check if form is valid
    return render(request, 'english_verbs/play.html', {'irregular_verb': base_verbale, 'form': form})


def end(request, result):
    # Check if user is authenticated
    # if not request.user.is_authenticated:
        # return redirect('login')

    # Save result
    player = Player.objects.get(
        user=request.user, irregular_verb=result['irregular_verb'])
    player.results = result['results']
    player.date_played = timezone.now()
    player.save()

    # Display result
    return render(request, 'english_verbs/fin.html', {'result': result})
