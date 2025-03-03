from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db import IntegrityError

from vault.models.candidate import Candidate, DEPARTMENT_CHOICES
from vault.utils.validations import CandidateForm

@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    try:
        # Check if the request body is empty
        if len(request.POST) == 0:
            return JsonResponse({"error": "Request body is required"}, status=400)
            
        # Parse and validate form data
        form = CandidateForm(request.POST, request.FILES)

        if not form.is_valid():
            return JsonResponse({"error": form.errors}, status=400)
        
        # Create candidate instance without file first
        candidate = Candidate(
            full_name=form.cleaned_data['full_name'],
            date_of_birth=form.cleaned_data['date_of_birth'],
            years_of_experience=form.cleaned_data['years_of_experience'],
            department_id=form.cleaned_data['department_id'],
            email=form.cleaned_data['email']
        )

        # Try to save without file first to check for unique constraint
        candidate.save()
        
        # If save succeeds, then handle file upload
        if form.cleaned_data.get('resume'):
            candidate.resume = form.cleaned_data['resume']
            candidate.save()

        return JsonResponse({"message": "Candidate registered successfully"}, status=201)

    except IntegrityError:
        return JsonResponse({"error": "A candidate with this email already exists"}, status=400)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



@csrf_exempt
@require_http_methods(["GET"])
def list_candidates(request):
    try:
        if request.headers.get('X-ADMIN') != '1':
            return JsonResponse({"error": "Unauthorized"}, status=401)
        
        # Validate department ID exists in choices
        department_id = int(request.GET.get('department_id')) if request.GET.get('department_id') else None
        
        # Get all candidates, filtered by department if specified
        if department_id:
            candidates = Candidate.objects.filter(department_id=department_id).order_by('created_at')
        else:
            candidates = Candidate.objects.all().order_by('created_at')

        count = int(request.GET.get('count', 10))
        
        paginator = Paginator(candidates, count)
        
        page_number = int(request.GET.get('page', 1))
        # Validate page number is within range
        if page_number < 1 or page_number > paginator.num_pages:
            return JsonResponse({"error": f"Page number must be between 1 and {paginator.num_pages}"}, status=400)
            
        # Get page and serialize candidates
        page_obj = paginator.page(page_number)
        
        candidates_json = [{
            'id': c.id,
            'full_name': c.full_name,
            'email': c.email,
            'date_of_birth': c.date_of_birth.isoformat(),
            'years_of_experience': c.years_of_experience,
            'department': DEPARTMENT_CHOICES[c.department_id][1],
        } for c in page_obj]
        

        return JsonResponse({
            'candidates': candidates_json,
            'total_pages': paginator.num_pages,
            'current_page': page_obj.number
        }, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def download_resume(request, candidate_id):
    try:
        if request.headers.get('X-ADMIN') != '1':
            return JsonResponse({"error": "Unauthorized"}, status=401)

        candidate = Candidate.objects.get(id=candidate_id)
        
        content_type = 'application/pdf'
        if candidate.resume.name.endswith('.doc'):
            content_type = 'application/msword'
        elif candidate.resume.name.endswith('.docx'):
            content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        elif candidate.resume.name.endswith('.pdf'):
            content_type = 'application/pdf'
            
        response = HttpResponse(candidate.resume.read(), content_type=content_type)
        response['Access-Control-Expose-Headers'] = 'content-disposition'
        response['Content-Disposition'] = f'attachment; filename="{candidate.resume.name}"'
        return response
        
    except Candidate.DoesNotExist:
        return JsonResponse({"error": "Candidate not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)