from django.core.paginator import Paginator
from django.shortcuts import render
from books.models import BookReview

def landing_page(request):
    # print(request.COOKIES['sessionid'], request.user.is_authenticated, request.path)
    return render(request, 'landing_page.html')

def home_page(request):
    book_reviews = BookReview.objects.all().order_by('-created_at')
    page_size = request.GET.get('page_size', 5)
    page_num = request.GET.get('page', 1)

    paginator = Paginator(book_reviews, page_size)
    page_obj = paginator.get_page(page_num)

    return render(request, 'home_page.html', {'page_obj': page_obj, 'page_size': page_size})