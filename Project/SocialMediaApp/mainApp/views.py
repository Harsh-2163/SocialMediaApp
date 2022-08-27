from cmath import log
import email
from django.shortcuts import render,redirect
from .models import CustomUser, Follower, LikePost,Profile,Post

from django.contrib.auth.decorators import login_required
# Create your views here.
from django.contrib import auth
from itertools import chain
import random

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
                new_profile = Profile.objects.create(user=user_model,userName=name,id_user=user_model.id)
                new_profile.save()
                return render(request,'settings.html')
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

    #post_list = Post.objects.all()

    ## correct post feed - of only of one we following.
    user_following_list = []
    feed = []

    user_obj = CustomUser.objects.get(email = request.user.email)
    following_list = Follower.objects.filter(followed_by = user_obj)

    for followed in following_list:
        user_following_list.append(followed.following_to)

    for user in user_following_list:
        posts = Post.objects.filter(user = user)
        feed.append(posts)

    feed_list = list(chain(*feed))
    feedLen = len(feed_list)
    user_following_all = []

    ## user suggestion list
    all_users = CustomUser.objects.all()
    for followed in following_list:
        user_list = CustomUser.objects.get(email = followed.following_to.email)
        user_following_all.append(user_list)

    
    suggestion_list = [x for x in list(all_users) if (x not in list(user_following_list))]
    final_suggestion_list = [x for x in list(suggestion_list) if (x != user_obj and x.email != 'admin@gmail.com')]
    random.shuffle(final_suggestion_list)

    return render(request,'home.html',{'user_obj':user_obj,'user_profile':user_profile,'feedLen':feedLen,'feed':feed_list,'suggested_users':final_suggestion_list})

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return render(request,'index.html')

@login_required(login_url='signin')
def settingsPage(request):
    user_profile = request.user.prof_obj
    if request.method == 'POST':

        if request.FILES.get('image') == None and request.FILES.get('coverimg') == None:

            image = user_profile.profileimg
            coverimg = user_profile.coverimg
            bio = request.POST['about']
            location = request.POST['location']
        
            user_profile.profileimg = image
            user_profile.coverimg = coverimg
            user_profile.bio = bio
            user_profile.location = location

            user_profile.save()
        
        if request.FILES.get('image') != None and request.FILES.get('coverimg') != None:

            image = request.FILES.get('image')
            coverimg = request.FILES.get('coverimg')
            bio = request.POST['about']
            location = request.POST['location']
        
            user_profile.profileimg = image
            user_profile.coverimg = coverimg
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
        return redirect('home')
    else:
        return render(request,'home.html')

@login_required(login_url='signin')
def like_post(request):

    post_id = request.GET.get('post_id')
    user = request.user
    post = Post.objects.get(id = post_id)

    like_filter = LikePost.objects.filter(liked_post = post, liked_by_user = user).first()

    #if user press like button for first time
    if like_filter == None:
        new_like = LikePost.objects.create(liked_post=post,liked_by_user=user)
        new_like.save()
        post.no_of_likes = post.no_of_likes + 1
        post.save()
        return redirect('home')
    
    #if user press it again so dislike
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes - 1
        post.save()
        return redirect('home')


@login_required(login_url='signin')
def getProfile(request,pk):

    user_object = CustomUser.objects.get(email = pk)
    user_profile = user_object.prof_obj
    user_posts = user_object.post_set.all()
    user_post_length = len(user_posts)

    user_is_following = CustomUser.objects.get(email = request.user.email)
    user_being_followed = CustomUser.objects.get(email = pk)

    if Follower.objects.filter(following_to = user_being_followed, followed_by = user_is_following).first():
        button_text = 'UnFollow'
    else:
        button_text = 'Follow' 

    no_of_following = len(Follower.objects.filter(followed_by = user_object))
    no_of_followers = len(Follower.objects.filter(following_to = user_object))

    context = {
        'userObj' : user_object,
        'userProfile' : user_profile,
        'userPosts' : user_posts,
        'userPostsLength' : user_post_length,
        'button_text':button_text,
        'no_of_following' : no_of_following,
        'no_of_followers' : no_of_followers,
    }

    return render(request,'profile.html',context)


@login_required(login_url='signin')
def FollowUser(request):
    if request.method == 'POST':

        being_followed = request.POST['being_followed']
        is_following = request.POST['is_following']

        user_being_followed = CustomUser.objects.get(email = being_followed)
        user_is_following =CustomUser.objects.get(email = is_following)

        if Follower.objects.filter(following_to = user_being_followed, followed_by =user_is_following).first():
            foll = Follower.objects.get(following_to = user_being_followed,followed_by=user_is_following)
            foll.delete()
            return redirect('/getProfile/'+ being_followed)
        else:
            new_foll = Follower.objects.create(following_to=user_being_followed,followed_by=user_is_following)
            new_foll.save()
            return redirect('/getProfile/'+ being_followed)


@login_required(login_url='signin')
def search(request):
    user_object = CustomUser.objects.get(email = request.user.email)
    user_profile = user_object.prof_obj
    if request.method == 'POST':
        email = request.POST['search-email']
        user_object = CustomUser.objects.filter(email__icontains = email)

        user_profile = []
        user_profile_list = []

        for user in user_object:
            user_profile.append(user.id)

        for ide in user_profile:
            profile_lists = Profile.objects.filter(id_user = ide)
            user_profile_list.append(profile_lists)

        user_profile_list = list(chain(*user_profile_list))
    return render(request,'search_result.html',{'user_profile_list':user_profile_list})


@login_required(login_url='signin')
def myProfile(request):
    user = CustomUser.objects.get(email = request.user.email)
    myProfileObj = user.prof_obj
    myPosts = Post.objects.filter(user = user)
    myPostsLen = len(myPosts)

    myFollowing = Follower.objects.filter(followed_by = user)
    noOfFollowing = len(myFollowing)
    myFollowers = Follower.objects.filter(following_to = user)
    noOfFollowers = len(myFollowers)
    
    context = {
        'userObj':user,
        'myProfileObj':myProfileObj,
        'myPosts':myPosts,
        'myPostsLen':myPostsLen,
        'myFollowers':myFollowers,
        'noOfFollowers':noOfFollowers,
        'myFollowing':myFollowing,
        'noOfFollowing':noOfFollowing,
    }
    return render(request,'myProfile.html',context)

@login_required(login_url='signin')
def deletePost(request):
    id = request.POST['post-id']
    post = Post.objects.get(id = id)
    post.delete()
    return redirect('myProfile')