from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from .forms import SignUpForm, ConjugaisonForm
from .models import Player, Verb

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


# def play(request):
#     # Check if user is authenticated
#     if not request.user.is_authenticated:
#         return redirect('login')

#     # Get a random verb
#     irregular_verb = IrregularVerb.objects.order_by('?').first()

#     # Check if user has already played this verb
#     if Player.objects.filter(user=request.user, irregular_verb=irregular_verb).exists():
#         messages.warning(request, "Vous avez déjà conjugué ce verbe.")

#     # form init
#     form = ConjugaisonForm()

#     # Check if form is valid
#     return render(request, 'english_verbs/jeu.html', {'irregular_verb': irregular_verb, 'form': form})


@login_required
def play(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')

    # Get a random verb
    irregular_verb = Verb.objects.order_by('?').first()

    # Check if user has already played this verb
    if Player.objects.filter(user=request.user, irregular_verb=irregular_verb).exists():
        messages.warning(request, "Vous avez déjà conjugué ce verbe.")

    # form init
    form = ConjugaisonForm()

    if request.method == 'POST':
        # Validate form data
        form = ConjugaisonForm(request.POST)
        if form.is_valid():
            preterit = form.cleaned_data['preterit']
            participe_passe = form.cleaned_data['participe_passe']
            base_verbale = form.cleaned_data['base_verbale']
            traduction = form.cleaned_data['traduction']
            result = {}
            result['irregular_verb'] = irregular_verb
            result['results'] = {}

            # Check preterit
            if preterit.lower() == irregular_verb.preterit.lower():
                result['results']['preterit'] = True
            else:
                result['results']['preterit'] = False

            # Check participe passe
            if participe_passe.lower() == irregular_verb.participe_passe.lower():
                result['results']['participe_passe'] = True
            else:
                result['results']['participe_passe'] = False

            # Check base verbale
            if base_verbale.lower() == irregular_verb.base_verbale.lower():
                result['results']['base_verbale'] = True
            else:
                result['results']['base_verbale'] = False

            # Check traduction
            if traduction.lower() == irregular_verb.traduction.lower():
                result['results']['traduction'] = True
            else:
                result['results']['traduction'] = False

            # Display result
            return render(request, 'english_verbs/fin.html', {'result': result})

    # Check if form is valid
    return render(request, 'english_verbs/jeu.html', {'irregular_verb': irregular_verb, 'form': form})


def end(request, result):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')

    # Save result
    player = Player.objects.get(
        user=request.user, irregular_verb=result['irregular_verb'])
    player.results = result['results']
    player.date_played = timezone.now()
    player.save()

    # Display result
    return render(request, 'english_verbs/fin.html', {'result': result})
