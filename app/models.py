from django.db import models


class User(models.Model):
    name = models.CharField(max_length=128, verbose_name='Имя клииента')
    chat_id = models.CharField(max_length=64, verbose_name='ID пользователя')
    phone = models.CharField(max_length=16, verbose_name='Номер телефона')
    address = models.CharField(max_length=256, verbose_name='Адрес')


class Order(models.Model):
    type = models.CharField(max_length=64, verbose_name='Тип заказа')
    user = models.ForeignKey('User', related_name='orders', on_delete=models.CASCADE, verbose_name='Пользователь')
    is_new = models.BooleanField(default=False, verbose_name='Новый ли клиент')
    text = models.TextField(verbose_name='Текст обращения')
    name = models.CharField(max_length=64, verbose_name='Имя клиента')
    visit_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата визита мастера')
    is_complete = models.BooleanField(default=False, verbose_name='Выполнен ли заказ')
    review = models.TextField(blank=True, null=True, verbose_name='Отзыв')
    rating = models.IntegerField(blank=True, null=True, verbose_name='Оценка',
                                 choices=[(i, str(i)) for i in range(1, 6)])
    complete_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Заказ #{self.id} - {self.name}"