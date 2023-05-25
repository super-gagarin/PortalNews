import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.conf import settings


# Create your models here.
class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default = 0)

    def update_rating(self):
        postrat = self.Post_set.aggregate(postrat=Sum('postrating'))
        prat = 0
        prat += postrat.get('postrat')
        comrat = self.author.comment_set.aggregate(commentrat=Sum('comrating'))
        crat = 0
        crat += comrat.get('commentrat')
        self.rating = prat * 3 + crat
        self.save()

class Category(models.Model):
     category = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    postauthor = models.ForeignKey(Author, on_delete = models.CASCADE)
    postnewstype = models.CharField(max_length=8, choices = [('article', 'статья'), ('news', 'новость')], default = 'news')
    postdatecreate = models.DateTimeField(auto_now_add=True)
    postcat = models.ManyToManyField(Category, through='PostCategory')
    posttitle = models.CharField(max_length=124)
    posttext = models.TextField()
    postrating = models.IntegerField(default=0)

    def like(self):
        self.postrating += 1
        self.save()

    def dislike(self):
        self.postrating -= 1
        self.save()

    def preview(self):
        return '{0}{1}'.format(self.posttext[:123], '...') if len(self.posttext) > 124 else self.posttext


class PostCategory(models.Model):
    postthrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categorythrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    compost = models.ForeignKey(Post, on_delete=models.CASCADE)
    comuser = models.ForeignKey(User, on_delete=models.CASCADE)
    comtext = models.TextField()
    comdatecreate = models.DateTimeField(auto_now_add=True)
    comrating = models.SmallIntegerField(default=0)

    def like(self):
        self.comrating += 1
        self.save()

    def dislike(self):
        self.comrating -= 1
        self.save()
