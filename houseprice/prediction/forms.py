from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

# Registration Form
class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields must match.")

        if len(password1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")

        return password2

class PredictionForm(forms.Form):
    number_of_rooms = forms.FloatField()
    number_of_bathrooms = forms.FloatField()
    number_of_floors = forms.FloatField()
    area = forms.FloatField()
    road_width = forms.FloatField()
    amenities_count = forms.IntegerField()
    city = forms.ChoiceField(choices=[('Bhaktapur', 'Bhaktapur'), ('Kathmandu', 'Kathmandu'), ('Lalitpur', 'Lalitpur')])
    road_type = forms.ChoiceField(choices=[('Blacktopped', 'Blacktopped'), ('Gravelled', 'Gravelled'), ('Soil Stabilized', 'Soil Stabilized')])


class ForgotPasswordForm(forms.Form):
    username = forms.CharField(max_length=150, label="Username")
    first_name = forms.CharField(max_length=30, label="First Name")
    last_name = forms.CharField(max_length=30, label="Last Name")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username does not exist.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        try:
            user = User.objects.get(username=username)
            if user.first_name != first_name or user.last_name != last_name:
                raise forms.ValidationError("First name or last name is incorrect.")
        except User.DoesNotExist:
            raise forms.ValidationError("Username does not exist.")
        return cleaned_data

# Password Reset Form
class PasswordResetForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput, label="New Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password != confirm_password:
            raise forms.ValidationError("The passwords do not match.")
        return cleaned_data
