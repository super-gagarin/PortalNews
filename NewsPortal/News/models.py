from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.validators import MinValueValidator
from django.urls import reverse


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default = 0)

    def update_rating(self):
        postrat = self.post_set.aggregate(postrat=Sum('postrating'))
        prat = 0
        prat += postrat.get('postrat')
        comrat = self.author.comment_set.aggregate(commentrat=Sum('comrating'))
        crat = 0
        crat += comrat.get('commentrat')
        self.rating = prat * 3 + crat
        self.save()

    def __repr__(self):
        return f"Author (author.name='{self.author}', rating='{self.rating}')"

    def __str__(self):
        return f'{self.author.username.title()}: рейтинг {str(self.rating)}'

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

class Category(models.Model):
    category = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f'{self.category.title()}'

    def __repr__(self):
        return f"Category (name='{self.category}')"

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Post(models.Model):
    NEWS = 'news'
    ARTICLE = 'article'
    CATEGORY_CHOISES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    postauthor = models.ForeignKey(Author, on_delete=models.CASCADE)
    postnewstype = models.CharField(max_length=8, choices=CATEGORY_CHOISES, default=NEWS)
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

    def preview(self, pre_len=20):
        return '{0}{1}'.format(self.posttext[:pre_len], '...') if len(self.posttext) > pre_len else self.posttext

    def categorys(self):
        return ', '.join([x.category for x in self.postcat.all()])

    def get_absolute_url(self):
        """ Вернуть url, зарегистрированный для отображения одной статьи """
        return reverse('post_detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.posttitle.title()}: {self.posttext[:20]}'

    def __repr__(self):
        return f"Post (postauthor.author.name='{self.postauthor.author}', " \
               f"posttitle='{self.posttitle}', postrating='{self.postrating}'," \
               f"postnewstype='{self.postnewstype}')"

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

class PostCategory(models.Model):
    postthrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categorythrough = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.categorythrough.category}: {self.postthrough.posttitle.title()}'


    class Meta:
        verbose_name = 'Катеогория сообщения'
        verbose_name_plural = 'Катеогория сообщений'



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

    def __str__(self):
        return f'{self.comuser.username}: {self.comtext[:20]}'


    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'