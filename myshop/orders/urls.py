#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: urls.py
#
# Descripción:
#   En este archivo se definen las urls de la app de las órdenes.
#
#   Cada url debe tener la siguiente estructura:
#
#   path( url, vista, nombre_url )
#
#-------------------------------------------------------------------------

from django.urls import path, re_path
from . import views

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('list/',views.order_list,name='order_list'),
    path('cancel-order/<int:id>',views.cancel_order,name='cancel_order'),
    path('cancel-order-confirm/<int:id>',views.cancel_order_confirm,name='cancel_order_confirm'),
    path('order-detail/<int:id>',views.order_detail,name='order_detail'),
    path('update-order/<int:id>',views.update_order, name='update_order'),
]
