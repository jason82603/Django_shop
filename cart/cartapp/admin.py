from django.contrib import admin
from cartapp import models

class ordersAdmin(admin.ModelAdmin):
 	list_display=('id','subtotal','shipping','customname','customemail','customaddress','customphone','paytype')

 	search_fields=('id',)
 	ordering=('id',)

class detailAdmin(admin.ModelAdmin):
 	list_display=('id','pname','unitprice','quantity','dtotal','dorder_id',)

 	search_fields=('id',)
 	ordering=('id',)

admin.site.register(models.OrdersModel,ordersAdmin)
admin.site.register(models.DetailModel,detailAdmin)
admin.site.register(models.ProductModel)


