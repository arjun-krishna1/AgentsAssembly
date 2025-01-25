from django.shortcuts import render, redirect
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Bill, AgentPreferences
from django.db import transaction
from datetime import datetime


def index(request):
    return render(request, 'app/index.html')

#@login_required
def dashboard(request):
    """Main dashboard view showing bills list and voting status"""
    bills = Bill.objects.all().order_by('-created_at')
    context = {
        'bills': bills
    }
    return render(request, 'app/dashboard.html', context)

#@login_required
def agent_settings(request):
    """View for managing voting agent preferences"""
    if request.method == 'POST':
        preferences = AgentPreferences(
            environmental_weight = request.POST.get('environmental', 50),
            economic_weight = request.POST.get('economic', 50),
            social_weight = request.POST.get('social', 50),
            token_strategy = request.POST.get('strategy', 'MODERATE')
        )
        preferences.save()
        return redirect('dashboard')

    preferences = AgentPreferences.objects.last()
    return render(request, 'app/agent_settings.html', {'preferences': preferences})

#@login_required
def create_bill(request):
    """View for creating new bills"""
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Convert the datetime-local string to datetime object
                deadline = datetime.strptime(
                    request.POST['deadline'],
                    '%Y-%m-%dT%H:%M'
                ).replace(tzinfo=timezone.get_current_timezone())

                # Create the bill
                bill = Bill(
                    title=request.POST['title'],
                    description=request.POST['description'],
                    deadline=deadline,
                    funding_goal=request.POST['funding_goal'],
                    environmental_impact=request.POST['environmental_impact'],
                    economic_impact=request.POST['economic_impact'],
                    social_impact=request.POST['social_impact']
                )
                
                # Validate the bill
                bill.save()
                return redirect('dashboard')

        except ValidationError as e:
            return render(request, 'app/create_bill.html', {
                'error_message': '; '.join(e.messages)
            })
        except Exception as e:
            return render(request, 'app/create_bill.html', {
                'error_message': str(e)
            })

    return render(request, 'app/create_bill.html')
