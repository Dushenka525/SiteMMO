from django.shortcuts import render
from .models import *
from .forms import *
# Create your views here.
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView,  DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail
from .filters import PostFilter


class PostsList(ListView):
    model = Post
    ordering = 'date_time'
    template_name = 'forums/posts.html'
    context_object_name = 'posts'
    paginate_by = 2
    # filterset_class = PostFilter
    def get_queryset(self):
       # Получаем обычный запрос
       queryset = super().get_queryset()
       # Используем наш класс фильтрации.
       # self.request.GET содержит объект QueryDict, который мы рассматривали
       # в этом юните ранее.
       # Сохраняем нашу фильтрацию в объекте класса,
       # чтобы потом добавить в контекст и использовать в шаблоне.
       self.filterset = PostFilter(self.request.GET, queryset)
       # Возвращаем из функции отфильтрованный список товаров
       return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        if self.request.user.is_authenticated:
            # Список ID категорий, на которые подписан текущий пользователь
            context['subscribed_category_ids'] = list(
                Subscription.objects.filter(user=self.request.user).values_list('category_id', flat=True)
            )
        else:
            context['subscribed_category_ids'] = []
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'forums/post.html'
    context_object_name = 'post'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Все комментарии к этому посту (новые сверху)
        context['comments'] = self.object.comment_set.all().order_by('-created_at')
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            if not request.user.is_authenticated:
                return redirect('login')  # или выведите сообщение
            # Создаём автора, если его ещё нет (связь с текущим пользователем)
            author, _ = Author.objects.get_or_create(user=request.user)
            comment = form.save(commit=False)
            comment.author = author
            comment.post = self.object
            comment.save()


        # --- Отправка писем ---
            # Письмо автору комментария (подтверждение)
            if comment.author.user.email:
                send_mail(
                    subject='Вы оставили комментарий на нашем сайте',
                    message=f'Здравствуйте, {comment.author.user.username}!\n\n'
                            f'Вы оставили комментарий к посту "{comment.post.heading}":\n'
                            f'{comment.text}\n\nСпасибо!',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[comment.author.user.email],
                    fail_silently=False,
                )

            # Письмо автору поста (уведомление)
            if comment.post.author.user.email:
                # Строим абсолютную ссылку на пост
                post_url = request.build_absolute_uri(comment.post.get_absolute_url())
                send_mail(
                    subject=f'Новый комментарий к вашему посту "{comment.post.heading}"',
                    message=f'Здравствуйте, {comment.post.author.user.username}!\n\n'
                            f'Пользователь {comment.author.user.username} оставил комментарий к вашему посту "{comment.post.heading}":\n'
                            f'{comment.text}\n\n'
                            f'Перейти к посту: {post_url}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[comment.post.author.user.email],
                    fail_silently=False,
                )

            return redirect('post_detail', pk=self.object.pk)
        # Если форма невалидна, показываем её с ошибками
        context = self.get_context_data()
        context['comment_form'] = form
        return self.render_to_response(context)



class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'forums/post_edit.html'
    def form_valid(self, form):
        form.instance.author = Author.objects.get(user=self.request.user)
        return super().form_valid(form)

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'forums/post_edit.html'

class PostDelete(DeleteView):
    model = Post
    template_name = 'forums/post_delete.html'
    context_object_name = 'post'



@login_required
def my_comments(request):
    # Получаем автора, связанного с текущим пользователем
    author = get_object_or_404(Author, user=request.user)
    # Получаем все комментарии к постам этого автора
    comments = Comment.objects.filter(post__author=author).select_related('post', 'author__user').order_by('-created_at')
    return render(request, 'forums/my_comments.html', {'comments': comments})



from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Subscription

# @login_required
# def manage_subscriptions(request):
#     categories = Category.objects.all()
#     # Получаем ID категорий, на которые подписан пользователь
#     subscribed_ids = set(Subscription.objects.filter(user=request.user).values_list('category_id', flat=True))
    
#     if request.method == 'POST':
#         # Обработка подписки/отписки
#         category_id = request.POST.get('category_id')
#         action = request.POST.get('action')
#         category = get_object_or_404(Category, id=category_id)
#         if action == 'subscribe':
#             Subscription.objects.get_or_create(user=request.user, category=category)
#         elif action == 'unsubscribe':
#             Subscription.objects.filter(user=request.user, category=category).delete()
#         return redirect('manage_subscriptions')
    
#     return render(request, 'forums/manage_subscriptions.html', {
#         'categories': categories,
#         'subscribed_ids': subscribed_ids,
#     })

@login_required
def toggle_subscription(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        next_url = request.POST.get('next', reverse('posts'))
        category = get_object_or_404(Category, id=category_id)
        # Если подписка уже есть – удаляем, если нет – создаём
        sub, created = Subscription.objects.get_or_create(user=request.user, category=category)
        if not created:
            sub.delete()
        return redirect(next_url)
    return redirect('posts')