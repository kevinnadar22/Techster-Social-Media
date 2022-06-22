from django.shortcuts import render

def error(request, *args, **kwargs):
    context = {
        'error_title':'Internal Server Error',
        'status_code': 500,
        'error_message':'Internal Server Error',
    }
    return render(request, 'core/error.html', context=context)