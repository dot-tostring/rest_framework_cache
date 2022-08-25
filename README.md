# REST FRAMEWORK CACHE

REST Framework Cache is a powerful and flexible toolkit for building cached 
views based on a fully dynamic lifecycle based on the variation of the 
information they provide.

REST Framework Cache is based on the Django REST Framework viewsets.

## Installation

The caching mechanisms are implemented in a middleware. Add it to your `MIDDLEWARE` setting:
```python
MIDDLEWARE = [
    #
    'rest_framework_cache.middlewares.RestFrameworkCacheMiddleware',
]
```
## Documentation

These arguments can be configured in the decorator:

* __reference__: Indicates de view reference.
* __model__: Indicates de model when using ModelViewSet.
* __lookup__: Indicates de lookup_field when using ModelViewSet.
* __resets__: Indicated a list of invalidation conditions.
* __private__: Indicates whether a view is relative to the user.

For non-detail based views __lookup__ argument should not be used.

These arguments can be configured in the controls:

* __model__: Indicates the model exposed to the signals.
* __signals__: Indicates the signals.
* __routes__: Indicates the route to the model indicated in the view.

The routes have to be defined as follows:
```python
Route(AttributeValue, 'attribute__product_class__products')
```
## Example

Let's take a look at a quick example of using REST framework cache.

In this example, the product list cache will be invalidated when a new 
product is created or an existing product is modified or deleted.

The product retrieve cache of the existing product that is modified or deleted 
will also be invalidated.
```python
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from django.db.models.signals import pre_save, pre_delete
from django.utils.decorators import method_decorator

from rest_framework_cache.controls import Reset, Route
from rest_framework_cache.decorators import cache_view

from warehouse.api.serializers import ProductSerializer
from warehouse.api.models import Product

@method_decorator(
    cache_view(
        'product-list',
        model = Product,
        resets = [
            Reset(
                model = Product
                signals = [pre_save, pre_delete]
            )
        ],
    ),
    name = 'list'
)
@method_decorator(
    cache_view(
        'product-retrieve',
        model = Product,
        lookup = 'identifier',
        resets = [
            Reset(
                model = Product
                signals = [pre_save, pre_delete]
            )
        ],
    ),
    name = 'retrieve'
)
class ProductModelViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'identifier'
    queryset = Product.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
```