from django.http import HttpResponse

# Create your views here.
def health_check(request):
    return HttpResponse("OK", status=200)