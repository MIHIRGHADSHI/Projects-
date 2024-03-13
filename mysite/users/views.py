from django.shortcuts import render, redirect
from users.forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from users.forms import CusOrdersForm
from django.contrib.auth.decorators import login_required
from food.models import Item
from users.models import CusOrders, CusRatingsFeedbacks
from users.forms import CusRateFeedForm
from users.models import Profile
from users.forms import ProfileForm
from django.http import JsonResponse
import json

# Create your views here.

def index(request):

    context = {

    }

    return render(request, 'users/home.html', context)


# register
#-------------------------------------------------------------------------------------------------------------
def register(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            messages.success(
                request,
                'Welcome, {} your account has been successfully created'.format(username)
            )

            regid = form.instance.id
            return redirect('profformcreate', regid)
        
        else:
            return redirect('register')

    else:
        form = RegisterForm(None)

    context = {
        'form':form
    }
    
    return render(request, 'users/register.html', context)


# Login view
# ------------------------------------------------------------------------------------------
def login_view(request):
    
    if request.method == "POST":

        # using username
        # ---------------------------------------------
        username = request.POST['username']
        password = request.POST['password']

        # using first name
        # -------------------------------------------
        # firstname = request.POST['firstname']
        # password = request.POST['password']
        # userobj = User.objects.get(first_name=firstname)
        # username=userobj.username

        user = authenticate(username=username, password=password)

        if user is None:
            messages.success(
                request,
                'invalid id login, try again'
            )
            return redirect('login')
        
        if user.is_superuser:
            messages.success(
                request,
                'Welcome superuser {}, you have been successfully logged in'.format(username)
            )
            login(request, user)
            return redirect('profile')
        
        if user is not None:
            messages.success(
                request,
                'Welcome {}, you have been successfully logged in'.format(username)
            )
            login(request, user)
            return redirect('profile')

    context = {

    }

    return render(request, 'users/login.html', context)

# Logout view
# ------------------------------------------------------------------------------------------
def logout_view(request):

    if request.method == 'POST':
        logout(request)
        return redirect('food:index')

    return render(request, 'users/logout.html')


# Profile
# -------------------------------------------------------------------------------------
def ProfilePage(request):

    context = {
        
    }

    return render(request, 'users/profile.html', context) 


# Profile view login_required
# -------------------------------------------------------------------------------------
# @login_required
# def ProfilePage(request):

#     context = {
        
#    }

#    return render(request, 'users/profile.html', context) 

# Profile view login_required
# -------------------------------------------------------------------------------------
def ProfilePage(request):

    if not request.user.is_authenticated:
        return redirect('login')

    context = {
        
    }

    print(request.user.email)
    
    return render(request, 'users/profile.html', context) 

# Customer Orders view 
# -------------------------------------------------------------------------------------
def CusOrdersViews(request, itemid, pc):

    form = CusOrdersForm(request.POST or None)

    if request.method == 'POST':
        form.instance.prod_code = pc
        form.instance.username = request.user.username
        if form.is_valid():
            form.save()
            return redirect('food:detail', item_id=itemid)

    context ={
        'form': form
    }

    return render(request, 'users/cusorders.html', context)


# Update Customer Orders view 
# -------------------------------------------------------------------------------------
def UpdateOrders(request, itemid, orderid):
    
    CusOrds = CusOrders.objects.get(order_id=orderid)
    form = CusOrdersForm(request.POST or None, instance=CusOrds)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('food:detail', item_id=itemid)

    context = {
        'form':form
    }

    return render(request, 'users/cusorders.html', context)


# Customer Ratings and Feedbacks
# -------------------------------------------------------------------------------------
def CusRatFeedView(request, itemid, pc):
    
    form = CusRateFeedForm(request.POST or None)

    if request.method == 'POST':
        form.instance.prod_code = pc
        form.instance.username = request.user.username
        if form.is_valid():
            if form.instance.ratings < 0:
                messages.success(
                    request,
                    'Ratings Cannot Be Negative'
                )
                return redirect('users:crf', itemid=itemid, pc=pc)
            form.save()
            return redirect('food:detail', item_id=itemid)

    context = {
        'itemid':itemid,
        'pc':pc,
        'form':form

    }

    return render(request, 'users/cusratfeed.html', context)


# Update Customer Ratings & Feedbacks
# --------------------------------------------------------------------------------------------------------------------------------------------
def UpdateCRF(request, itemid, crfid):

    crfo = CusRatingsFeedbacks.objects.get(pk=crfid)
    form = CusRateFeedForm(request.POST or None, instance=crfo)

    context = {
        'form':form
    }

    if form.is_valid():
        form.save()
        return redirect('food:detail', item_id=itemid)

    return render(request, 'users/cusratfeed.html', context)



# Delete Customer Ratings & Feedbacks
# --------------------------------------------------------------------------------------------------------------------------------------------
def DeleteCRF(request, itemid, crfid):

    crfo = CusRatingsFeedbacks.objects.get(pk=crfid)

    if request.method == 'POST':
        crfo.delete()
        return redirect('food:detail', item_id=itemid)

    context = {
        'crfo':crfo,
        'itemid':itemid

    }

    return render(request, 'users/delcusratfeed.html', context)



# Delete Customer Ratings & Feedbacks
# --------------------------------------------------------------------------------------------------------------------------------------------
def ProfFormEdit(request, userid):

    prof = Profile.objects.get(user=userid)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=prof)
    
    if request.method == 'POST':
        form.save()
        return redirect('profile')

    context = {
        'userid':userid,
        'form':form
    }

    return render(request, 'users/profform.html', context)


# Delete Customer Ratings & Feedbacks
# --------------------------------------------------------------------------------------------------------------------------------------------
def ProfFormCreate(request, userid):

    prof = Profile.objects.get(user=userid)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=prof)

    if request.method == 'POST':
        form.save()
        return redirect('login')

    context = {
        'userid':userid,
        'form':form 
    }

    return render(request, 'users/profform.html', context)


# Delete Customer Ratings & Feedbacks
# --------------------------------------------------------------------------------------------------------------------------------------------
def Payment(request, amt, qnt, ordid):

    context = {
        'amt':amt,
        'qnt':qnt,
        'tot':amt * qnt,
        'ordid':ordid
    }

    return render(request, 'users/payment.html', context)


# Delete Customer Ratings & Feedbacks
# --------------------------------------------------------------------------------------------------------------------------------------------
def OnApprove(request):

    if request.method == 'POST':
        body = json.loads(request.body)
        print(body)

        context = {

        }

        return JsonResponse(context)


# Delete Customer Ratings & Feedbacks
# --------------------------------------------------------------------------------------------------------------------------------------------
def PaymentSuccess(request, ordid):

    context ={
        'ordid':ordid
    }

    return render(request, 'users/pymtsuccess.html', context)
