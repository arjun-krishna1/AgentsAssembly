from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Project(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PASSED', 'Passed'),
        ('FAILED', 'Failed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    funding_goal = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    current_funding = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    
    # Impact statements
    environmental_impact = models.TextField(blank=True)
    economic_impact = models.TextField(blank=True)
    social_impact = models.TextField(blank=True)

    def __str__(self):
        return self.title

    @property
    def funding_progress(self):
        if self.funding_goal == 0:
            return 0
        return (self.current_funding / self.funding_goal) * 100

class AgentPreferences(models.Model):
    STRATEGY_CHOICES = [
        ('CONSERVATIVE', 'Conservative'),
        ('MODERATE', 'Moderate'),
        ('AGGRESSIVE', 'Aggressive'),
    ]

    environmental_weight = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=50
    )
    economic_weight = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=50
    )
    social_weight = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=50
    )
    token_strategy = models.CharField(
        max_length=20,
        choices=STRATEGY_CHOICES,
        default='MODERATE'
    )

    def __str__(self):
        return f"heres preferences"

class Vote(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    tokens_committed = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    agent = models.ForeignKey(AgentPreferences, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"vote on {self.project.title}"
