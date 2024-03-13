from django import forms
from food.models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['rest_owner', 'prod_code', 'item_name', 'item_desc', 'item_price', 'item_image']