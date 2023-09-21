from django.shortcuts import render

# Create your views here.
def create_subject(request):
    
    context = {
        'page_title':'Create Class Subject',
    }
    return render(request, 'results/create_subject.html', context)
