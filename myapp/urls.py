from django.conf.urls import include, url

urlpatterns = [
    url(r'', include('hello.urls', namespace='hello')),
]
