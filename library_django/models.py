from django.db import models
from django.contrib.auth.models import User

class Genres(models.Model):
    name = models.CharField(max_length=256)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

class Books(models.Model):
    name = models.CharField(max_length=255)
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE)
    image = models.ImageField(blank=False)
    pages_number = models.IntegerField()
    quantity = models.IntegerField()
    in_stock = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

class LoanedBooks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    returned = models.BooleanField(default=False)
    
    def __str__(self):
        return self.book.name
    
    class Meta:
        verbose_name = 'LoanedBook'
        verbose_name_plural = 'LoanedBooks'