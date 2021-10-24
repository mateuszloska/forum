from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse
from .decorators import forum_group_manager
from .models import ForumGroup, Branch, Category
from .forms import ForumGroupForm, ForumGroupEditForm, CreateBranchForm, CreateCategoryForm, StyleForm

def main_page_view(request, *args, **kwargs):
    context = {}

    if request.user.is_authenticated:
        permissions = []

        #making forum elements visible
        if request.user.profile.group is not None:
            for p in request.user.profile.group.permissions.all():
                permissions.append(p.name)
            context['permissions'] = permissions
            context['branches'] = Branch.objects.all()

    return render(request, 'forum/main_page.html', context)

@forum_group_manager
def manage_groups_view(request, *args, **kwargs):
    groups = ForumGroup.objects.all()
    context = {'groups':groups}

    form = ForumGroupForm()
    if request.method == 'POST':
        form = ForumGroupForm(request.POST or None)

        if form.is_valid():
            form.save()
            form = ForumGroupForm()
        
    context['form'] = form

    return render(request, 'forum/manage_groups.html', context)

@forum_group_manager
def update_group_view(request, group, *args, **kwargs):
    to_edit = ForumGroup.objects.get(slug=group)
    current_data = {'group_name' : to_edit.group_name,
                    'color': to_edit.color,
                    'sign': to_edit.sign,
                    'permissions': to_edit.permissions}

    print(to_edit.permissions)
    form = ForumGroupEditForm(current_data)
    context= {'group':group,
            'form':form}

    if request.method == 'POST':
        form = ForumGroupEditForm(request.POST)
        if form.is_valid():
            to_edit.group_name = form.cleaned_data['group_name']
            to_edit.color = form.cleaned_data['color']
            to_edit.sign = form.cleaned_data['sign']
            to_edit.permissions.set(form.cleaned_data['permissions'])
            to_edit.save()
            return redirect(reverse('forum:manage_groups'))

    return render(request, 'forum/update_group.html', context)


@forum_group_manager
def remove_group_view(request, group, *args, **kwargs):
    context= {'group':group}
    if request.method == 'POST':
        to_delete = ForumGroup.objects.get(slug=group)
        to_delete.delete()
        return redirect(reverse('forum:manage_groups'))

    return render(request, 'forum/remove_group.html', context)

@forum_group_manager
def user_list_view(request, *args, **kwargs):
    users = User.objects.all()
    
    context={'users':users}
    print(context)

    return render(request, 'forum/user_list.html', context)


def create_branch_view(request, *args, **kwargs):
    form = CreateBranchForm()
    if request.method == 'POST':
        form = CreateBranchForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect(reverse('forum:main_page'))
    return render(request, 'forum/create_branch.html', {'form':form})
    

def create_category_view(request, *args, **kwargs):
    form = CreateCategoryForm()
    if request.method == 'POST':
        form = CreateCategoryForm(request.POST or None)
        print("One")
        if form.is_valid():
            print("Two")
            form.save()
            print("Three")
            return redirect(reverse('forum:main_page'))
    return render(request, 'forum/create_category.html', {'form':form})


def forum_style_view(request, *args, **kwargs):
    form = StyleForm()

    if request.method == "POST":
        form = StyleForm(request.POST or None)
        if form.is_valid():
            form.save()
            form = StyleForm()

    return render(request, 'forum/forum_style.html', {'form':form})

