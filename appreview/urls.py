from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

import appreview.views
app_name = "appreview"
urlpatterns = [
    path("", appreview.views.home, name="home"),
    path('ticket/<int:ticket_id>/', appreview.views.view_ticket, name='view_ticket'),
    path('ticket/create/', appreview.views.ticket_and_photo_upload, name='create_ticket'),
    path('ticket/<int:ticket_id>/add', appreview.views.ticket_review, name='ticket_review'),
    path("my_posts/", appreview.views.my_posts, name="my_posts"),

#    path("ticket/add/", appreview.views.create_ticket, name="create_ticket"),
    path('update_post/<str:post_type>/<int:post_id>/', appreview.views.update_post, name='update_post'),
    path("ticket/<int:ticket_id>/delete/", appreview.views.delete_ticket, name="delete_ticket"),

#   path("review/add/", appreview.views.create_review, name="create_review"),
#    path("review/<int:ticket_id>/add/",
#         appreview.views.create_review_existing_ticket, name="create_review_ticket"),
    path('review/<int:review_id>/delete/', appreview.views.delete_review, name='delete_review'),

    path('user/search/', appreview.views.user_search, name='user_search'),
    path('follow_user/<int:user_id>/', appreview.views.follow_user, name='follow_user'),
    path('followers/', appreview.views.followers, name='followers'),
    path('followers/<int:user_id>/unfollow', appreview.views.unfollow, name='unfollow'),

]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)