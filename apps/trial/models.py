from django.db import models

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    photo = models.URLField(blank=True)
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Post"
        ordering = ('-created_at',)  # - 表示降序

    def __str__(self):
        return self.title


class ProductCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        ProductCategory, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    # decimal_places：小數的最大位數
    price = models.DecimalField(max_digits=8, decimal_places=2)
    photo = models.URLField(blank=True)

    def __str__(self):
        return self.name


# python manage.py makemigrations
# python manage.py migrate
