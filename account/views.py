from django.contrib.auth import login as auth_login
from django.shortcuts import render,get_object_or_404,redirect
from .forms import SignUpForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView,ListView
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from boards.models import Board,Topic,Post

def signup(request):
     if request.method=='POST':
         form=SignUpForm(request.POST)
         if form.is_valid():
               user=form.save()
               auth_login(request,user)
               return redirect('home')
     else:
         form=SignUpForm() 
     return render(request,'signup.html',{'form':form})

@method_decorator(login_required,name='dispatch')     
class UserUpdateView(UpdateView):
     model = User
     fields = ('first_name','last_name','email',)
     template_name='my_account.html'
     success_url=reverse_lazy('my_details')
     
     def form_valid(self,form):
          user=form.save()
          user.save()
          return redirect('my_details', user_name=user.username)   
     
     def get_object(self):
          return self.request.user
          
class my_details(ListView):
     template_name='my_details.html'
     context_object_name='posts'
     model = Post
     ordering = ['-created_at']
     paginate_by=20
     
     def get_queryset(self):
          queryset = super().get_queryset()
          return queryset.filter(created_by__username=self.kwargs['user_name'])
 
    
     
     def get_context_data(self,**kwargs):
          user1=get_object_or_404(User,username=self.kwargs.get('user_name'))
          kwargs['user1']=user1
          return super().get_context_data(**kwargs)
     

                   
