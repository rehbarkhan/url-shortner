from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import URLModelForm, URLModel
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from datetime import timedelta
# Create your views here.


class Index(View):
    def get(self, request):
        form = URLModelForm()
        return render(request, 'app/index.html', {'form':form})
    
    def post(self ,request):
        if request.htmx:
            form = URLModelForm(request.POST)
            if form.is_valid():
                data = form.save()

                form = URLModelForm()
                return render(request, 'app/success.html',{'form':form, 'url':data.short_url})
            else:
                return render(request, 'app/error.html',)
        return redirect('index')

def route(request, data):
    router = get_object_or_404(URLModel, short_url = data)
    return HttpResponseRedirect(router.url)

def delete_old_retention(request):
    if request.method == 'GET':
        return redirect('index')
    if request.method == 'POST':
        cred = request.POST.get('cred',None)
        if cred is not None:
            today_time = timezone.now()
            data = URLModel.objects.filter(
                created__gte = (today_time - timedelta(days = 7)), 
                retention = '1 Week')
            data.delete()
    return redirect('index')


