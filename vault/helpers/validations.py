from django import forms
from vault.models.candidate import DEPARTMENT_CHOICES
from datetime import datetime


ALLOWED_FILE_TYPES = ["application/pdf", "application/docx", "application/doc"]  # Define allowed MIME types
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB file size limit

class CandidateForm(forms.Form):

    full_name = forms.CharField(min_length=5, max_length=255, required=True)
    date_of_birth = forms.DateField(required=True, input_formats=['%Y-%m-%d'])
    years_of_experience = forms.IntegerField(required=True)
    department_id = forms.IntegerField(required=True)
    resume = forms.FileField(required=True)
    email = forms.EmailField(required=True)

   
    # Validate the date of birth
    def date_of_birth_validator(self):
        if self.cleaned_data.get('date_of_birth') > datetime.now().date():
            raise forms.ValidationError("Date of birth cannot be in the future.")
        return self.cleaned_data.get('date_of_birth')

    # Validate the years of experience
    def years_of_experience_validator(self):
        if self.cleaned_data.get('years_of_experience') < 0:
            raise forms.ValidationError("Years of experience cannot be negative.")
        return self.cleaned_data.get('years_of_experience')

    # Validate the resume file
    def clean_resume(self):
        file = self.cleaned_data.get('resume')
        if file:
            if file.size > MAX_FILE_SIZE:
                raise forms.ValidationError("File size exceeds the maximum limit of 10 MB.")
            if file.content_type not in ALLOWED_FILE_TYPES:
                raise forms.ValidationError("Invalid file type. Only PDF, DOCX, and DOC files are allowed.")
        return file
    
    # Validate the department ID
    def clean_department_id(self):
        department_id = self.cleaned_data.get('department_id')
        if department_id not in [choice[0] for choice in DEPARTMENT_CHOICES]:
            choices_str = ", ".join([f"{choice[0]} ({choice[1]})" for choice in DEPARTMENT_CHOICES])
            raise forms.ValidationError(f"Invalid department ID, possible values are: {choices_str}")
        return department_id
