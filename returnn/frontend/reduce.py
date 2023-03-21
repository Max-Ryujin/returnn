"""
Reduce
"""

from __future__ import annotations
from typing import Union, TypeVar, Sequence
from returnn.util.basic import NotSpecified
from returnn.tensor import Tensor, Dim
from ._backend import get_backend_by_tensor

T = TypeVar("T")

__all__ = [
    "reduce",
    "reduce_sum",
    "reduce_max",
    "reduce_min",
    "reduce_mean",
    "reduce_logsumexp",
    "reduce_any",
    "reduce_all",
    "reduce_argmin",
    "reduce_argmax",
]


def reduce(
    source: Tensor[T],
    *,
    mode: str,
    axis: Union[Dim, Sequence[Dim]],
    use_time_mask: bool = NotSpecified,
) -> Tensor[T]:
    """
    Reduce the tensor along the given axis

    :param source:
    :param mode: "sum", "max", "min", "mean", "logsumexp", "any", "all", "argmin", "argmax"
    :param axis:
    :param use_time_mask: if True (default), use the time mask (part of dim tag) to ignore padding frames
    :return: tensor with axis removed
    """
    rf = get_backend_by_tensor(source)
    return rf.reduce(source=source, mode=mode, axis=axis, use_time_mask=use_time_mask)


def reduce_sum(source: Tensor[T], *, axis: Union[Dim, Sequence[Dim]], use_time_mask: bool = NotSpecified) -> Tensor[T]:
    """
    Reduce the tensor along the given axis

    :param source:
    :param axis:
    :param use_time_mask: if True (default), use the time mask (part of dim tag) to ignore padding frames
    :return: tensor with axis removed
    """
    return reduce(source=source, mode="sum", axis=axis, use_time_mask=use_time_mask)


def reduce_max(source: Tensor[T], *, axis: Union[Dim, Sequence[Dim]], use_time_mask: bool = NotSpecified) -> Tensor[T]:
    """
    Reduce the tensor along the given axis

    :param source:
    :param axis:
    :param use_time_mask: if True (default), use the time mask (part of dim tag) to ignore padding frames
    :return: tensor with axis removed
    """
    return reduce(source=source, mode="max", axis=axis, use_time_mask=use_time_mask)


def reduce_min(source: Tensor[T], *, axis: Union[Dim, Sequence[Dim]], use_time_mask: bool = NotSpecified) -> Tensor[T]:
    """
    Reduce the tensor along the given axis

    :param source:
    :param axis:
    :param use_time_mask: if True (default), use the time mask (part of dim tag) to ignore padding frames
    :return: tensor with axis removed
    """
    return reduce(source=source, mode="min", axis=axis, use_time_mask=use_time_mask)


def reduce_mean(source: Tensor[T], *, axis: Union[Dim, Sequence[Dim]], use_time_mask: bool = NotSpecified) -> Tensor[T]:
    """
    Reduce the tensor along the given axis

    :param source:
    :param axis:
    :param use_time_mask: if True (default), use the time mask (part of dim tag) to ignore padding frames
    :return: tensor with axis removed
    """
    return reduce(source=source, mode="mean", axis=axis, use_time_mask=use_time_mask)


def reduce_logsumexp(
    source: Tensor[T], *, axis: Union[Dim, Sequence[Dim]], use_time_mask: bool = NotSpecified
) -> Tensor[T]:
    """
    Reduce the tensor along the given axis

    :param source:
    :param axis:
    :param use_time_mask: if True (default), use the time mask (part of dim tag) to ignore padding frames
    :return: tensor with axis removed
    """
    return reduce(source=source, mode="logsumexp", axis=axis, use_time_mask=use_time_mask)


def reduce_any(source: Tensor[T], *, axis: Union[Dim, Sequence[Dim]], use_time_mask: bool = NotSpecified) -> Tensor[T]:
    """
    Reduce the tensor along the given axis

    :param source:
    :param axis:
    :param use_time_mask: if True (default), use the time mask (part of dim tag) to ignore padding frames
    :return: tensor with axis removed
    """
    return reduce(source=source, mode="any", axis=axis, use_time_mask=use_time_mask)


def reduce_all(source: Tensor[T], *, axis: Union[Dim, Sequence[Dim]], use_time_mask: bool = NotSpecified) -> Tensor[T]:
    """
    Reduce the tensor along the given axis

    :param source:
    :param axis:
    :param use_time_mask: if True (default), use the time mask (part of dim tag) to ignore padding frames
    :return: tensor with axis removed
    """
    return reduce(source=source, mode="all", axis=axis, use_time_mask=use_time_mask)


def reduce_argmin(
    source: Tensor[T], *, axis: Union[Dim, Sequence[Dim]], use_time_mask: bool = NotSpecified
) -> Tensor[T]:
    """
    Reduce the tensor along the given axis

    :param source:
    :param axis:
    :param use_time_mask: if True (default), use the time mask (part of dim tag) to ignore padding frames
    :return: tensor with axis removed
    """
    return reduce(source=source, mode="argmin", axis=axis, use_time_mask=use_time_mask)


def reduce_argmax(
    source: Tensor[T], *, axis: Union[Dim, Sequence[Dim]], use_time_mask: bool = NotSpecified
) -> Tensor[T]:
    """
    Reduce the tensor along the given axis

    :param source:
    :param axis:
    :param use_time_mask: if True (default), use the time mask (part of dim tag) to ignore padding frames
    :return: tensor with axis removed
    """
    return reduce(source=source, mode="argmax", axis=axis, use_time_mask=use_time_mask)
