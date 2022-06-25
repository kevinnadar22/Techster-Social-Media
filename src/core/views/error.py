from django.shortcuts import render

def error(request, *args, **kwargs):
    context = {
        'error_title':'Internal Server Error',
        'status_code': 500,
        'error_message':'Internal Server Error',
    }
    return render(request, 'core/error.html', context=context)

def my_custom_page_not_found_view(request, *args, **kwargs):
    context = {
        'error_title':'Page not found',
        'status_code': 404,
        'error_message':'Page not found',
    }
    return render(request, 'core/error.html', context=context)


def my_custom_error_view(request, *args, **kwargs):
    context = {
        'error_title':'Server Error',
        'status_code': 500,
        'error_message':'Server Error',
    }
    return render(request, 'core/error.html', context=context)

def my_custom_permission_denied_view(request, *args, **kwargs):
    context = {
        'error_title':'Permission Denied',
        'status_code': 403,
        'error_message':'Permission Denied',
    }
    return render(request, 'core/error.html', context=context)


def my_custom_bad_request_view(request, *args, **kwargs):
    context = {
        'error_title':'Bad Request',
        'status_code': 400,
        'error_message':'Bad Request',
    }
    return render(request, 'core/error.html', context=context)