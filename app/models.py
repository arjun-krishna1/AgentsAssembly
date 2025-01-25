from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Bill(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PASSED', 'Passed'),
        ('FAILED', 'Failed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    funding_goal = models.PositiveIntegerField()
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

    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
        return f"{self.user.username}'s preferences"

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    tokens_committed = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'bill']

    def __str__(self):
        return f"{self.user.username}'s vote on {self.bill.title}"
