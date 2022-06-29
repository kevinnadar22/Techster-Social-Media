from django.shortcuts import redirect, render

def home(request):
    """
    It takes a request object and returns a response object
    
    :param request: The request is an HttpRequest object
    :return: The home page is being returned.
    """
    return render(request, 'auth/home.html')