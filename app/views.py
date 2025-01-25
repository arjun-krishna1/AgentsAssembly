from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Bill, AgentPreferences, Vote
import json
from django.db import models, transaction
from datetime import datetime

# Create your views here.

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
        preferences, created = AgentPreferences.objects.get_or_create(user=request.user)
        preferences.environmental_weight = request.POST.get('environmental', 50)
        preferences.economic_weight = request.POST.get('economic', 50)
        preferences.social_weight = request.POST.get('social', 50)
        preferences.token_strategy = request.POST.get('strategy', 'MODERATE')
        preferences.save()
        return redirect('dashboard')

    preferences = AgentPreferences.objects.filter(user=request.user).first()
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
                bill.full_clean()
                bill.save()

                # Handle document uploads
                if request.FILES.getlist('documents'):
                    for document in request.FILES.getlist('documents'):
                        BillDocument.objects.create(
                            bill=bill,
                            document=document
                        )

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

# API endpoints
@require_http_methods(["GET"])
def get_bills(request):
    """API endpoint to fetch bills with filtering options"""
    sort_by = request.GET.get('sort', 'deadline')
    bills = Bill.objects.all()
    
    if sort_by == 'deadline':
        bills = bills.order_by('deadline')
    elif sort_by == 'funding':
        bills = bills.order_by('-current_funding')

    bills_data = []
    for bill in bills:
        time_remaining = bill.deadline - timezone.now()
        bills_data.append({
            'id': bill.id,
            'title': bill.title,
            'description': bill.description,
            'deadline': bill.deadline.isoformat(),
            'funding_progress': bill.funding_progress,
            'time_remaining': str(time_remaining).split('.')[0],
            'status': bill.status
        })
    
    return JsonResponse({'bills': bills_data})

@require_http_methods(["POST"])
def vote_on_bill(request, bill_id):
    """API endpoint to submit a vote on a bill"""
    try:
        data = json.loads(request.body)
        bill = get_object_or_404(Bill, id=bill_id)
        
        vote, created = Vote.objects.get_or_create(
            user=request.user,
            bill=bill,
            defaults={'tokens_committed': data['tokens']}
        )
        
        if not created:
            vote.tokens_committed = data['tokens']
            vote.save()
        
        # Update bill funding
        bill.current_funding = Vote.objects.filter(bill=bill).aggregate(
            total=models.Sum('tokens_committed'))['total'] or 0
        bill.save()
        
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
