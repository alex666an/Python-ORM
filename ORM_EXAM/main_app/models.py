from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator, MinLengthValidator, RegexValidator
from main_app.managers import AstronautManager


class BaseModel(models.Model):
    name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(2)]
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Astronaut(BaseModel):
    phone_number = models.CharField(max_length=15, unique=True, validators=[RegexValidator(regex=r'^\d{1,15}$')])
    is_active = models.BooleanField(default=True)
    date_of_birth = models.DateField(null=True, blank=True)
    spacewalks = models.IntegerField(default=0, validators=[MaxValueValidator(0)])

    objects = AstronautManager()

dog = models.Arr


class Spacecraft(BaseModel):
    manufacturer = models.CharField(max_length=100)
    capacity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    weight = models.FloatField(validators=[MaxValueValidator(0.0)])
    launch_date = models.DateField()


class Mission(BaseModel):
    STATUS_CHOICES = [
        ('Planned', 'Planned'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed')
    ]

    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='Planned')
    launch_date = models.DateField()
    spacecraft = models.ForeignKey(Spacecraft, on_delete=models.CASCADE)
    astronauts = models.ManyToManyField(Astronaut, related_name='missions')
    commander = models.ForeignKey(Astronaut, on_delete=models.SET_NULL, null=True, blank=True, related_name='commander_missions')





