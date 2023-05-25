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
        rate_post_author = self.post_set.all().aggregate(sum_postrating=Sum('postrating') * 3)['sum_postrating']
        rate_comment = self.author.comment_set.all().aggregate(sum_comrating=Sum('comrating'))['sum_comrating']
        rate_comment_post = Post.objects.filter(postauthor=self).values('postrating')
        # в ответ список querry_set , проходим циклом и складываем сумму рейтинга всех комментариев ко всем post автора.
        a = 0
        for i in range(len(rate_comment_post)):
            a = a + rate_comment_post[i]['postrating']
        self.rating = rate_post_author + rate_comment + a
        self.save()
        # postrat = self.Post_set.aggregate(postrating=Sum('rating'))
        # prat = 0
        # prat += postRat.get('postrating')
        #
        # commentrat = self.Comment_set.aggregate(commentrating=Sum('rating'))
        # crat = 0
        # crat += commentRat.get('commentrating')
        #
        # self.ratingAuthor = pRat * 3 + cRat
        # self.save()

class Category(models.Model):
    # hotnews = 'HN'
    # intresting = 'IT'
    # sport = 'SR'
    # incidents = 'IN'
    # politics = 'PT'
    # society = 'ST'
    # economy = 'EC'
    # cosmos = 'CM'
    #
    # POS_CAT = [
    #     (hotnews, 'Сейчас в СМИ'),
    #     (intresting, 'Интересное'),
    #     (sport, 'Спорт'),
    #     (incidents, 'Проишествия'),
    #     (politics, 'Политика'),
    #     (society, 'Общество'),
    #     (economy, 'Экономика'),
    #     (cosmos, 'Космонавтика')
    # ]
    # сategory = models.CharField(choices = POS_CAT, default = hotnews, unique = True)
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
        return self.posttext[:123] + '...' if len(self.posttext) > 124 else self.posttext


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