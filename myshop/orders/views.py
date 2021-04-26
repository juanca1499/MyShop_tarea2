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
#           |                        |                          |  - Extrae todas las   |
#           |                        |  - request: datos de     |    ordenes creadas    |
#           |    order_list()        |    la solicitud.         |    y las envia a      |
#           |                        |                          |    un template.       |
#           |                        |                          |                       |
#           +------------------------+--------------------------+-----------------------+
#           |                        |                          |                       |
#           |   order_detail()       |  - request: datos de     |  - Muestra los        |
#           |                        |    la solicitud.         |    detalles (items)   |
#           |                        |                          |    de la orden        |
#           |                        |  - id: id de la orden    |    especificada.      |
#           |                        |    a visualizar.         |                       |
#           |                        |                          |                       |
#           +------------------------+--------------------------+-----------------------+
#           |                        |                          |                       |
#           |                        |  - request: datos de     |  - Extrae el elemento |
#           |                        |    la solicitud.         |    order que se desea |
#           |    cancel_order()      |                          |    eliminar y después |
#           |                        |  - id: id del la orden   |    se lo envía por    |
#           |                        |    que se desea eliminar.|    contexto a un      |
#           |                        |                          |    template.          |
#           +------------------------+--------------------------+-----------------------+
#           |                        |                          |                       |
#           |                        |  - request: datos de     |  - Elimina la orden   |
#           |                        |    la solicitud.         |   correspondiente     |
#           | cancel_order_confirm() |                          |   al order_id.        |
#           |                        |  - id: id de la orden    |                       |
#           |                        |    que se desea eliminar.|                       |                
#           |                        |                          |                       |
#           +------------------------+--------------------------+-----------------------+
#           |                        |                          |                       |
#           |                        |  - request: datos de     |  - Elimina los items  |
#           |                        |    la solicitud.         |    seleccionados desde|
#           |     update_order()     |                          |    el template.       |
#           |                        |  - id: id de la orden a  |                       |
#           |                        |    la que se le          |                       |
#           |                        |    eliminarán items.     |                       |
#           +------------------------+--------------------------+-----------------------+
#           |                        |                          |  - Envía un email de  |
#           |                        |  - order_id: id de la    |    confirmación con   |
#           |     update_confirm()   |    orden a la que se     |    los datos de la    |
#           |                        |    le eliminaron items   |    orden actualizados.|
#           |                        |                          |                       |
#           |                        |                          |                       |
#           +------------------------+--------------------------+-----------------------+
#           |                        |                          |  - Construye un       |
#           |                        |  -order_id: id de la     |    mensaje genérico   |
#           |                        |   orden a la que se le   |    que se enviará vía |
#           |                        |   realizó un cambio.     |    email con los datos|
#           |      confirm()         |                          |    del cambio que se  |
#           |                        |  - notas: lista con los  |    le hizo a una      |
#           |                        |    mensajes a usar.      |    orden.             |
#           |                        |                          |                       |
#           +------------------------+--------------------------+-----------------------+
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
    return render(request, 'orders/order/cancel_order_confirm.html', {'order' : order})

def cancel_order_confirm(request, id):
    order = Order.objects.get(id=id)
    notas=['cancelled','were contained','cancellation']
    confirm(order.id,notas)
    order.delete()
    return redirect('order_list')

def order_detail(request, id):
    order = Order.objects.get(id=id)    #   Obtener id de la orden que se quiere consultar 

    #   Variable que indica si ya han pasado o no las 24 horas desde que se confirmó la orden. 
    # Flag igual a True indica que aún puede modificarse la orden, dado que no han pasado 24 horas.
    # Flag igual a False indica que ya no puede modificarse la orden, dado que ya pasaron 24 horas.
    flag = True  

    todays_date = datetime.now() # Obtener fecha y hora del sistema (esta variable no considera la zona horaria)
    timezone = pytz.timezone(settings.TIME_ZONE) # Se crea una zona horaria en formato tzfile basada en la zona horaria 
                                                 # definida en el archivo settings del proyecto.

    todays_date_wo = timezone.localize(todays_date) # Se asigna la zona horaria 'timezone' a la fecha del sistema 
    takeaway_hours = todays_date_wo - timedelta(hours=24) # Se obtienen la fecha y hora exactas 24 antes de la fecha actual.
    
    # Se obtiene la fecha en la que fue confirmada la orden y se transforma a la zona horaria del sistema local (provista en el archivo settings). 
    order_date = order.created.replace(tzinfo=pytz.utc)
    order_date = order_date.astimezone(timezone)

    # ¿Ya pasaron 24 horas desde la confirmación del pedido?:
    if (takeaway_hours > order_date):
        flag = False

    # Listar los artículos de la orden
    order_items = OrderItem.objects.filter(order=id)
    return render(request, 'orders/order/items_list.html', {'order' : order,
                                                            'order_items' : order_items,
                                                            'flag' : flag,})

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
    message_part4 = '\n\n\n Total: $'+ str(order.get_total_cost())
    message_part5 = '\n\n\n Date of '+ notas[2] +' : ' + datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    body = message + message_part2 + message_part3 + message_part4 + message_part5

    # Se envía el correo.
    send_mail(subject, body, 'pruebas.jogglez@gmail.com', [order.email], fail_silently=False)

def update_confirm(order_id):
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
        # Se extrae la lita de OrderItems seleccionadas.
        ids_to_delete = request.POST.getlist('item')
        # Validamos que se haya seleccionado por lo menos un OrderItem.
        if len(ids_to_delete) > 0:
            # Se consulan los OrderItem que tiene que tiene la Order.
            items_in_order = OrderItem.objects.filter(order=id)
            # Si se seleccionaron todos los productos de la orden, 
            # entonces se procede a una cancelación total.
            if len(ids_to_delete) == len(items_in_order):
                return cancel_order(request,id)
            # De lo contrario, se procede a la cancelación parcial.
            else:
                for item_id in ids_to_delete:
                    order_item = OrderItem.objects.get(id=item_id)
                    order_item.delete()     
                update_confirm(id)
                confirm(id,['modified','are still','modification'])

    return redirect('order_detail',id=id)