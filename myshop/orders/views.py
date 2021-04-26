#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------------------------
# Archivo: views.py
#
# Descripción:
#   En este archivo se definen las vistas para la app de órdenes.
#
#   A continuación se describen los métodos que se implementaron en este archivo:
#
#                                               Métodos:
#           +------------------------+--------------------------+-----------------------+
#           |         Nombre         |        Parámetros        |        Función        |
#           +------------------------+--------------------------+-----------------------+
#           |                        |                          |  - Verifica la infor- |
#           |                        |  - request: datos de     |    mación y crea la   |
#           |    order_create()      |    la solicitud.         |    orden de compra a  |
#           |                        |                          |    partir de los datos|
#           |                        |                          |    del cliente y del  |
#           |                        |                          |    carrito.           |
#           +------------------------+--------------------------+-----------------------+
#           |                        |                          |  - Crea y envía el    |
#           |        send()          |  - order_id: id del      |    correo electrónico |
#           |                        |    la orden creada.      |    para notificar la  |
#           |                        |                          |    compra.            |
#           +------------------------+--------------------------+-----------------------+
#
#--------------------------------------------------------------------------------------------------

from django.shortcuts import render,redirect
from .models import OrderItem, Order
from .forms import OrderCreateForm
from django.core.mail import send_mail
from cart.cart import Cart
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from django.conf import settings
import pytz
import time


def order_create(request):

    # Se crea el objeto Cart con la información recibida.
    cart = Cart(request)

    # Si la llamada es por método POST, es una creación de órden.
    if request.method == 'POST':

        # Se obtiene la información del formulario de la orden,
        # si la información es válida, se procede a crear la orden.
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            
            # Se limpia el carrito con ayuda del método clear()
            cart.clear()
            
            # Llamada al método para enviar el email.
            send(order.id, cart)
            return render(request, 'orders/order/created.html', { 'cart': cart, 'order': order })
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart,
                                                        'form': form})

def send(order_id, cart):
    # Se obtiene la información de la orden.
    order = Order.objects.get(id=order_id)

    # Se crea el subject del correo.
    subject = 'Order nr. {}'.format(order.id)

    # Se define el mensaje a enviar.
    message = 'Dear {},\n\nYou have successfully placed an order. The id your order is {}.\n\n\n'.format(order.first_name,order.id)
    message_part2 = 'Your order: \n\n'
    mesagges = []

    for item in cart:
        msg = str(item['quantity']) + 'x '+ item['product'].name +'  $'+ str(item['total_price'])+ '\n'
        mesagges.append(msg)
    
    message_part3 = ' '.join(mesagges)
    message_part4 = '\n\n\n Total: $'+ str(cart.get_total_price())
    body = message + message_part2 + message_part3 + message_part4

    # Se envía el correo.
    send_mail(subject, body, 'pruebas.jogglez@gmail.com', [order.email], fail_silently=False)

def order_list(request):
    orders = Order.objects.all()
    return render(request, 'orders/order/list.html', {'orders' : orders})

def cancel_order(request, id):
    order = Order.objects.get(id=id)
    flag = True
    note = "No, I am not sure"
    todays_date = datetime.now()
    timezone = pytz.timezone(settings.TIME_ZONE)
    todays_date_wo = timezone.localize(todays_date)
    takeaway_hours = todays_date_wo - timedelta(hours=24)
    
    local_time = pytz.timezone(settings.TIME_ZONE)
    order_date = order.created.replace(tzinfo=pytz.utc)
    order_date = order_date.astimezone(local_time)

    if (takeaway_hours > order_date):
        flag = False
        note = "Return to order list"
 
    return render(request, 'orders/order/delete_order_confirm.html', {'order' : order,
                                                                      'flag' : flag,
                                                                      'note' : note})
def delete_order_confirm(request, id):
    order = Order.objects.get(id=id)
    notas=['cancelled','were contained','cancellation']
    confirm(order.id,notas)
    order.delete()
    return redirect('order_list')

def order_detail(request, id):
    order = Order.objects.get(id=id)

    flag = True
    todays_date = datetime.now()
    timezone = pytz.timezone(settings.TIME_ZONE)
    todays_date_wo = timezone.localize(todays_date)
    takeaway_hours = todays_date_wo - timedelta(hours=24)
    
    local_time = pytz.timezone(settings.TIME_ZONE)
    order_date = order.created.replace(tzinfo=pytz.utc)
    order_date = order_date.astimezone(local_time)

    if (takeaway_hours > order_date):
        flag = False

    order_items = []
    order_items = OrderItem.objects.filter(order=id)
    return render(request, 'orders/order/items_list.html', {'order' : order,
                                                            'order_items' : order_items,
                                                            'flag' : flag,})



def remove_order_item(request, id):
    order_item = OrderItem.objects.get(id=id)
    order_id = str(order_item.order)
    order_id = order_id[6:len(order_id)]
    order_item.delete()
    return redirect('order_detail', id = order_id)

def remove_order_confirm(request, id):
    notas=['modified','are still','modification']
    update_confirmation(id)
    confirm(id,notas)
    return redirect('order_list')

def confirm(order_id, notas):
    # Se obtiene la información de la orden.
    order = Order.objects.get(id=order_id)

    # Se crea el subject del correo.
    subject = 'Order nr. {}'.format(order.id)

    # Se define el mensaje a enviar.
    message = 'Dear {},\n\nYou have successfully {} your order. The number of your {} order is {}.\n\n\n'.format(order.first_name,notas[0],notas[0],order.id)
    message_part2 = 'The following products {} in your order: \n\n'.format(notas[1])
    mesagges = []

    order_items = []
    order_items = OrderItem.objects.filter(order=order_id)

    for item in order_items:
        msg = str(item.quantity) + 'x '+ str(item.product.name) +'  $'+ str(item.get_cost())+ '\n'
        mesagges.append(msg)
    
    message_part3 = ' '.join(mesagges)
    message_part4 = '\n\n\n Date of '+ notas[2] +' : ' + datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    body = message + message_part2 + message_part3 + message_part4

    # Se envía el correo.
    send_mail(subject, body, 'pruebas.jogglez@gmail.com', [order.email], fail_silently=False)

def update_confirmation(order_id):
    # Se obtiene la información de la orden.
    order = Order.objects.get(id=order_id)

    # Se crea el subject del correo.
    subject = 'Order nr. {}'.format(order.id)

    # Se define el mensaje a enviar.
    message = 'Dear {},\n\nYou have successfully updated your order. The number of your updated order is {}.\n'.format(order.first_name,order.id)

    message_part2 = '\n\n Date of update : ' + datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    body = message + message_part2

    # Se envía el correo.
    send_mail(subject, body, 'pruebas.jogglez@gmail.com', [order.email], fail_silently=False)

def update_order(request,id):
    if request.method == "POST":
        ids_to_delete = request.POST.getlist('item')
        if len(ids_to_delete) > 0:
            # Parcial order items deletion
            for item_id in ids_to_delete:
                order_item = OrderItem.objects.get(id=item_id)
                order_item.delete()
                     
            update_confirmation(id)
            confirm(id,['modified','are still','modification'])
            return redirect('order_list')
        else:
            return redirect('order_detail')
    else:
        return redirect('order_detail')
