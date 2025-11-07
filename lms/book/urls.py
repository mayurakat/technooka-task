from rest_framework.routers import DefaultRouter
from .views import BookViewSet, AuthorViewSet, GenreViewSet, BorrowRequestViewSet
from django.urls import path
from .views import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register("books", BookViewSet, basename="books")
router.register("borrow", BorrowRequestViewSet, basename="borrow")

urlpatterns = router.urls

urlpatterns +=  [
    path("register/", RegisterView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("authors/", AuthorViewSet.as_view(), name="authors"),
    path("genres/", GenreViewSet.as_view(), name="genres"),


]