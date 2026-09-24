from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect

from .forms import RunForm
from .models import Run


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        messages.success(
            self.request,
            'You have logged in successfully.'
        )
        return super().form_valid(form)


class CustomLogoutView(LogoutView):

    def dispatch(self, request, *args, **kwargs):
        messages.success(
            request,
            'You have logged out successfully.'
        )
        return super().dispatch(request, *args, **kwargs)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(
        request,
        'registration/register.html',
        {'form': form}
    )


@login_required
def home(request):
    if request.method == 'POST':
        form = RunForm(request.POST)

        if form.is_valid():
            run = form.save(commit=False)
            run.user = request.user
            run.full_clean()
            run.save()

            messages.success(
                request,
                'Run added successfully.'
            )
            return redirect('home')
    else:
        form = RunForm()

    runs = Run.objects.filter(
        user=request.user
    ).order_by('-date')

    total_runs = runs.count()
    total_distance = sum(run.distance for run in runs)

    if total_runs:
        average_distance = total_distance / total_runs
    else:
        average_distance = 0

    return render(
        request,
        'home.html',
        {
            'form': form,
            'runs': runs,
            'total_runs': total_runs,
            'total_distance': total_distance,
            'average_distance': average_distance,
        }
    )


@login_required
def edit_run(request, run_id):
    run = Run.objects.get(
        id=run_id,
        user=request.user
    )

    if request.method == 'POST':
        form = RunForm(
            request.POST,
            instance=run
        )

        if form.is_valid():
            run = form.save(commit=False)
            run.full_clean()
            run.save()

            messages.success(
                request,
                'Run updated successfully.'
            )
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


@login_required
def delete_run(request, run_id):
    run = Run.objects.get(
        id=run_id,
        user=request.user
    )

    if request.method == 'POST':
        run.delete()

        messages.success(
            request,
            'Run deleted successfully.'
        )
        return redirect('home')

    return render(
        request,
        'delete_run.html',
        {
            'run': run,
        }
    )