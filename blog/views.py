from django.shortcuts import redirect, render

def start(request):
    return redirect('home')

def error(request, error):
    message=''
    if error == "profile_not_found":
        message = "Sorry, couldnt find a profile"
    elif error == "post_not_found":
        message = "Sorry, couldnt find a post for you :("
    return render(request, 'error.html', {'message':message})
