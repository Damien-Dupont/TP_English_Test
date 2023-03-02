from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from .forms import SignUpForm, ConjugaisonForm
from .models import Player, IrregularVerb

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
    return render(request, 'english_verbs/signUp.html', {'form': form})

def log_in(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('game')
        else:
            return render(request, 'english_verbs/logIn.html', {'error': 'Invalid username or password.'})
    else:
        return render(request, 'english_verbs/logIn.html')

@login_required
def log_out(request):
    logout(request)
    return redirect('index')

@login_required
def game(request):
    return render(request, 'english_verbs/game.html')

def play(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    irregular_verb = IrregularVerb.objects.order_by('?').first()

    if Player.objects.filter(email=request.user, irregular_verb=irregular_verb).exists():
      messages.warning(request, "Vous avez déjà conjugué ce verbe.")

    form = ConjugaisonForm()

    return render(request, 'english_verbs/play.html', {'irregular_verb': irregular_verb, 'form': form})

def end(request, result):
    if not request.user.is_authenticated:
        return redirect('login')

    player = Player.objects.get(user=request.user, irregular_verb=result['irregular_verb'])
    player.results = result['results']
    player.date_played = timezone.now()
    player.save()

    return render(request, 'english_verbs/end.html', {'result': result})