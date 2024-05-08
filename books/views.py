from django.contrib import messages
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .models import Book, BookReview
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.core.paginator import Paginator
from .forms import BookReviewForm

# class BookListView(generic.ListView):
#     template_name = 'books/list.html'
#     queryset = Book.objects.all().order_by('-id')
#     context_object_name = 'books'
#     paginate_by = 2

class BookListView(View):
    def get(self, request):
        books = Book.objects.all().order_by('-id')
        search_query = request.GET.get('q', '')
        if search_query:
            books = books.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
        page_size = request.GET.get('page_size', 2)
        paginator = Paginator(books, page_size)

        page_num = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_num)

        return render(request,
                      'books/list.html',
                      {'page_obj': page_obj, 'page_size': page_size, 'search_query': search_query})


# class BookDetailView(generic.DetailView):
#     template_name = 'books/detail.html'
#     pk_url_kwarg = 'id'
#     model = Book
    # context_object_name = 'book'  # It is default value

class BookDetailView(View):
    def get(self, request, id):
        try:
            book = Book.objects.get(id=id)
        except Book.DoesNotExist:
            # raise Http404("The Book With This ID Does Not Exist!!!")
            return render(request, '404.html')

        form = BookReviewForm()
        book_reviews = book.reviews.all().order_by('-id')
        context = {
            'book': book,
            'book_reviews': book_reviews,
            'form': form,
        }

        return render(request, 'books/detail.html', context)


class AddReviewView(LoginRequiredMixin, View):
    def post(self, request, id):
        book = Book.objects.get(id=id)
        form = BookReviewForm(data=request.POST)

        if form.is_valid():
            book_review = BookReview(
                book=book,
                user=request.user,
                comment=form.cleaned_data['comment'],
                stars_given=form.cleaned_data['stars_given']
            )
            book_review.save()

            return redirect(reverse('books:detail', kwargs={'id': book.id}))

        return render(request, 'books/detail.html', {'book': book, 'form': form})


class EditReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.reviews.get(id=review_id)

        review_form = BookReviewForm(instance=review)
        return render(request, 'books/edit_review.html', {'book': book, 'review': review, 'form': review_form})

    def post(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.reviews.get(id=review_id)
        review_form = BookReviewForm(instance=review, data=request.POST)

        if review_form.is_valid():
            review_form.save()
            return redirect(reverse('books:detail', kwargs={'id': book.id}))

        return render(request, 'books/edit_review.html', {'book': book, 'review': review, 'form': review_form})

class ConfirmDeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = BookReview.objects.get(id=review_id)

        return render(request, 'books/confirm_delete.html', {'book': book, 'review': review})

class DeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = BookReview.objects.get(id=review_id)

        review.delete()

        messages.success(request, 'You have successfully deleted this review.')

        return redirect(reverse('books:detail', kwargs={'id': book.id}))
