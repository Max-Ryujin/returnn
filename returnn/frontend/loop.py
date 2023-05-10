"""
While loop.

Why did we choose this API?
To allow for both eager-based and graph-based frameworks,
and also to avoid any magic happening here.
https://github.com/rwth-i6/returnn/issues/1282
https://github.com/rwth-i6/returnn/issues/1324
"""

from __future__ import annotations
from typing import Optional, Union, TypeVar, Callable, Tuple
import tree
from returnn.tensor import Tensor, Dim
import returnn.frontend as rf
from .tensor_array import TensorArray
from ._backend import global_backend


__all__ = ["while_loop", "scan"]


S = TypeVar("S")
X = TypeVar("X")  # any nested structure, can be None
Y = TypeVar("Y")  # any nested structure, can be None


def while_loop(
    cond: Callable[[S], Union[bool, Tensor]],
    body: Callable[[S], S],
    initial: S,
) -> S:
    """
    It executes::

        while cond(loop_vars):
            loop_vars = body(loop_vars)

    And then it returns the final loop vars.

    If you want to iterate over some axis,
    maybe of an existing tensor,
    or if you want to accumulate frames in each iteration,
    see :func:`scan`.

    :param cond:
    :param body:
    :param initial: initial loop vars
    :return: final loop vars
    """
    # noinspection PyProtectedMember
    backend = initial[0]._raw_backend if initial is not None else global_backend
    if backend.executing_eagerly():
        loop_vars = initial
        while cond(loop_vars):
            loop_vars = body(loop_vars)
        return loop_vars
    raise NotImplementedError("while_loop() not implemented for backend %r" % backend)


def scan(
    *,
    spatial_dim: Optional[Dim] = None,
    initial: S = None,
    xs: X = None,
    ys: Y = None,
    cond: Optional[Callable[[S, X], Tensor]] = None,
    body: Callable[[S, X], Tuple[S, Y]],
    max_seq_len: Optional[int] = None,
) -> Tuple[S, Y, Dim]:
    """
    Extended variant of :func:`while_loop`.

    Supports iterating over a given axis (spatial_dim),
    supports iterating over some input tensors (xs: X) on the given axis,
    and supports returning some frame-accumulated output tensors (ys: Y).

    https://github.com/rwth-i6/returnn/issues/1324

    :param spatial_dim: if None or unknown, need to provide cond. must be given if xs is not None.
    :param initial: state/carry
    :param xs: input, will be unstacked over spatial_dim. can be None.
    :param ys: output, as templates, per iteration (excluding spatial_dim)
    :param cond: if spatial_dim is None/unknown, need to provide this.
        unlike while_loop cond, does not need to be scalar.
    :param body:
    :param max_seq_len:
    :return: final state, outputs ys, and the new spatial_dim
    """
    if spatial_dim is None or not spatial_dim.is_dim_known():
        assert cond is not None, f"scan: spatial_dim {spatial_dim} is None/unknown, need to provide `end`"
        assert xs is None, f"scan: spatial_dim {spatial_dim} is None/unknown, cannot use input `xs` {xs}"
        if spatial_dim is None:
            spatial_dim = Dim(None, name="scan_dim")

        def _cond(_s: Tuple[Tensor, Tensor, Tensor, S, Y]) -> Tensor:
            i, _, c, _, _ = _s
            c = rf.reduce_any(c, axis=c.dims)
            if max_seq_len is not None:
                c = rf.logical_and(c, i < max_seq_len)
            return c

        def _body(_s: Tuple[Tensor, Tensor, Tensor, S, Y]) -> Tuple[Tensor, Tensor, Tensor, S, Y]:
            i, seq_len_, prev_cond, s, ys_ = _s
            s, y = body(s, None)
            tree.assert_same_structure(ys_, y)
            ys_ = tree.map_structure(lambda ys__, y_: ys__.push_back(y_), ys_, y)
            c = cond(s, None)
            c = rf.logical_and(c, prev_cond)
            seq_len_ = seq_len_ + rf.cast(c, dtype=seq_len_.dtype)
            return i + 1, seq_len_, c, s, ys_

        _, seq_len, _, final_s, ys = while_loop(
            _cond,
            _body,
            (
                rf.constant(0, dtype=rf.get_default_array_index_dtype()),  # i
                rf.constant(0, dtype=rf.get_default_array_index_dtype()),  # seq_len
                cond(initial, None),  # initial cond. keep this in state such that we can update seq_len in body
                initial,  # state
                tree.map_structure(lambda y: TensorArray(y), ys),
            ),
        )

        spatial_dim.dyn_size_ext = seq_len
        return final_s, tree.map_structure(lambda ys_: ys_.stack(axis=spatial_dim), ys), spatial_dim

    else:
        assert cond is None, f"scan: spatial_dim {spatial_dim} is known, cannot use `end` {cond}"
        raise NotImplementedError
