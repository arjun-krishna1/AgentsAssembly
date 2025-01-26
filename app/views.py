from django.shortcuts import render, redirect
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Project, AgentPreferences, Vote
from django.db import transaction
from datetime import datetime
import openai
from django.conf import settings
import os
openai.api_key = os.environ.get('OPENAI_API_KEY')


def index(request):
    return render(request, 'app/index.html')

#@login_required
def dashboard(request):
    """Main dashboard view showing projects list and voting status"""
    projects = Project.objects.all().order_by('-created_at')
    context = {
        'projects': projects
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
def create_project(request):
    """View for creating new projects"""
    if request.method == 'POST':
        try:
            with transaction.atomic():

                import subprocess
                command = f"""npx tsx ./src/ts/create_project.ts --name {request.POST['title']}"""
                result = subprocess.run(command, shell=True, capture_output=True, text=True)

                # Access the stdout
                if result.returncode == 0:  # Check if the command was successful
                    project_id = result.stdout.strip()  # Remove any extra whitespace
                    print("Project ID:", project_id)
                else:
                    print("Error:", result.stderr)  # Print any errors

                # Create the project
                project = Project(
                    title=request.POST['title'],
                    description=request.POST['description'],
                    funding_goal=request.POST['funding_goal'],
                    environmental_impact=request.POST['environmental_impact'],
                    economic_impact=request.POST['economic_impact'],
                    social_impact=request.POST['social_impact'],
                    story_id=project_id
                )
                
                # Validate and save the project
                project.save()



                # Get all agent preferences
                agents = AgentPreferences.objects.all()
                
                # Process votes for each agent
                for agent in agents:
                    # Prepare the prompt for OpenAI
                    prompt = f"""
                    As an AI voting agent with the following preferences:
                    - Environmental weight: {agent.environmental_weight}%
                    - Economic weight: {agent.economic_weight}%
                    - Social weight: {agent.social_weight}%
                    - Strategy: {agent.token_strategy}

                    Evaluate this project proposal:
                    Title: {project.title}
                    Description: {project.description}
                    Funding Goal: {project.funding_goal}
                    Environmental Impact: {project.environmental_impact}
                    Economic Impact: {project.economic_impact}
                    Social Impact: {project.social_impact}

                    Do you support this project? If yes, what number of tokens should you commit?
                    You have a total budget of 100 tokens.
                    Your commitment should be below this and also below the project's funding goal.
                    Respond only with one number, the number of tokens you commit without any other text or context.
                    """

                    # Call OpenAI API - Updated to use environment variable
                    client = openai.OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a voting agent making funding decisions."},
                            {"role": "user", "content": prompt}
                        ]
                    )

                    print("ARJUN LOG")
                    print(response)
                    print("ARJUN LOG")
                    print(response.choices[0].message.content)

                    contribution = 0
                    # Parse response - Updated to ma
                    contribution = int(response.choices[0].message.content.strip())

                    if contribution:
                        # Create vote record
                        Vote.objects.create(
                            project=project,
                            tokens_committed=contribution,
                            agent=agent
                        )
                        
                        # Update project's current funding
                        project.current_funding += contribution
                        project.save()

                return redirect('dashboard')

        except ValidationError as e:
            return render(request, 'app/create_project.html', {
                'error_message': '; '.join(e.messages)
            })
        except Exception as e:
            return render(request, 'app/create_project.html', {
                'error_message': str(e)
            })

    return render(request, 'app/create_project.html')
