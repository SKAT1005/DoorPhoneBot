from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse

import buttons
from const import bot
from review import review
from .models import Order, User


def login_view(request):
    if request.user.is_authenticated:
        return redirect('orders_page')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('orders_page')
        else:
            # Если логин или пароль неверные
            messages.error(request, 'Неверный логин или пароль.')

    return render(request, 'login.html')


@login_required
def main(request):
    # Получаем все заказы
    orders = Order.objects.select_related('user').all().order_by('-id')

    # Получаем параметры фильтрации из GET-запроса
    type_filter = request.GET.get('type', 'all')
    client_filter = request.GET.get('client', 'all')
    status_filter = request.GET.get('status', 'all')
    has_review_filter = request.GET.get('has_review', 'all')

    # Применяем фильтры
    if type_filter != 'all':
        orders = orders.filter(type=type_filter)

    if client_filter == 'new':
        orders = orders.filter(is_new=True)
    elif client_filter == 'regular':
        orders = orders.filter(is_new=False)

    if status_filter == 'complete':
        orders = orders.filter(is_complete=True)
    elif status_filter == 'incomplete':
        orders = orders.filter(is_complete=False)

    # Фильтр по наличию отзыва
    if has_review_filter == 'with_review':
        orders = orders.exclude(review__isnull=True).exclude(review='')
    elif has_review_filter == 'without_review':
        orders = orders.filter(review__isnull=True) | orders.filter(review='')

    # Получаем статистику
    total_orders = Order.objects.count()
    new_clients = Order.objects.filter(is_new=True).count()

    # Подсчитываем предстоящие визиты (начиная с текущего момента)
    upcoming_visits = Order.objects.filter(
        visit_date__gte=timezone.now(),
        is_complete=False
    ).count()

    # Подсчитываем заказы с отзывами
    orders_with_reviews = Order.objects.exclude(review__isnull=True).exclude(review='').count()

    # Получаем уникальные типы заказов для фильтра
    order_types = Order.objects.values_list('type', flat=True).distinct()

    context = {
        'orders': orders.order_by('is_complete'),
        'total_orders': total_orders,
        'new_clients': new_clients,
        'upcoming_visits': upcoming_visits,
        'orders_with_reviews': orders_with_reviews,
        'order_types': order_types,
        'current_type_filter': type_filter,
        'current_client_filter': client_filter,
        'current_status_filter': status_filter,
        'current_has_review_filter': has_review_filter,
    }

    return render(request, 'main.html', context)


@login_required
def set_visit_date(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        visit_date = request.POST.get('visit_date')

        if visit_date:
            order.visit_date = visit_date
            order.save()
            text = f'Вам назначен мастер на {order.visit_date.replace("T", " ")}.\n\n' \
                   f'Если вам не удобно в это время, обратитесь в тех.поддержку, назовите им Идентификатор заказа: {order.id} или ваш номер телефона'
            bot.send_message(chat_id=order.user.chat_id, text=text, reply_markup=buttons.back())
            messages.success(request, 'Дата визита успешно установлена!')
        else:
            messages.error(request, 'Пожалуйста, выберите дату и время')

    # Возвращаемся на страницу заказов с текущими фильтрами
    return_url = reverse('orders_page')
    query_params = request.GET.urlencode()
    if query_params:
        return_url += f'?{query_params}'

    return redirect(return_url)


@login_required
def confirm_meeting(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        order.is_complete = True
        order.complete_date = timezone.now().date()
        order.save()
        messages.success(request, 'Встреча подтверждена! Заказ отмечен как выполненный.')
        review(order=order, user=order.user)

    # Возвращаемся на страницу заказов с текущими фильтрами
    return_url = reverse('orders_page')
    query_params = request.GET.urlencode()
    if query_params:
        return_url += f'?{query_params}'

    return redirect(return_url)


@login_required
def view_review(request, order_id):
    """Просмотр отзыва и оценки заказа"""
    order = get_object_or_404(Order, id=order_id)

    context = {
        'order': order,
    }

    return render(request, 'view_review.html', context)