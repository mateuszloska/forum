from django import forms
from django.conf import settings
from django.forms import widgets
from django.forms.fields import CharField, MultipleChoiceField
from django.forms.models import ModelMultipleChoiceField
from django.forms.widgets import CheckboxSelectMultiple, HiddenInput, SelectMultiple, TextInput
from io import open
import json
from PIL import Image
from .models import ForumGroup, UserProfile, Branch, Category, Thread, Post

#Form for adding forum groups
class ForumGroupForm(forms.ModelForm):
    class Meta:
        model = ForumGroup

        widgets = {
            'color': TextInput(attrs={'type':'color'}),
        }


        fields = ['group_name', 'color', 'sign', 'permissions']

    def clean(self):
        cleaned_data = self.cleaned_data
        if ForumGroup.objects.filter(group_name__iexact=cleaned_data['group_name']).count() > 0:
            raise forms.ValidationError("The group name must be unique")


#Form for editing forum groups
class ForumGroupEditForm(forms.ModelForm):

    class Meta:
        model = ForumGroup
        widgets = {
            'color': TextInput(attrs={'type':'color'}),
        }

        fields = ['group_name', 'color', 'sign', 'permissions']

    def clean(self):
        cleaned_data = self.cleaned_data

class EditUserProfile(forms.ModelForm):
    class Meta:
        model = UserProfile

        fields = '__all__'


class CreateBranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        exclude = ('slug',)


class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ('slug',)

class CreateThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        exclude = ('slug','date_created')

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('slug','date_created')

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']

    def clean(self):
        cleaned_data = self.cleaned_data

        return cleaned_data

#Style form - used to define how the forum looks
class StyleForm(forms.Form):
    initials = {}
    try:
        dir = settings.BASE_DIR /'forum/static/style.json'
        file = open(dir)
        initials = dict(json.load(file))
        file.close()
    except:
        initials = {
            'bg_color':'#77767b',
            'main_panel':'#f6f5f4',
            'branch_text_color':'#241f31',
            'branch_bg_color':'#000000',
            'category_bg_color':'#3d3846',
            'category_text_color':'#000000',
        }



    bg_color = forms.CharField(label="Background color:",
                widget=TextInput(attrs={'type':'color'}),
                initial=initials['bg_color'])
    main_panel = forms.CharField(label="Main panel background color:",
                widget=TextInput(attrs={'type':'color'}),
                initial=initials['main_panel'])
    branch_text_color = forms.CharField(label="Branch text color:",
                widget=TextInput(attrs={'type':'color'}),
                initial=initials['branch_text_color'])
    branch_bg_color = forms.CharField(label="Branch background color:",
                widget=TextInput(attrs={'type':'color'}),
                initial=initials['branch_bg_color'])
    category_text_color = forms.CharField(label="Category text color:",
                widget=TextInput(attrs={'type':'color'}),
                initial=initials['category_text_color'])
    category_bg_color = forms.CharField(label="Category background color:",
                widget=TextInput(attrs={'type':'color'}),
                initial=initials['category_bg_color'])

    def clean(self):
        cleaned_data = self.cleaned_data
        return cleaned_data

    def save(self):

        #Generating .json file
        dir = settings.BASE_DIR /'forum/static/style.json'
        with open(dir, 'w+') as file:
            json.dump(self.cleaned_data,file)

        #Generating .css file
        dir = settings.BASE_DIR /'forum/static/style.css'
        with open(dir, 'w+') as file:
            file.write("body{{ \n\tbackground-color:{};\n}}\n".format(self.cleaned_data['bg_color']))
            file.write(".main-panel{{ \n\tbackground-color:{};\n}}\n".format(self.cleaned_data['main_panel']))
            file.write(".branch{{ \n\tbackground-color:{};\n\tcolor:{};\n}}\n".format(
                self.cleaned_data['branch_bg_color'],self.cleaned_data['branch_text_color']))
            file.write(".category{{ \n\tbackground-color:{};\n\tcolor:{};\n}}\n".format(
                self.cleaned_data['category_bg_color'],self.cleaned_data['category_text_color']))
            file.write("a{{ \n\ttext-decoration:none;\n\tcolor:{};\n\tfont-size:15px;\n}}\n".format(self.cleaned_data['category_text_color']))
