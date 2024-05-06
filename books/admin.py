from django.contrib import admin
from .models import Book, Author, BookAuthor, BookReview

class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'isbn', 'description')
    search_fields = ('title__icontains',)
    list_display_links = ['id']
    # list_editable = ['title']
    # list_filter = ('title',)

admin.site.register(Book, BookAdmin)
admin.site.register([Author, BookAuthor, BookReview])