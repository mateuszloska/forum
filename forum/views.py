from typing import List
from django.shortcuts import render, redirect, get_list_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.generic.list import ListView
from django.conf import settings
from .decorators import forum_group_manager
from .models import ForumGroup, Branch, Category, Thread, Post, UserProfile
from .forms import (ForumGroupForm, ForumGroupEditForm, 
CreateBranchForm, CreateCategoryForm, StyleForm,
CreatePostForm, CreateThreadForm, EditProfileForm)

def main_page_view(request, *args, **kwargs):
    context = {}
    permissions = []

    if request.user.is_authenticated:
        #defining permissions
        if request.user.profile.group is not None:
            for p in request.user.profile.group.permissions.all():
                permissions.append(p.name)

    #making forum elements visible
    context['branches'] = Branch.objects.all()
    context['permissions'] = permissions
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

    return render(request, 'forum/user_list.html', context)


def create_branch_view(request, *args, **kwargs):
    form = CreateBranchForm()
    if request.method == 'POST':
        form = CreateBranchForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect(reverse('forum:main_page'))
    return render(request, 'forum/create_branch.html', {'form':form})
    

def create_category_view(request, branch_slug, *args, **kwargs):
    br = Branch.objects.get(slug=branch_slug)
    form = CreateCategoryForm({'branch':br})
    if request.method == 'POST':
        form = CreateCategoryForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect(reverse('forum:main_page'))
    return render(request, 'forum/create_category.html', {'form':form})

def create_thread_view(request, category_slug, branch_slug, *args, **kwargs):
    cat = Category.objects.get(slug = category_slug)
    form = CreateThreadForm({'category':cat})
    if request.method == 'POST':
        form = CreateThreadForm(request.POST or None)
        if form.is_valid():
            form.save()
            th_slug = Thread.objects.filter(name=form.cleaned_data['name']).last().slug
            return redirect(reverse('forum:create_post', kwargs={
                "branch_slug":branch_slug,
                "category_slug":category_slug,
                "thread_slug":th_slug
            }))
    return render(request, 'forum/create_thread.html', {'form':form})

def create_post_view(request, branch_slug, category_slug, thread_slug, *args, **kwargs):
    th = Thread.objects.get(slug = thread_slug)
    author = request.user
    form = CreatePostForm({
        'thread':th,
        'author':author
    })
    if request.method == 'POST':
        form = CreatePostForm(request.POST or None)

        if form.is_valid():
            #for secure issues - author needs to be the current user
            if form.cleaned_data['author'] == request.user:
                form.save()
                return redirect(reverse('forum:thread', kwargs={
                    'thread_slug':thread_slug,
                    'category_slug':category_slug,
                    'branch_slug':branch_slug
                }))
    return render(request, 'forum/create_post.html', {'form':form})


def forum_style_view(request, *args, **kwargs):
    form = StyleForm(None)
    context = {'saved':False}

    if request.method == "POST":
        form = StyleForm(request.POST or None)
        if form.is_valid():
            form.save()
            context['saved']=True
    
    context['form']=form

    return render(request, 'forum/forum_style.html', context)

def category_view(request, branch_slug, category_slug, *args, **kwargs):
    cat = get_list_or_404(Category, slug = category_slug)[0]
    threads = Thread.objects.filter(category = cat.id)
    context = {'category':cat,
                'threads':threads}
    return render(request, 'forum/category.html', context)

def thread_view(request, branch_slug, category_slug, thread_slug, *args, **kwargs):
    thread = get_list_or_404(Thread, slug = thread_slug)
    
    context = {'thread':thread}
    return render(request, 'forum/thread.html', context)


class ThreadView(ListView):
    model = Post

    def get_queryset(self, *args, **kwargs):
        thread = Thread.objects.get(slug=self.kwargs['thread_slug'])
        qs = thread.posts.all()
        return qs

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        #Parsing slugs by the context to generate links for creating posts
        context['MEDIA_URL'] = settings.MEDIA_URL
        context['thread_slug'] = self.kwargs['thread_slug']
        context['category_slug'] = self.kwargs['category_slug']
        context['branch_slug'] = self.kwargs['branch_slug']
        context['thread_id'] = Thread.objects.get(slug=self.kwargs['thread_slug']).id
        return context


@login_required
def edit_profile_view(request, *args, **kwargs):
    form = EditProfileForm(instance = request.user.profile)
    
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance = request.user.profile)
        if form.is_valid():
            form.save()
            form = EditProfileForm(instance = request.user.profile)

    context = {'form':form,
                'MEDIA_URL':settings.MEDIA_URL}
    return render(request, 'forum/edit_profile.html', context)