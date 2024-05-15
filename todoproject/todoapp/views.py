from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from todoapp.forms import ToDoForm
from todoapp.models import Task
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView,DeleteView

class Tasklistview(ListView):
    model = Task
    template_name = 'home.html'
    context_object_name = 'task1'

class TaskDetailview(DetailView):
    model = Task
    template_name = 'detail.html'
    context_object_name = 'task'

class TaskUpdateview(UpdateView):
    model = Task
    template_name = 'update.html'
    context_object_name = 'task'
    fields = ('name','priority','date')

    def get_success_url(self):
        return reverse_lazy('cbvdetail',kwargs={'pk':self.object.id})

class TaskDeleteview(DeleteView):
    model = Task
    template_name = 'delete.html'
    success_url = reverse_lazy('cbvhome')
# Create your views here.
def add(request):
    task1 = Task.objects.all()
    if request.method=='POST':
        Name = request.POST.get('task', '')
        Priority = request.POST.get('priority', '')
        Date=request.POST.get('date','')
        task = Task(name=Name, priority=Priority,date=Date)
        task.save()

    return render(request,'home.html',{'task1':task1})

####def details(request):
    #return render(request,'detail.html')

def delete(request,taskid):

    if request.method=='POST':
        task = Task.objects.get(id=taskid)
        task.delete()
        return redirect('/')
    return render (request,'delete.html')

def update(request,id):
    task=Task.objects.get(id=id)
    f=ToDoForm(request.POST or None, instance=task)
    if f.is_valid():
        f.save()
        return redirect('/')
    return render(request,'edit.html',{'f':f,'task':task})