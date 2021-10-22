from django.shortcuts import render


def main_page_view(request):
    context = {}
    return render(request, 'forum/main_page.html', context)