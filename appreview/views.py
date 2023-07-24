from itertools import chain

from authentication.models import User
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from . import forms, models
from .forms import ReviewForm, TicketForm, PhotoForm, UserSearchForm
from .models import Review, Ticket, UserFollows


@login_required
def photo_upload(request):
    form = forms.PhotoForm()
    if request.method == 'POST':
        form = forms.PhotoForm(request.POST, request.FILES)
        photo = form.save(commit=False)
        photo.uploader = request.user
        photo.save()
        return redirect('login')
    return render(request, 'appreview/photo_upload.html', context={'form': form})


@login_required
def home(request):
    photos = models.Photo.objects.all()
    tickets = models.Ticket.objects.all()
    followed_users = UserFollows.objects.filter(user=request.user).values_list('followed_user', flat=True)
    print(followed_users)
    followed_users_tickets = Ticket.objects.filter(author__in=followed_users)
    discover_tickets = tickets.exclude(author__in=followed_users)
    followed_tickets = followed_users_tickets.order_by('-created_on')
    discover_tickets = discover_tickets.order_by('-created_on')
    return render(request, 'appreview/home.html', context={'photos': photos, 'followed_tickets': followed_tickets,
                                                           'discover_tickets': discover_tickets})


@login_required
def ticket_and_photo_upload(request):
    ticket_form = forms.TicketForm()
    photo_form = forms.PhotoForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST)
        photo_form = forms.PhotoForm(request.POST, request.FILES)
        if all([ticket_form.is_valid(), photo_form.is_valid()]):
            photo = photo_form.save(commit=False)
            photo.uploader = request.user
            photo.save()
            ticket = ticket_form.save(commit=False)
            ticket.author = request.user
            ticket.photo = photo
            ticket.save()
            return redirect('appreview:home')
    context = {
        'ticket_form': ticket_form,
        'photo_form': photo_form,
    }
    return render(request, 'appreview/create_ticket.html', context=context)


def create_ticket_and_review(request):
    photo_form = forms.PhotoForm()
    ticket_form = forms.TicketForm()
    comment_form = forms.ReviewForm()

    if request.method == 'POST':
        photo_form = forms.PhotoForm(request.POST, request.FILES)
        ticket_form = forms.TicketForm(request.POST)
        comment_form = forms.ReviewForm(request.POST)

        if all([ticket_form.is_valid(), comment_form.is_valid(), photo_form.is_valid()]):
            photo = photo_form.save(commit=False)
            photo.uploader = request.user
            photo.save()

            ticket = ticket_form.save(commit=False)
            ticket.author = request.user
            ticket.save()

            comment = comment_form.save(commit=False)
            comment.ticket = ticket
            comment.user = request.user
            comment.save()

            return redirect('appreview:home')

    context = {
        'photo_form': photo_form,
        'ticket_form': ticket_form,
        'comment_form': comment_form,
    }
    return render(request, 'appreview/create_ticket_and_review.html', context=context)


@login_required
def view_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    reviews = Review.objects.filter(ticket=ticket)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()

    else:
        form = ReviewForm()

    context = {
        'ticket': ticket,
        'reviews': reviews,
        'form': form,
    }

    return render(request, 'appreview/view_ticket.html', context)


@login_required
def ticket_review(request, slug):
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.rating = request.POST.get('rating')
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})


@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    # Vérifier si l'utilisateur est l'auteur du ticket
    if ticket.author == request.user:
        ticket.delete()
        return redirect('appreview:my_posts')  # Remplacez 'nom_de_la_vue' par le nom de votre vue
    else:
        # Gérer le cas où l'utilisateur n'est pas autorisé à supprimer le ticket
        return HttpResponseForbidden("Vous n'êtes pas autorisé à supprimer ce ticket.")


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    # Vérifier si l'utilisateur est l'auteur de la critique
    if review.user == request.user:
        review.delete()
        return redirect('appreview:my_posts')  # Remplacez 'nom_de_la_vue' par le nom de votre vue
    else:
        # Gérer le cas où l'utilisateur n'est pas autorisé à supprimer la critique
        return HttpResponseForbidden("Vous n'êtes pas autorisé à supprimer cette critique.")


@login_required
def my_posts(request):
    tickets = Ticket.objects.filter(author=request.user)
    reviews = Review.objects.filter(user=request.user)
    tickets_and_reviews = sorted(chain(tickets, reviews), key=lambda instance:
    instance.created_on, reverse=True)

    context = {
        "tickets": tickets,
        "reviews": reviews,
        "tickets_and_reviews": tickets_and_reviews,
    }
    return render(request, "appreview/my_posts.html", context=context)


@login_required
def update_post(request, post_type, post_id):
    if post_type == "ticket":
        post = get_object_or_404(Ticket, id=post_id)
        form = TicketForm(instance=post)
        photo_form = PhotoForm(instance=post.photo)
    elif post_type == "review":
        post = get_object_or_404(Review, id=post_id)
        form = ReviewForm(instance=post)
        photo_form = None

    if request.method == 'POST':
        if post_type == "ticket":
            form = TicketForm(request.POST, instance=post)
            photo_form = PhotoForm(request.POST, request.FILES, instance=post.photo)
        elif post_type == "review":
            form = ReviewForm(request.POST, instance=post)

        if form.is_valid() and (photo_form is None or photo_form.is_valid()):
            post = form.save(commit=False)
            if post_type == "ticket":
                if photo_form:
                    photo = photo_form.save(commit=False)
                    photo.uploader = request.user
                    photo.save()
                    post.photo = photo
            post.save()
            return redirect('appreview:my_posts')

    context = {
        'form': form,
        'photo_form': photo_form,
    }
    return render(request, 'appreview/update_post.html', context=context)


from django.contrib.auth.decorators import login_required


@login_required
def followers(request):
    form = UserSearchForm()

    if request.method == 'POST':
        form = UserSearchForm(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data['search_query']
            User = get_user_model()
            users = User.objects.filter(username__icontains=search_query)
            return render(request, 'appreview/user_search_results.html', {'users': users})

    users_following = UserFollows.objects.filter(user=request.user)
    users_followed_by = UserFollows.objects.filter(followed_user=request.user)

    context = {
        "form": form,
        "users_following": users_following,
        "users_followed_by": users_followed_by,
    }

    return render(request, "appreview/followers.html", context=context)


@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        try:
            user_follows = UserFollows.objects.create(user=request.user, followed_user=user_to_follow)
            messages.success(request, f"Vous suivez maintenant {user_to_follow.username}.")
            return redirect(reverse('appreview:followers'))
        except IntegrityError:
            # Gérer l'erreur de contrainte unique
            messages.error(request, "Vous suivez déjà cet utilisateur.")
            return redirect(reverse('appreview:followers'))

    return render(request, 'appreview/follow_user.html', context={'user_to_follow': user_to_follow})


@login_required
def unfollow(request, user_id):
    user = get_object_or_404(UserFollows, id=user_id)
    if request.method == "POST":
        user.delete()
        return redirect("appreview:followers")
    context = {
        "user": user,
    }
    return render(request, "appreview/unfollow.html", context=context)
