from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RunForm
from .models import Run


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        messages.success(self.request, 'You have logged in successfully.')
        return super().form_valid(form)


class CustomLogoutView(LogoutView):

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'You have logged out successfully.')
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

    return render(request, 'registration/register.html', {'form': form})


@login_required
def home(request):
    if request.method == 'POST':
        form = RunForm(request.POST)
        if form.is_valid():
            run = form.save(commit=False)
            run.user = request.user
            
            # Try to save safely; if model validation fails, show error on form instead of crashing
            try:
                run.full_clean()
                run.save()
                messages.success(request, 'Run added successfully.')
                return redirect('home')
            except ValidationError as e:
                form.add_error(None, e)
    else:
        form = RunForm()

    runs = Run.objects.filter(user=request.user).order_by('-date')

    total_runs = runs.count()
    total_distance = Decimal('0.00')

    # Convert miles to km for simple overall stats
    for run in runs:
        if run.distance_unit == 'mi':
            total_distance += run.distance * Decimal('1.60934')
        else:
            total_distance += run.distance

    # Round to 2 decimal places so you don't get ugly long numbers
    total_distance = round(total_distance, 2)

    if total_runs:
        average_distance = round(total_distance / total_runs, 2)
    else:
        average_distance = Decimal('0.00')

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
    run = get_object_or_404(Run, id=run_id, user=request.user)

    if request.method == 'POST':
        form = RunForm(request.POST, instance=run)
        if form.is_valid():
            run = form.save(commit=False)
            try:
                run.full_clean()
                run.save()
                messages.success(request, 'Run updated successfully.')
                return redirect('home')
            except ValidationError as e:
                form.add_error(None, e)
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
    run = get_object_or_404(Run, id=run_id, user=request.user)

    if request.method == 'POST':
        run.delete()
        messages.success(request, 'Run deleted successfully.')
        return redirect('home')

    return render(request, 'delete_run.html', {'run': run})