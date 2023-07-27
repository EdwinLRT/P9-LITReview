from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from appreview import views as appreview_views

app_name = "appreview"
urlpatterns = [
    path("", appreview_views.home, name="home"),

    path("tickets/my_posts/", appreview_views.my_posts, name="my_posts"),
    path('ticket/create/',appreview_views.ticket_and_photo_upload, name='create_ticket'),
    path('ticket/<int:ticket_id>/add', appreview_views.ticket_review, name='ticket_review'),
    path('ticket/<int:ticket_id>/', appreview_views.view_ticket, name='view_ticket'),
    path('update_post/<str:post_type>/<int:post_id>/', appreview_views.update_post, name='update_post'),
    path('ticket/<int:ticket_id>/delete/', appreview_views.delete_ticket, name="delete_ticket"),
    path('ticket/create_and_review/', appreview_views.create_ticket_and_review, name='create_ticket_and_review'),
    path('review/<int:review_id>/delete/', appreview_views.delete_review, name='delete_review'),
    path('followers/search/', appreview_views.followers, name='user_search'),
    path('follow_user/<int:user_id>/', appreview_views.follow_user, name='follow_user'),
    path('followers/', appreview_views.followers, name='followers'),
    path('followers/<int:user_id>/unfollow', appreview_views.unfollow, name='unfollow'),

]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
