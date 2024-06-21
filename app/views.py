from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import datetime

from app.forms import RegisterForm, LoginForm, PredictForm, FinalistPredictForm, ChampionsForm
from .models import User, Team, Match, Prediction, FinalistPrediction, ChampionPrediction


def home(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    return render(request, 'app/home.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect(to='/dashboard/')
    if request.method == 'GET':
        return render(request, 'app/login.html', context={'form': LoginForm()})
    elif request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect(to='/dashboard/')
        else:
            return redirect(to='/login/')


def register_view(request):
    if request.user.is_authenticated:
        return redirect(to='/dashboard/')
    if request.method == 'GET':
        return render(request, 'app/register.html', context={'form': RegisterForm()})
    elif request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            account = form.save()
            login(request, account)
            return redirect(to='/login/')
        else:
            return redirect(to='/register/')


def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect(to='/')
    today_matches = Match.objects.filter(date__gte=datetime.date.today())
    today_matches_predictions = Prediction.objects.filter(
        match__in=Match.objects.filter(date__gte=datetime.date.today()), user=request.user)
    dic = {}
    for match in today_matches:
        for prediction in today_matches_predictions:
            if prediction.match == match:
                dic[match] = prediction
                break
        if dic.get(match) is None:
            dic[match] = None
    user = User.objects.get(username=request.user)
    return render(request, 'app/dashboard.html',
                  context={'user': user, 'matches': dic, 'time': datetime.datetime.now()})


def predictions_view(request):
    if datetime.datetime.now().hour < 14:
        return redirect('/dashboard/')
    matches = Match.objects.all().order_by('date')
    predictions = Prediction.objects.filter(match__in=matches)
    dic = {}
    for match in matches:
        list_prediction = []
        for prediction in predictions:
            if prediction.match == match:
                list_prediction.append(prediction)
        dic[match] = list_prediction
    return render(request, 'app/predictions.html', {'matches': dic, 'time': datetime.datetime.now()})


def finals_prediction_view(request):
    if request.method == 'GET':
        finals_form = FinalistPredictForm()
        if FinalistPrediction.objects.filter(pk=1).exists():
            finals_form.fields['team_1'].initial = FinalistPrediction.objects.get(pk=1).team
        if FinalistPrediction.objects.filter(pk=2).exists():
            finals_form.fields['team_2'].initial = FinalistPrediction.objects.get(pk=2).team
        champion_form = ChampionsForm()
        if ChampionPrediction.objects.filter(pk=1).exists():
            champion_form.fields['team'].initial = ChampionPrediction.objects.get(pk=1).team
        return render(request, 'app/FinalPrediction.html',
                      context={'time': datetime.datetime.now(), 'finals_form': finals_form,
                               'champion_form': champion_form})

    elif request.method == 'POST':
        form1 = FinalistPredictForm(request.POST)
        form2 = ChampionsForm(request.POST)
        if form1.is_valid():
            user = User.objects.get(username=request.user)
            if FinalistPrediction.objects.filter(user=user, pk=1).exists():
                FinalistPrediction.objects.filter(user=user, pk=1).update(
                    team=form1.cleaned_data['team_1'])
            else:
                prediction = FinalistPrediction.objects.create(
                    team=form1.cleaned_data['team_1'], user=user, pk=1)
                prediction.save()
            if FinalistPrediction.objects.filter(user=user, pk=2).exists():
                FinalistPrediction.objects.filter(user=user, pk=2).update(
                    team=form1.cleaned_data['team_2'])
            else:
                prediction = FinalistPrediction.objects.create(
                    team=form1.cleaned_data['team_2'], user=user, pk=2)
                prediction.save()
            return redirect('/dashboard/')

        elif form2.is_valid():
            user = User.objects.get(username=request.user)
            if ChampionPrediction.objects.filter(user=user).exists():
                ChampionPrediction.objects.filter(user=user).update(team=form2.cleaned_data['team'])
            else:
                prediction = ChampionPrediction.objects.create(team=form2.cleaned_data['team'], user=user)
                prediction.save()
            return redirect('/dashboard/')
    else:
        return redirect(to='/finalsprediction/')


def leaderboard(request):
    if not request.user.is_authenticated:
        return redirect(to='/')
    users = User.objects.filter(is_staff=False).order_by('-score')
    return render(request, 'app/leaderboard.html', context={'time': datetime.datetime.now(), 'users': users})


def logout_view(request):
    if request.method == 'GET':
        logout(request)
        return redirect(to='/login/')


def predict_view(request, match_id, team_1_name, team_2_name):
    if not request.user.is_authenticated:
        return redirect(to='/')
    if datetime.datetime.now().hour >= 14:
        return redirect('/dashboard/')
    if request.method == 'GET':
        return render(request, "app/predict.html",
                      context={'match_id': match_id, 'team_1_name': team_1_name, 'team_2_name': team_2_name,
                               'form': PredictForm()})
    elif request.method == 'POST':
        form = PredictForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=request.user)
            if Prediction.objects.filter(match=match_id, user=user).exists():
                Prediction.objects.filter(match=match_id, user=user).update(
                    team_1_score=form.cleaned_data['team_1_score'], team_2_score=form.cleaned_data['team_2_score'])
                return redirect('/dashboard/')
            else:
                prediction = Prediction.objects.create(match=Match.objects.get(pk=match_id),
                                                       team_1_score=form.cleaned_data['team_1_score'],
                                                       team_2_score=form.cleaned_data['team_2_score'], user_id=user.id)
                prediction.save()
                return redirect(to='/dashboard/')
        else:
            return redirect(to='/predict/' + str(match_id) + '/' + team_1_name + '/' + team_2_name + '/')
