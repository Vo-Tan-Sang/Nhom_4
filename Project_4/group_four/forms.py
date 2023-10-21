from django import forms
from django.contrib.auth.models import User
from group_four.models import BlogPost,Profile

# class UserForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput())
#     class Meta():
#         model = User
#         fields = ('username','email','password')
class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title','slug','content','image']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nhập Tên Bài Viết'}),
            'slug': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Copy the title with no space'}),
            'content': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Nhập Nội Dung'}),
        }
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_no', 'bio', 'facebook', 'instagram', 'linkedin', 'image', )