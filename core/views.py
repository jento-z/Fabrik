from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from .models import Profile, Post, LikePost, FollowersCount, ClosetItem, Outfit
from itertools import chain

### Third party imports
from rembg import remove
from PIL import Image
from io import BytesIO


@login_required
def create_outfit(request):
    # Fetch items by category to display in the dropdowns
    hats = ClosetItem.objects.filter(user=request.user, category='Hats')
    tops = ClosetItem.objects.filter(user=request.user, category='Tops')
    bottoms = ClosetItem.objects.filter(user=request.user, category='Bottoms')
    shoes = ClosetItem.objects.filter(user=request.user, category='Shoes')
    accessories = ClosetItem.objects.filter(user=request.user, category='Accessories')

    if request.method == 'POST':
        # Get selected items' IDs from the form
        hat_id = request.POST.get('hat')
        top_id = request.POST.get('top')
        bottom_id = request.POST.get('bottom')
        shoes_id = request.POST.get('shoes')
        accessories_id = request.POST.get('accessories')
        
        # Retrieve ClosetItem instances based on the selected IDs, or None if not selected
        hat = ClosetItem.objects.get(id=hat_id) if hat_id else None
        top = ClosetItem.objects.get(id=top_id) if top_id else None
        bottom = ClosetItem.objects.get(id=bottom_id) if bottom_id else None
        shoes = ClosetItem.objects.get(id=shoes_id) if shoes_id else None
        accessories = ClosetItem.objects.get(id=accessories_id) if accessories_id else None

        # Create the Outfit instance
        outfit = Outfit.objects.create(
            user=request.user,
            hat=hat,
            top=top,
            bottom=bottom,
            shoes=shoes,
            accessories=accessories
        )

        # Redirect to a page where the outfit is displayed or to the main outfits page
        return redirect('outfit_list')  # Replace 'outfit_list' with the name of your target URL

    context = {
        'hats': hats,
        'tops': tops,
        'bottoms': bottoms,
        'shoes': shoes,
        'accessories': accessories
    }
    return render(request, 'createoutfit.html', context)

# Create your views here.
@login_required(login_url='signin')
def index(request):
    #return HttpResponse('<h1>Welcome To Social Book</h1>')
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    # TODO: Need to only show following profile posts
    posts = Post.objects.all()

    return render(request, 'index.html', {'user_profile': user_profile, 'posts':posts})

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    # TODO: Need to only display following posts
    post = Post.objects.get(id=post_id)
    
    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('/')

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        return redirect('settings')

    return render(request, 'setting.html', {'user_profile': user_profile})

def signup(request):
    
    if request.method=="POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Password guidelines
        if password != password2:
            messages.info(request, 'Passwords Not Matching')
            return redirect('signup')
        elif len(password) < 8:
            messages.info(request, 'Password must contain at least 8 characters')
            return redirect('signup')
        elif password.isdigit():
            messages.info(request, 'Password cannot be entirely numeric')
            return redirect('signup')
        
        # Check if the username or email already exists
        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email Taken')
            return redirect('signup')
        elif User.objects.filter(username=username).exists():
            messages.info(request, 'Username Taken')
            return redirect('signup')
        else:
            # Create the user if all checks pass
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            
            # Log user in and redirect to settings page
            user_login = auth.authenticate(username=username, password=password)
            auth.login(request, user_login)

            # Create profile object for the new user
            user_model = User.objects.get(username=username)
            new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
            new_profile.save()
            
            return redirect('settings')
    else:        
        return render(request, 'signup.html')
    
def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request, "Credentials Invalid")
            return redirect('signin')
    else:
        return render(request, 'signin.html')

@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)

        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})

@login_required(login_url='signin')
def upload(request):

    if request.method == 'POST':
        user = request.user
        image= request.FILES.get('image_upload')
        item_name = request.POST.get('item_name', '')
        category = request.POST.get('category', '')

        if image:
            # Open the uploaded image
            original_image = Image.open(image)

            # Convert image to bytes and remove background
            image_bytes = BytesIO()
            original_image.save(image_bytes, format='PNG')
            image_bytes = image_bytes.getvalue()

            # Process image with rembg
            processed_image_data = remove(image_bytes)

            # Save the processed image as a new file
            processed_image = ContentFile(processed_image_data, name=f"processed_{image.name}")

            # Create a new ClosetItem instance
            new_item = ClosetItem.objects.create(
                user=user,
                item_name=item_name,
                category=category,
                image=processed_image
            )
            new_item.save()
            
        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_clothing = ClosetItem.objects.filter(user=user_object).order_by('-date_added')
    user_clothing_length = len(user_clothing)

    is_own_profile = (request.user == user_object)

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_clothing': user_clothing,
        'user_clothing_length': user_clothing_length,
        'is_own_profile': is_own_profile
    }

    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def follow (request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
        
    else:
        return redirect('/')