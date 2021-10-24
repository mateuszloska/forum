from django import forms
from django.forms.fields import MultipleChoiceField
from django.forms.models import ModelMultipleChoiceField
from django.forms.widgets import CheckboxSelectMultiple, SelectMultiple, TextInput
from .models import ForumGroup, UserProfile, Branch, Category
from io import open
from django.conf import settings

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
        print(self.cleaned_data)
        cleaned_data = self.cleaned_data

class EditUserProfile(forms.ModelForm):
    class Meta:
        model = UserProfile

        fields = '__all__'


class CreateBranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = '__all__'

class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

#Style form - used to define how the forum looks
class StyleForm(forms.Form):
    bg_color = forms.CharField(label="Background color:",
                widget=TextInput(attrs={'type':'color'}))
    main_panel = forms.CharField(label="Main panel background color:",
                widget=TextInput(attrs={'type':'color'}))
    branch_text_color = forms.CharField(label="Branch text color:",
                widget=TextInput(attrs={'type':'color'}))
    branch_bg_color = forms.CharField(label="Branch background color:",
                widget=TextInput(attrs={'type':'color'}))
    category_text_color = forms.CharField(label="Category text color:",
                widget=TextInput(attrs={'type':'color'}))
    category_bg_color = forms.CharField(label="Category background color:",
                widget=TextInput(attrs={'type':'color'}))

    def clean(self):
        cleaned_data = self.cleaned_data
        return cleaned_data

    def save(self):
        #Generating .css file
        dir = settings.BASE_DIR /'forum/static/style.css'
        with open(dir, 'w+') as file:
            file.write("body{{ \n\tbackground-color:{};\n}}\n".format(self.cleaned_data['bg_color']))
            file.write(".main-panel{{ \n\tbackground-color:{};\n}}\n".format(self.cleaned_data['main_panel']))
            file.write(".branch{{ \n\tbackground-color:{};\n\tcolor:{};\n}}\n".format(
                self.cleaned_data['branch_bg_color'],self.cleaned_data['branch_text_color']))
            file.write(".category{{ \n\tbackground-color:{};\n\tcolor:{};\n}}\n".format(
                self.cleaned_data['category_bg_color'],self.cleaned_data['category_text_color']))
