from django.db import models
from django.urls import reverse
from account.models import CustomUser


class Ticket(models.Model):
    order_information = 'Информация по заказу'
    commercial_offer = 'Коммерческое предложение'
    product_consultation = 'Консультация по товару'
    discount_cards = 'Дисконтные карты'
    exchange_and_return_of_goods = 'Обмен и возврат товара'
    marriage_and_warranty_issues = 'Вопросы по браку и гарантии'
    company_review = 'Отзыв о компании'
    cooperation_offer = 'Предложение сотрудничества'
    work_in = 'Работа в ноябре'
    website_error = 'Ошибка на сайте'
    call_back = 'Перезвонить'

    subject_list = [
        (order_information, 'Информация по заказу'),
        (commercial_offer, 'Коммерческое предложение'),
        (product_consultation, 'Консультация по товару'),
        (discount_cards, 'Дисконтные карты'),
        (exchange_and_return_of_goods, 'Обмен и возврат товара'),
        (marriage_and_warranty_issues, 'Вопросы по браку и гарантии'),
        (company_review, 'Отзыв о компании'),
        (cooperation_offer, 'Предложение сотрудничества'),
        (work_in, 'Работа в ноябре'),
        (website_error, 'Ошибка на сайте'),
        (call_back, 'Перезвонить')

    ]
    ticket_is_open = 'Обращение открыто'
    ticket_is_closed = 'Обращение закрыто'
    ticker_status = [
        (ticket_is_open, 'Обращение открыто'),
        (ticket_is_closed, 'Обращение закрыто')
    ]
    customer_response = 'green'
    technical_support_response = 'red'
    closed = 'grey'
    indicator_status = [
        (customer_response, 'green'),
        (technical_support_response, 'red'),
        (closed, 'grey')
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Покупатель',
                             related_name='user_ticket')
    order_number = models.PositiveIntegerField(verbose_name='Номер заказа')
    subject = models.CharField(max_length=256, verbose_name='Тема обращения', choices=subject_list)
    text = models.TextField(verbose_name='Текст обращения')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    status = models.CharField(max_length=256, verbose_name='Статус обращения', choices=ticker_status,
                              default=ticket_is_open)
    indicator = models.CharField(max_length=256, verbose_name='Индикатор обращения', choices=indicator_status,
                                 default=customer_response)

    class Meta:
        verbose_name = 'Обращение'
        verbose_name_plural = 'Обращения'

    def number_of_messages(self):
        return self.ticket_msg.count()

    def __str__(self):
        return f'Обращение #{self.id}'

    def get_absolute_url(self):
        return reverse('account:ticket_detail', kwargs={'id': self.id})


class TicketMessage(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, verbose_name='Сообщение в обращении',
                               related_name='ticket_msg')
    msg = models.TextField(verbose_name='Сообщение')
    is_admin = models.BooleanField(default=False, verbose_name='Сообщение от админа')

    class Meta:
        verbose_name = 'Сообщения в обращении'
        verbose_name_plural = 'Сообщения в обращениях'

    def __str__(self):
        return self.ticket
