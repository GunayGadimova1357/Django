from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import MovieForm
from .models import Movie


def login_view(request):
    if request.user.is_authenticated:
        return redirect('movie_list')

    next_url = request.GET.get('next') or request.POST.get('next') or '/'
    context = {'next': next_url}

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        context['username'] = username

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(next_url)

        context['error'] = 'Invalid username or password.'

    return render(request, 'registration/login.html', context)


def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return render(request, 'registration/logged_out.html')


@login_required
def movie_list(request):
    status = request.GET.get('status', '')
    genre = request.GET.get('genre', '')

    movies = Movie.objects.filter(user=request.user)
    if status:
        movies = movies.filter(status=status)
    if genre:
        movies = movies.filter(genre=genre)

    genres = (
        Movie.objects
        .filter(user=request.user)
        .order_by('genre')
        .values_list('genre', flat=True)
        .distinct()
    )

    context = {
        'movies': movies,
        'status_choices': Movie.STATUS_CHOICES,
        'genres': genres,
        'selected_status': status,
        'selected_genre': genre,
    }
    return render(request, 'watchlist/movie_list.html', context)


@login_required
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.user = request.user
            movie.save()
            return redirect('movie_list')
    else:
        form = MovieForm()

    return render(request, 'watchlist/movie_form.html', {
        'form': form,
        'title': 'Add movie',
        'button_text': 'Add',
    })


@login_required
def edit_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk, user=request.user)

    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movie_list')
    else:
        form = MovieForm(instance=movie)

    return render(request, 'watchlist/movie_form.html', {
        'form': form,
        'title': 'Edit movie',
        'button_text': 'Save',
    })


@login_required
def delete_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk, user=request.user)

    if request.method == 'POST':
        movie.delete()
        return redirect('movie_list')

    return render(request, 'watchlist/movie_confirm_delete.html', {'movie': movie})
