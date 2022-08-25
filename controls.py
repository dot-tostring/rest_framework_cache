"""
@dataclass classes to define cache reset controls.

resets can be based on signals from the model defined in the view, or from 
models that are related in some way to that model.
"""

from dataclasses import dataclass
from typing import List, Optional
from django.db.models.base import ModelBase
from django.db.models.signals import ModelSignal


@dataclass
class Route:
    """
    @dataclass to relate the model defined in the view to another model related to
    it.
    """

    query: str

    @property
    def build_filter(self, instance: any) -> dict:
        return {self.query: instance}


@dataclass
class Reset:
    """
    @dataclass to define the cache reset conditions of a view.
    """

    model: ModelBase
    signals: List[ModelSignal]
    routes: Optional[List[Route]]

    def __init__(
        self,
        model: ModelBase,
        signals: List[ModelSignal],
        routes: Optional[List[Route]] = None,
    ):
        self.model = model
        self.signals = signals
        self.routes = routes
