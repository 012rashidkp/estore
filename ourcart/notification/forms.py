from django import forms



class TestNotification(forms.Form):
    user_id = forms.IntegerField()
    title=forms.CharField()
    body=forms.CharField()
    icon_url=forms.CharField(help_text="Images to display")
    url=forms.CharField(help_text="url to open by clicking")
    