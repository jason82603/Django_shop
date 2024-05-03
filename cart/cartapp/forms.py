# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    # def clean_password2(self):
    #     password1 = self.cleaned_data.get("password1")
    #     password2 = self.cleaned_data.get("password2")
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError("密碼確認不匹配")
    #     return password2
    #
    # def clean(self):
    #     print('clean')
    #     cleaned_data = super().clean()
    #     self.clean_password2()  # 呼叫 clean_password2() 方法來驗證密碼確認字段
    #     return cleaned_data
