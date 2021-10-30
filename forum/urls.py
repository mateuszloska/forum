from django.urls import path
from .views import (forum_style_view, main_page_view, manage_groups_view, 
remove_group_view, update_group_view, user_list_view,
create_branch_view, create_category_view, create_thread_view, create_post_view, forum_style_view,
category_view, ThreadView, edit_profile_view
)

app_name = 'forum'

urlpatterns = [
    path('', main_page_view, name='main_page'),
    path('edit_profile', edit_profile_view, name='edit_profile'),
    path('manage_groups/', manage_groups_view, name='manage_groups'),
    path('remove_group/<slug:group>', remove_group_view, name='remove_group'),
    path('update_group/<slug:group>', update_group_view, name='update_group'),
    path('user_list', user_list_view, name='user_list'),
    path('create_branch', create_branch_view, name='create_branch'),
    path('create_category/<slug:branch_slug>', create_category_view, name='create_category'),
    path('create_thread/<slug:branch_slug>/<slug:category_slug>', create_thread_view, name='create_thread'),
    path('create_post/<slug:branch_slug>/<slug:category_slug>/<slug:thread_slug>', create_post_view, name='create_post'),
    path('forum_style', forum_style_view, name='forum_style'),
    path('discussion/<slug:branch_slug>/<slug:category_slug>', category_view, name="category"),
    path('discussion/<slug:branch_slug>/<slug:category_slug>/<slug:thread_slug>', ThreadView.as_view(), name="thread"),
]


