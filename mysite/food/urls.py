from django.urls import path
from food import views

app_name = 'food'

urlpatterns = [
    # function base index view
    #------------------------------------------------------------------------------------------------------------------------------------------
    path('home/', views.index, name='index'),

    # class base index view
    #------------------------------------------------------------------------------------------------------------------------------------------
    # path('home/', views.IndexClassView.as_view(), name= 'index'),

    # function base detail view
    #------------------------------------------------------------------------------------------------------------------------------------------
    path('detail/<int:item_id>/', views.detail, name='detail'),

    # class base detail view
    #------------------------------------------------------------------------------------------------------------------------------------------
    #path('detail/<int:pk>/', views.FoodDetail.as_view(), name='detail'),

    # function base create item view
    #------------------------------------------------------------------------------------------------------------------------------------------
    # path('add/', views.CreateItem, name='create_item'),

    # class base create item view
    #------------------------------------------------------------------------------------------------------------------------------------------
    path('add/', views.CreateItem.as_view(), name='create_item'),  

    # function base update item view
    #------------------------------------------------------------------------------------------------------------------------------------------
    path('update/<int:item_id>/', views.UpdateItem, name='update_item'),

    # function base delete item view
    #------------------------------------------------------------------------------------------------------------------------------------------
    path('delete/<int:item_id>/', views.DeleteItem, name='delete_item'),

    # navbar form
    #------------------------------------------------------------------------------------------------------------------------------------------
    path('navform/', views.NavForm, name='navform'),
]
