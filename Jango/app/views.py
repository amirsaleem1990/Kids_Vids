from django.shortcuts import render

def dashboard(request):
    try:
        print(request.POST)
    except:
        pass
    print('................ app.dashboard called')
    return render(request, 'dashboard.html', {"name" : "amir"})


def auth(request):
    print("\n------------------------------\n")
def add(request):
    email_ = request.POST["email_address"]
    password_ = request.POST["user_password"]
    print(email_)
    print(password_)