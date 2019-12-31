from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator
from markdown import markdown
import math
from django.utils.html import mark_safe
from simplemde.fields import SimpleMDEField

class Board(models.Model):
     name=models.CharField(max_length=30, unique=True)
     description=models.CharField(max_length=100)
     def __str__(self):
         return self.name
     
     def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

     def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()    
     
class Topic(models.Model):
     subject=models.CharField(max_length=255)
     last_update=models.DateTimeField(auto_now_add=True)
     board=models.ForeignKey(Board,related_name='topics', on_delete=models.PROTECT)
     starter=models.ForeignKey(User, related_name='topics', on_delete=models.PROTECT)
     views=models.PositiveIntegerField(default=0)
     def __str__(self):
         return self.subject
         
     def get_page_count(self):
        count = self.posts.count()
        pages = count / 4
        return math.ceil(pages)

     def has_many_pages(self, count=None):
        if count is None:
            count = self.get_page_count()
        return count > 6

     def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1, 5)
        return range(1, count + 1)    
     
     

     def get_last_ten_posts(self):
        return self.posts.order_by('-created_at')[:10]
class Post(models.Model):
     message=models.TextField(max_length=4000)
     topic=models.ForeignKey(Topic, related_name='posts', on_delete=models.PROTECT)
     created_at=models.DateTimeField(auto_now_add=True)
     updated_at=models.DateTimeField(null=True)
     created_by=models.ForeignKey(User,related_name='posts', on_delete=models.PROTECT)
     updated_by=models.ForeignKey(User,null=True,related_name='+', on_delete=models.PROTECT)
     page=models.PositiveIntegerField(default=1)
     
     def get_page_number(self):
        count = self.topic.posts.count()
        page=count/4
        return math.ceil(page)    
     
     def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)
     
     def get_message_as_markdown(self):
        return mark_safe(markdown(self.message,safe_mode='escape'))   
        

class Entry(models.Model):
     title = models.CharField(max_length=4000, verbose_name=u'Title')
     content = SimpleMDEField(verbose_name=u'mardown content')        
