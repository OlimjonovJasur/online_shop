from django import forms
from phonenumber_field.modelfields import PhoneNumberField

from shop.models import Comment


class OrderForm(forms.Form):
    full_name = forms.CharField()
    phone_number = PhoneNumberField(region='UZ')
    quantity = forms.IntegerField()


class OrderModelForm(forms.Form):
    pass


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
