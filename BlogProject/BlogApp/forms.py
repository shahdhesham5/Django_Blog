from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#a modified UserCreationForm so we can add a new field(email)
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']