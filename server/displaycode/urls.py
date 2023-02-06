# howdy/urls.py
#from django.urls import path

from django.conf import settings
from django.conf.urls import url, include
from django.urls import path
from displaycode import views
from rest_framework import routers
from rest_framework.routers import SimpleRouter
from django.conf.urls.static import static
from django.urls import path

#http://polyglot.ninja/django-rest-framework-viewset-modelviewset-router/

#router = SimpleRouter(trailing_slash=False)
router = SimpleRouter()
#If you add SearchViewSet after SnippetViewSet, tests will break because both use SnippetSerializer.
router.register(r'search', views.SearchViewSet) 
router.register(r'snippets', views.SnippetViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'waitlistusers', views.WaitListUserViewSet)

#https://joel-hanson.medium.com/drf-how-to-make-a-simple-file-upload-api-using-viewsets-1b1e65ed65ca
router.register(r'upload', views.UploadViewSet, basename="upload")
#Actually, fetchdata endpoint should be  fetchurl endpoint.
#But for perceived safety reasons, I will not do that.
router.register(r'fetchdata', views.FetchDataViewSet, basename="fetchdata")
#We don't have much stuff. So, just return something random.
router.register(r'randompic', views.RandomPicViewSet, basename="randompic")
router.register(r'listpics', views.ListPicsViewSet, basename="listpics")
#Fetch a specific pic from /dispaycode/pic/<picId>
router.register(r'pic', views.PicDetailViewSet, basename="pic")
#router.register(r'pic', views.RaghuViewSet, basename="pic")


router.register(r'camera', views.CameraViewSet)
router.register(r'snapshotdetails', views.SnapshotDetailsViewSet)

urlpatterns = router.urls;

urlpatterns = [
#    #url(r'^$', views.HomePageView.as_view()),
    url(r'^$', views.loadSnippet, name='loadFirstSnippet'),
#    #url(r'^snippet(?P<snippetId>\d+)$', views.loadSnippet, name='loadSnippet'),
#    url(r'^allsnippets$', views.SnippetListView.as_view(), name="allsnippets"),
#    #instead of a seperate submit comment  url, we just post to same page and 
#    #hope that it works!
#    #url(r'^submitComment$', views.submitComment, name='urlname'),
    url(r'^addSnippet$', views.addSnippet, name='addSnippet'),
    path('accounts/', include('django.contrib.auth.urls')), # new
    url(r"^api/v1/", include("djoser.urls.base")),
    url(r'^api/v1/', include('djoser.urls')),
    url(r"^api/v1/", include("djoser.urls.authtoken")),
    #url(r"^api/v1/", include("djoser.urls.jwt")),
    #url(r"^api/v1/", include("djoser.social.urls")),

    #url(r'^login$', views.addSnippet, name='login'),
    #url(r'^logout$', views.addSnippet, name='logout'),
#
#    #Coming from Rest tutorial https://www.django-rest-framework.org/tutorial/quickstart/
#    #Get all snippets in one shot.
#    #url(r'^snippets$', views.SnippetViewSet.as_view({'get': 'list'}), name='allsnippetsrestapi'),
#url(r'^snippets/(?P<snippetId>\d+)$', views.SnippetViewSet.as_view({'get': 'list'}), name='getsnippetrestapi'),
    path('', include(router.urls)),
    # url('', views.homepageview, name='home')
#    include(router.urls),
#    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


print (urlpatterns)
