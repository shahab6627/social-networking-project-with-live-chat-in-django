from django.shortcuts import render, redirect
from django.http import response, JsonResponse
from .models import User, ProfilePicture, Post, PostLike, FriendRequest, UserChat
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .tasks import sendVerificationEmail


from django.db.models import Q

import datetime

# Create your views here.
def home(request):
    # if user is not authenticated then redirect to login 
    if request.user.is_authenticated:
        return redirect('profile')
    # ajax request 
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        name = request.POST.get('name')
        email = request.POST.get('email')
        gender = request.POST.get('gender')

        date = request.POST.get('date')
        password = request.POST.get('password')
        # checking if df email already exists
        if User.objects.filter(email = email).exists():
            return JsonResponse({'msg': 'exists'})
        user = User.objects.create_user(email = email, full_name=name, gender = gender, date_of_birth = date, password=password, profile_pic="")
        """ initially the is_active status of user will be false.
        user must activate account through email that was sent to the user """
        
        user.is_active = False
        user.save()
        # if user created then verification email will be send by using celery 
        if user:
            sendVerificationEmail.delay(email)
            return JsonResponse({'msg':'true'})
        return JsonResponse({'msg':'error'})
        
    return render(request, 'socialapp/index.html')



# activating account 
def activateAccount(request, email):
    verify = User.objects.filter(email = email)
    if verify:
        user = User.objects.get(email=email)
        # changing user is_active status to True
        user.is_active = True
        user.save()
        messages.add_message(request, messages.SUCCESS, 'your account is verified... You can now login to your account ')
        return redirect('userLogin')
    else:
        messages.add_message(request, messages.SUCCESS, 'your activation link not working')
        return render(request, "socialapp/login.html")
        
def userLogin(request):
    if request.user.is_authenticated:
        return redirect('profile')
    # ajax request 
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        email = request.POST.get('email')
        password = request.POST.get('password')
         
        user = authenticate(email=email,password=password)
        # if user authenticated then 
        if user is not None:
            login(request, user)
            return JsonResponse({'msg':'true'})
        else:
            return JsonResponse({'msg':'false'})
            
    return render(request, "socialapp/login.html")

# user must login if he/she wants to access profile 
@login_required(login_url=('userLogin'))
def userProfile(request):
    # getting all posts
    
    all_posts = Post.objects.all().select_related('user')
    # getting likes on post 
    likes = PostLike.objects.filter(user_id = request.user.id)
   
    dict = {
        'posts':all_posts,
        'likes':likes
    }
    # uploading posts 
    if request.method == "POST":
        post_content = request.POST['post_content']
        post_image = request.FILES.get('post_image')
        post_author = request.user
        
        post = Post.objects.create(post_content = post_content, post_image = post_image, user = post_author)
        post.save()
        return render(request, 'socialapp/profile.html', dict)
        
    
    return render(request, 'socialapp/profile.html', dict)

# uploading profile pic 
def uploadProfilePic(request):
    
    if request.method == "POST":
        image = request.FILES.get('profile-pic') 
        # uploading to all pictures
        imageu = ProfilePicture.objects.create(user=request.user, profile_pic = image)
        imageu.save()
        
        # changing as a profile picture 
        userprofile_pic = User.objects.get(email = request.user)
        userprofile_pic.profile_pic = image
        userprofile_pic.save()
        return redirect('profile')
    return render(request, 'socialapp/profile.html')

# accessing profiles 
@login_required(login_url=('userLogin'))
def otherUserProfile(request, id, full_name):
    
    profile_pics = ProfilePicture.objects.filter(user_id = id)
    user_data = User.objects.get(id = id)
    print(user_data)
    posts = Post.objects.filter(user_id = id).select_related('user')
    try:
        friend_status =FriendRequest.objects.filter(Q(sender=id, to=request.user.id)) | FriendRequest.objects.filter(Q(to=id, sender=request.user.id))
        for fr in friend_status:
            print(fr)
        # print("friends" ,friend_status)
        dict = {
        'posts':posts,
        'profile_pics':profile_pics,
        'user_data':user_data,
        'friend_status':friend_status
        
        }
    except Exception as e:
        print("except")
        dict = {
        'posts':posts,
        'profile_pics':profile_pics,
        'user_data':user_data,
        # 'friend_status':friend_status
        
        }
    
    return render(request, 'socialapp/otheruserprofile.html', dict)
    
# like a post 
def likePost(request):
    post_id = request.GET['post_id']
    #  if already liked then 
    check = PostLike.objects.filter(user = request.user, post_id=post_id).exists()
    if check:
        return JsonResponse({'msg':'false'})
    
    like_post = PostLike.objects.create(user = request.user, post_id=post_id)
    like_post.save()
    return JsonResponse({'msg':'true'})



# handel friend requests 
def handelFriendRequests(request):
    request_id = request.GET['request_id']
    check_friend = FriendRequest.objects.get(id = request_id)
    check_friend.status = "accepted"
    check_friend.updated = datetime.date.today()
    check_friend.save()
    return JsonResponse({'msg':'true'})


# chatting with friends using django channels on backend 
@login_required(login_url=('userLogin'))
def chat(request,slug):
    friend = FriendRequest.objects.get(slug = slug) 
    msgs = UserChat.objects.filter(friends_rel_id = friend.id).select_related('msg_from','msg_to')
    
    message_to_id = "" 
    if friend.sender_id == request.user.id:
        message_to_id = friend.sender_id
    message_to_id = friend.to_id

    dict = {
        'slug':slug, # passing slug to the template to make a websocket connection
        'msgs':msgs, # all messages b/w friends
        'friend_rel':friend.id, # relation id
        'message_to_id':message_to_id, # to whom msg will be send
        'friend':friend,
        }
    return render(request, 'socialapp/chat.html', dict)

# sending friend request 
def sendInvitation(request):
    send_from = request.GET['send_from']
    send_to = request.GET['send_to']
    
    send_request = FriendRequest.objects.create(sender_id = send_from, to_id = send_to)
    send_request.save()
    return JsonResponse({'msg':'true'})

# delete your post 
def deletePost(request):
    post_id = request.GET['post_id']
    post = Post.objects.get(id = post_id)
    if post is not None:
        post.delete()
        return JsonResponse({'msg':'true'})
    return JsonResponse({'msg':'false'})
    

def logoutUser(request):
    logout(request)
    
    return redirect('userLogin')