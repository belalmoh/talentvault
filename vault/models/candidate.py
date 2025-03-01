from django.db import models

DEPARTMENT_CHOICES = [
    (1, 'Engineering'),
    (2, 'Sales'),
    (3, 'Marketing'),
    (4, 'Human Resources'),
    (5, 'Finance'),
    (6, 'Operations'),
]

class Candidate(models.Model):
    full_name = models.CharField(max_length=255, blank=False)
    email = models.EmailField(max_length=255, blank=False, unique=True)
    date_of_birth = models.DateField(blank=False)
    years_of_experience = models.IntegerField(blank=False)
    department_id = models.IntegerField(choices=DEPARTMENT_CHOICES, blank=False)
    resume = models.FileField(upload_to='documents/')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name
    
    def __repr__(self):
        return f"<Candidate(full_name={self.full_name}, date_of_birth={self.date_of_birth}, years_of_experience={self.years_of_experience}, department_id={self.department_id}, email={self.email}, resume={self.resume})>"

