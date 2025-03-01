from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.http import HttpResponse

from vault.models.candidate import Candidate
from vault.helpers.validations import CandidateForm

from vault.models.candidate import DEPARTMENT_CHOICES

@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    try:
        # Check if the request body is empty
        if len(request.POST) == 0:
            return JsonResponse({"error": "Request body is required"}, status=400)
            
        # Parse the request body as dictionary
        data = CandidateForm(request.POST, request.FILES)

        if not data.is_valid():
            return JsonResponse({"error": data.errors}, status=400)
        

        # Create the candidate object
        candidate = Candidate(
            full_name=data.cleaned_data.get('full_name'),
            date_of_birth=data.cleaned_data.get('date_of_birth'),
            years_of_experience=data.cleaned_data.get('years_of_experience'),
            department_id=data.cleaned_data.get('department_id'),
            resume=data.cleaned_data.get('resume'),
            email=data.cleaned_data.get('email')
        )
        
        # Save the candidate object
        candidate.save()

        return JsonResponse({"message": "Candidate registered successfully"}, status=201)

    except Exception as e:
        if request.method != "POST":
            return JsonResponse({"error": "Only POST requests are allowed"}, status=405)
        else:
            return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def list_candidates(request):
    try:
        # TODO: will be moved to a middleware class in a separate file
        if request.headers.get('X-ADMIN') != '1':
            return JsonResponse({"error": "Unauthorized"}, status=401)
        
        # Validate department ID exists in choices
        department_id = int(request.GET.get('department_id')) if request.GET.get('department_id') else None
        
        candidates = Candidate.objects.filter(department_id=department_id) if department_id else Candidate.objects.all()
        paginator = Paginator(candidates, 10)
        
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
            'department_id': c.department_id,
            'resume': c.resume.url if c.resume else None,
            'created_at': c.created_at.isoformat(),
            'updated_at': c.updated_at.isoformat()
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
        # TODO: will be moved to a middleware class in a separate file
        # if request.headers.get('X-ADMIN') != '1':
        #     return JsonResponse({"error": "Unauthorized"}, status=401)

        candidate = Candidate.objects.get(id=candidate_id)
        
        resume_path = candidate.resume.path
        with open(resume_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{candidate.resume.name}"'
            return response
        
    except Candidate.DoesNotExist:
        return JsonResponse({"error": "Candidate not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)