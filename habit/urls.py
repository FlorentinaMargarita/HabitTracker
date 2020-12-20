from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('habit/', habit),
]


def home(request):
    return HttpResponse('Home Page')

def habit(request):
    return HttpResponse('Habit Page')