from django import forms
from .models import Club, ClubActivity
from django.utils import timezone


class ClubActivityForm(forms.ModelForm):
    class Meta:
        model = ClubActivity
        fields = ['activity_header', 'activity_is_active']


class ClubActivityForm(forms.Form):
    activity_header = forms.CharField(max_length=100, label='Activity Header')
    activity_content = forms.CharField(widget=forms.Textarea, label='Activity Content')
    activity_image = forms.ImageField(label='Activity Image')
    activity_club = forms.ModelChoiceField(queryset=Club.objects.all(), label='Activity Club')
    activity_date = forms.DateTimeField(label='Activity Date', initial=timezone.now)

