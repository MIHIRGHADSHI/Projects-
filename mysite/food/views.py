from django.forms.models import BaseModelForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from food.models import Item, History
from food.forms import ItemForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from users.models import CusOrders, CusRatingsFeedbacks
from django.core.paginator import Paginator



# Create your views here.

# function base index view
#------------------------------------------------------------------------------------------------------------------------------------------
def index(request):

    if request.user.is_superuser:
        itemlist  = Item.objects.all()

        # for search functionality
        item_name = request.GET.get('item_name')
        if item_name != '' and item_name is not None:
            itemlist = Item.objects.filter(item_name__icontains=item_name).order_by('item_price')

        # for pagination
        paginator = Paginator(itemlist, 3)
        page = request.GET.get('page')
        itemlist = paginator.get_page(page)

    elif request.user.is_authenticated and request.user.profile.user_type == 'rest':
        itemlist = Item.objects.filter(rest_owner=request.user.id).order_by('item_price')

         # for search functionality
        item_name = request.GET.get('item_name')
        if item_name != '' and item_name is not None:
            itemlist = Item.objects.filter(item_name__icontains=item_name).order_by('item_price')

    elif request.user.is_authenticated and request.user.profile.user_type == 'cust':
        itemlist = Item.objects.all().order_by('item_price')

         # for search functionality
        item_name = request.GET.get('item_name')
        if item_name != '' and item_name is not None:
            itemlist = Item.objects.filter(item_name__icontains=item_name).order_by('item_price')
        
    else:
        itemlist = Item.objects.all().order_by('item_price')

    context = {
        'itemlist':itemlist
    }
    return render(request, 'food/home.html', context)


# class base index view
#------------------------------------------------------------------------------------------------------------------------------------------
class IndexClassView(ListView):
    model = Item
    context_object_name = 'itemlist'
    template_name = 'food/home.html'


# function base detail view
#------------------------------------------------------------------------------------------------------------------------------------------
def detail(request, item_id):
    item = Item.objects.get(id=item_id)

    hist = History.objects.filter(
        prod_code=item.prod_code
    )

    crf =  CusRatingsFeedbacks.objects.filter(
        prod_code=item.prod_code
    )

    # resturant and admin
    if request.user.profile.user_type == 'rest' or request.user.profile.user_type == 'admin':
        coo = CusOrders.objects.filter(
            prod_code = item.prod_code,
            username=request.user.username
        )

    # customer
    elif request.user.profile.user_type == 'cust':
        coo = CusOrders.objects.filter(
            prod_code = item.prod_code,
            username = request.user.username
        )
    context = {
        'item':item,
        'hist':hist,
        'coo' :coo,
        'crf':crf
    }

    return render(request, 'food/detail.html', context)


# class base detail view
#------------------------------------------------------------------------------------------------------------------------------------------
class FoodDetail(DetailView):
    model = Item
    context_object_name = 'item'
    template_name = 'food/detail.html'



# function base create item view
#------------------------------------------------------------------------------------------------------------------------------------------
def CreateItem(request):

    form = ItemForm(request.POST or None)

    if request.method == 'POST':
        form.instance.added_by = request.user.username
        form.save()
        return redirect('food:index')
    
    context = {
        'form':form
    }
    return render(request, 'food/item-form.html', context)


# class base create item view
#------------------------------------------------------------------------------------------------------------------------------------------
class CreateItem(CreateView):
    model = Item
    fields = ['rest_owner', 'prod_code', 'item_name', 'item_desc', 'item_price', 'item_image']
    template_name = 'food/item-form.html'
    context_object_name = 'form'
    success_url = reverse_lazy('food:index')

    def form_valid(self, form):
        form.instance.added_by = self.request.user.username

        objhist = History(
            username=self.request.user.username,
            prod_code=form.instance.prod_code,
            item_name=self.request.POST.get('item_name'),   # self.request.POST['item_name]
            operation_type='created'
        )

        objhist.save()

        return super().form_valid(form)


# function base update item view
#------------------------------------------------------------------------------------------------------------------------------------------
def UpdateItem(request, item_id):

    item = Item.objects.get(id=item_id)
    form = ItemForm(request.POST or None, instance=item)

    if form.is_valid():
        form.save()

        objhist = History(
            username=request.user.username,
            prod_code=form.instance.prod_code,
            item_name=request.POST.get('item_name'),   # self.request.POST['item_name]
            operation_type='updated'
        )

        objhist.save()

        return redirect('food:detail', item_id)
    
    context = {
        'form':form
    }

    return render(request, 'food/item-form.html',context)

# function base delete view
#------------------------------------------------------------------------------------------------------------------------------------------
def DeleteItem(request, item_id):

    item = Item.objects.get(id=item_id)
    

    context = {
        'item':item
    }

    if request.method == 'POST':

        objhist = History(
            username=request.user.username,
            prod_code=item.prod_code,
            item_name=item.item_name,
            operation_type='deleted'
        )

        objhist.save()

        item.delete()
        return redirect('food:index')

    return render(request, 'food/item-delete.html', context)


# navbar form
# -------------------------------------------------------------------------------
def NavForm(request):

    path = request.POST.get('path_name')
    nfd = request.POST.get('navformdata')
    print(nfd)

    return redirect(str(path))