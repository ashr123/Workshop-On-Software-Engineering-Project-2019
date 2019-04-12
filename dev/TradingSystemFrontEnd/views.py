from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    # Get an HttpRequest - the request parameter
    # perform operations using information from the request.
    # Return HttpResponse
    # return HttpResponse('Hello from Django!')
    list_teams = Team.objects.filter(team_level__exact="U09")
    context = {'youngest_teams': list_teams}
    return render(request, 'home.html', context)
