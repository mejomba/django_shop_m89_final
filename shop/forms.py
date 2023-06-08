from django import forms

from shop.models import Comment


class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}),
                              label='نظر شما')
    rating = forms.IntegerField(widget=forms.NumberInput(attrs={'type': 'range', 'min': '1', 'max': '5', 'value': '5'}),
                                label='امتیاز')
    parent_comment = forms.IntegerField(widget=forms.HiddenInput(), initial=0)


# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = '__all__'

    # content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}),
    #                           label='نظر شما')
    # rating = forms.IntegerField(widget=forms.NumberInput(attrs={'type': 'range', 'min': '1', 'max': '5', 'value': '5'}),
    #                             label='امتیاز')
    # parent_comment = forms.IntegerField(widget=forms.HiddenInput(), initial=1)