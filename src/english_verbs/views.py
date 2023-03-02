from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from .forms import SignUpForm, ConjugaisonForm
from .models import Player, IrregularVerb
import threading

# Create your views here.
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.joined_date = timezone.now()
            player.save()
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'english_verbs/inscription.html', {'form': form})

def log_in(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('game')
        else:
            return render(request, 'english_verbs/inscription.html', {'error': 'Invalid username or password.'})
    else:
        return render(request, 'english_verbs/inscription.html')

@login_required
def log_out(request):
    logout(request)
    return redirect('index')

@login_required
def game(request):
    return render(request, 'english_verbs/jeu.html')

def play(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')

    # Get a random verb
    irregular_verb = IrregularVerb.objects.order_by('?').first()

    # Timer
    def end_timer():
        return redirect('end', result={'irregular_verb': irregular_verb})

    time_limit = 60
    timer = threading.Timer(time_limit, end_timer)
    timer.start()

    # Check if user has already played this verb
    if Player.objects.filter(user=request.user, irregular_verb=irregular_verb).exists():
      messages.warning(request, "Vous avez déjà conjugué ce verbe.")

    # form init
    form = ConjugaisonForm()

    # Check if form is valid
    return render(request, 'english_verbs/jeu.html', {'irregular_verb': irregular_verb, 'form': form})

@receiver(user_logged_out)
def cancel_timer(sender, request, **kwargs):
    # Cancel timer
    if 'timer' in request.session:
       request.session['timer'].cancel()
       del request.session['timer']

def end(request, result):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')

    # Save result
    player = Player.objects.get(user=request.user, irregular_verb=result['irregular_verb'])
    player.results = result['results']
    player.date_played = timezone.now()
    player.save()

    # Display result
    return render(request, 'english_verbs/fin.html', {'result': result})