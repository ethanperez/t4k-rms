from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from riders.models import Teammate

# Form to create new riders in the admin area
class TeammateCreationForm(forms.ModelForm):
    
    # Ask for a password
    password1 = forms.CharField(label = 'Password', widget = forms.PasswordInput)
    password2 = forms.CharField(label = 'Password Confirmation',
                                widget = forms.PasswordInput)
    
    # Designates the model this form is for
    class Meta:
        model = Teammate
        
    # Validates the user's password
    def clean_password2(self):
        # Make sure the two passwords match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            # If not, tell the user
            raise forms.ValidationError("The passwords don't match!")
        return password2
    
    # Saves the new teammate into the database
    def save(self, commit = True):
        user = super(TeammateCreationForm, self).save(commit = False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
        
# Form to change teammates in the admin area
class TeammateChangeForm(forms.ModelForm):
    
    # Displays the password as a hash field
    password = ReadOnlyPasswordHashField()
    
    # Metadata points to the appropriate model to modify
    class Meta:
        model = Teammate
        
    # Returns the user's initial password
    def clean_password(self):
        return self.initial["password"]