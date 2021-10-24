from django.urls import path

from .views import (forum_style_view, main_page_view, manage_groups_view, 
remove_group_view, update_group_view, user_list_view,
create_branch_view, create_category_view, forum_style_view,
)

app_name = 'forum'

urlpatterns = [
    path('', main_page_view, name='main_page'),
    path('manage_groups/', manage_groups_view, name='manage_groups'),
    path('remove_group/<slug:group>', remove_group_view, name='remove_group'),
    path('update_group/<slug:group>', update_group_view, name='update_group'),
    path('user_list', user_list_view, name='user_list'),
    path('create_branch', create_branch_view, name='create_branch'),
    path('create_category', create_category_view, name='create_category'),
    path('forum_style', forum_style_view, name='forum_style'),

]