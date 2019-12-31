from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.views.generic import UpdateView,ListView,CreateView
from django.utils import timezone
from .models import Board,Topic,Post
from .forms import NewTopicForm,PostForm
from django.urls import resolve, reverse,reverse_lazy
import math

class BoardListView(ListView):
    model = Board
    context_object_name='boards'
    template_name='home.html'
    paginate_by=10
    
    def get_queryset(self):
         queryset = super().get_queryset()
         return queryset.order_by('name')
               

class TopicListView(ListView):
    model = Topic
    context_object_name= 'topics' 
    template_name= 'topics.html'
    paginate_by = 20
    
    def get_context_data(self,**kwargs):
         kwargs['board']=self.board
         return super().get_context_data(**kwargs)
    
    def get_queryset(self):
         self.board = get_object_or_404(Board,name=self.kwargs.get('board_name'))
         queryset = self.board.topics.order_by('-last_update').annotate(replies=Count('posts') - 1)
         return queryset     
@login_required
def new_topic(request,board_name):
    board = get_object_or_404(Board,name=board_name)
    if request.method=='POST':
           form=NewTopicForm(request.POST)
           if form.is_valid(): 
                topic=form.save(commit=False)
                topic.board=board
                topic.starter=request.user
                topic.save()

                Post.objects.create(
                     message=form.cleaned_data.get('message'),
                     topic=topic,
                     created_by=request.user
                     )
                return redirect('topic_posts',board_name=board.name,topic_pk=topic.pk)
           
    else:
           form=NewTopicForm()     
    return render(request, 'new_topics.html', {'board': board,'form':form})        
    
class PostListView(ListView):
    model = Post 
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 4
    
    def get_context_data(self,**kwargs):
        session_key = 'viewed_topic_{}'.format(self.topic.pk)  
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True  
        
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)
    def get_queryset(self):
        board=get_object_or_404(Board,name=self.kwargs.get('board_name'))
        self.topic = get_object_or_404(Topic,board=board,pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset    
  
@login_required
def reply_topic(request, board_name, topic_pk):
    board = get_object_or_404(Board,name=board_name)
    topic= get_object_or_404(Topic,board=board,pk=topic_pk)
    if request.method == 'POST':
         form = PostForm(request.POST)
         if form.is_valid():
             post = form.save(commit=False)             
             topic.last_update=timezone.now()     
             post.topic = topic             
             post.created_by = request.user
             post.save()
             
             post.page = post.get_page_number()
             post.save()
             topic.last_update=timezone.now()
             topic.save()
             
             
             topic_url = reverse('topic_posts', kwargs={'board_name': board_name, 'topic_pk': topic_pk})
             topic_post_url = '{url}?page={page}#{id}'.format(
                url=topic_url,
                id=post.pk,
                page=post.get_page_number()
             )
             return redirect(topic_post_url)
    else:
         form=PostForm()         
    return render(request,'reply_topic.html',{'topic':topic,'form':form})    
    
@method_decorator(login_required, name='dispatch')        
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_oject_name = 'post'    
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)
    
    def form_valid(self,form):
        post=form.save(commit=False)
        post.updated_by=self.request.user
        post.updated_at=timezone.now()
        post.save()
        return redirect('topic_posts', board_name=post.topic.board.name, topic_pk=post.topic.pk)        
       

