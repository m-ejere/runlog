from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from .forms import RunForm
from .models import Run


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def home(request):
    if request.method == 'POST':
        form = RunForm(request.POST)

        if form.is_valid():
            run = form.save(commit=False)
            run.user = request.user
            run.save()
            return redirect('home')
    else:
        form = RunForm()

    runs = Run.objects.filter(user=request.user).order_by('-date')

    return render(
        request,
        'home.html',
        {
            'form': form,
            'runs': runs,
        }
    )


@login_required
def edit_run(request, run_id):
    run = Run.objects.get(id=run_id, user=request.user)

    if request.method == 'POST':
        form = RunForm(request.POST, instance=run)

        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RunForm(instance=run)

    return render(
        request,
        'edit_run.html',
        {
            'form': form,
            'run': run,
        }
    )