from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from .models import Profile, Post, LikePost, FollowersCount, ClosetItem, Outfit
from itertools import chain
<<<<<<< HEAD
import random
=======
from .utils.weather import get_weather
>>>>>>> cb09a8e187d1094f3455c9190a5d4548042476f6

### Third party imports
from rembg import remove
from PIL import Image
from io import BytesIO

@login_required
def outfit_list(request):
    # Retrieve all outfits created by the logged-in user
    outfits = Outfit.objects.filter(user=request.user)

    # Pass the outfits to the template for display
    return render(request, 'outfit_list.html', {'outfits': outfits})

@login_required
def create_outfit(request):
    # Fetch items by category to display in the dropdowns
    hats = ClosetItem.objects.filter(user=request.user, category='Hats')
    tops = ClosetItem.objects.filter(user=request.user, category='Tops')
    bottoms = ClosetItem.objects.filter(user=request.user, category='Bottoms')
    shoes = ClosetItem.objects.filter(user=request.user, category='Shoes')
    accessories = ClosetItem.objects.filter(user=request.user, category='Accessories')

    ## Fetch current weather data
    weather_info = get_weather()
    current_temp = weather_info.get('current_temperature_fahrenheit', 'N/A')
    daily_high = weather_info.get('daily_high_fahrenheit', 'N/A')
    weather_classification = weather_info.get('weather_classification', 'Unknown')

    # Map weather classification to image file names
    weather_images = {
        "Sunny": "Sunny.png",
        "Sun with Cloud Cover": "SunWithCloudCover.png",
        "Sun with Cloud Cover and Rain": "SunWithCloudCoverandRain.png",
        "Cloud Cover and Rain": "CloudCoverandRain.png",
        "Cloud Cover": "CloudCover.png"
    }
    weather_image = weather_images.get(weather_classification, "SunWithCloudCover.png")  # Use a default image if classification is missing

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
            accessories=accessories,
        )

        # Redirect to a page where the outfit is displayed or to the main outfits page
        #return redirect('outfit_list')  # Replace 'outfit_list' with the name of your target URL
        return redirect('index')

    context = {
        'hats': hats,
        'tops': tops,
        'bottoms': bottoms,
        'shoes': shoes,
        'accessories': accessories,
        'current_temp': current_temp,
        'daily_high': daily_high,
        'weather_image': weather_image  # Add the image file path to the context
    }
    return render(request, 'createoutfit.html', context)

# Create your views here.
@login_required(login_url='signin')
def index(request):
    #return HttpResponse('<h1>Welcome To Social Book</h1>')
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    user_following_list = []
    feed = []

    #show only posts of following
    user_following = FollowersCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)

    #show user's posts in their own feed
    user_posts = feed_lists = Post.objects.filter(user=request.user.username)
    feed.append(user_posts)
    
    feed_list = list(chain(*feed))

    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)

    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if (x not in list(current_user))]

    random.shuffle(final_suggestions_list)


    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))
    # TODO: Need to only show following profile posts
    # posts = Post.objects.all()

    return render(request, 'index.html', {'user_profile': user_profile, 'posts':feed_list, 'suggestions_username_profile_list': suggestions_username_profile_list[:4]})

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

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))

    is_own_profile = (request.user == user_object)

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_clothing': user_clothing,
        'user_clothing_length': user_clothing_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
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