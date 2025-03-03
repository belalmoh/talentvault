from django.shortcuts import render

def get_docs(request):
    return render(request, 'vault/docs.html')