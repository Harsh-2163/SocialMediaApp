from django.shortcuts import render,redirect
from .models import CustomUser,Profile,Post

from django.contrib.auth.decorators import login_required
# Create your views here.
from django.contrib import auth



def index(request):
    return render(request,'index.html')

def signUpPage(request):

    if request.method == 'POST':
        email = request.POST['email']
        name = request.POST['name']
        password = request.POST['password']
        password1 = request.POST['password1']

        if password == password1:
            if CustomUser.objects.filter(email=email).exists():
                return render(request,'signup.html',{'error':'Email already used.! Try different one!!'})
            else:
                user = CustomUser.objects.create_user(email=email,password=password)
                user.save()

                user_login = auth.authenticate(email=email, password=password)
                auth.login(request, user_login)

                user_model = CustomUser.objects.get(email=email)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            return render(request,'signup.html',{'error':'Passwords does not match! Enter again'})

    else:
        return render(request,'signup.html')

def signIn(request):
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request,'index.html',{'error':'Invalid Credentials..Try again!!'})
    else:
        return render(request, 'index.html')


@login_required(login_url='signin')
def home(request):
    user_profile = request.user.prof_obj
    return render(request,'home.html',{'user_profile':user_profile})

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return render(request,'index.html')

@login_required(login_url='signin')
def settingsPage(request):
    user_profile = request.user.prof_obj
    if request.method == 'POST':

        if request.FILES.get('image') == None:

            image = user_profile.profileimg
            bio = request.POST['about']
            location = request.POST['location']
        
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location

            user_profile.save()
        
        if request.FILES.get('image') != None:

            image = request.FILES.get('image')
            bio = request.POST['about']
            location = request.POST['location']
        
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location

            user_profile.save()

        return render(request,'settings.html',{'user_profile':user_profile})
    return render(request,'settings.html',{'user_profile':user_profile})


@login_required(login_url='signin')
def upload(request):

    if request.method == 'POST':
        user = request.user
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user = user, image = image, caption = caption)
        new_post.save()
        return render(request,'home.html')
    else:
        return render(request,'home.html')