from django.urls import path
from users import views as userviews

app_name = 'users'

urlpatterns = [

    # hpme page
    path('home/', userviews.index, name='index'),

    # customer orders
    path('cusorders/<int:itemid>/<int:pc>/', userviews.CusOrdersViews, name='cusorders'),

    # update Orders
    path('updorders/<int:itemid>/<int:orderid>/', userviews.UpdateOrders, name='updorders'),

    # customer ratings and feedbacks
    path('crf/<int:itemid>/<int:pc>/', userviews.CusRatFeedView, name='crf'),

    # updating customer ratings and feedbacks
    path('crfupd/<int:itemid>/<int:crfid>/', userviews.UpdateCRF, name='crfupd'),

    # updating customer ratings and feedbacks
    path('delcrf/<int:itemid>/<int:crfid>/', userviews.DeleteCRF, name='delcrf'),

    # paypal checkout button
    path('buy/<int:amt>/<int:qnt>/<int:ordid>/', userviews.Payment, name='buy'),

    # paypal on approve
    path('oa/', userviews.OnApprove, name='oa'),

    # paypal payment success
    path('ps/', userviews.PaymentSuccess, name='ps'),
]