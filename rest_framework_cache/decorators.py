"""
decorators to enable the use of cache in the views.
"""

from functools import wraps
from hashlib import md5
from typing import List, Optional

from django.core.cache import cache
from django.db.models.base import ModelBase
from django.utils import translation

from .controls import Reset
from .middlewares import CACHE_KEY_ATTRIBUTE


def cache_view(
    reference: str,
    model: Optional[ModelBase] = None,
    lookup: Optional[str] = None,
    resets: Optional[list[Reset]] = [],
    private: Optional[bool] = False,
):
    """view cache decorator

    this decorator can be used in views based on django rest framework.

    args:
        reference:
            to indicate the identifier.
        model:
            to indicate the base model.
        lookup:
            to indicate the search field.
        resets:
            to indicate the reset conditions.
        private:
            to indicate the privacy.
    """

    __routes = dict()

    def __build_model_name(model):
        return model.__name__.lower()

    def __build_cache_key(request, **kwargs):
        salt = str(request.user.pk) if request.user.is_authenticated and private else ""
        hash = md5((request.build_absolute_uri() + salt).encode("ascii")).hexdigest()

        if model:
            model_reference = __build_model_name(model)
            model_instance_reference = kwargs.get(lookup, "")

        else:
            model_reference = model_instance_reference = ""

        return f"{reference}:{model_reference}:{model_instance_reference}:{hash}:{translation.get_language()}"

    def __reset_by_reference(*args, **kwargs):
        cache.delete_many(cache.keys(f"{reference}:*"))

    def __reset_by_model(*args, **kwargs):
        cache.delete_many(cache.keys(f"{reference}:{__build_model_name(model)}:*"))

    def __reset_by_model_instance(instance, *args, **kwargs):
        cache.delete_many(
            cache.keys(
                f"{reference}:{__build_model_name(model)}:{getattr(instance, lookup)}:*"
            )
        )

    def __reset_external(sender, instance, *args, **kwargs):
        if not lookup:
            __reset_by_model()

        else:
            for route in __routes.get(__build_model_name(sender), []):
                for instance in model.objects.filter(
                    **route.build_filter(instance)
                ).distinct():
                    __reset_by_model_instance(instance)

    def __register_reset():
        for reset in resets:
            receiver = __reset_by_reference

            if model:
                if reset.routes:
                    __routes.setdefault(__build_model_name(reset.model), []).extend(
                        reset.routes
                    )
                    receiver = __reset_external

                else:
                    receiver = __reset_by_model_instance if lookup else __reset_by_model

            for signal in reset.signals:
                signal.connect(receiver, reset.model)

    def decorator(func):
        @wraps(func)
        def controller(request, *args, **kwargs):
            if not hasattr(request, "META"):
                raise TypeError(
                    "cache_view didn't receive an HttpRequest. If you are "
                    "decorating a classmethod, be sure to use "
                    "@method_decorator."
                )

            if request.method != "GET":
                return func(request, *args, **kwargs)

            cache_key = __build_cache_key(request, **kwargs)
            cache_response = cache.get(cache_key, None)

            if cache_response:
                return cache_response

            response = func(request, *args, **kwargs)
            setattr(response, CACHE_KEY_ATTRIBUTE, cache_key)

            return response

        return controller

    __register_reset()

    return decorator
