#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Blocos combinacionais de somadores em MyHDL.

Este modulo declara implementacoes de:
- meio somador (half adder),
- somador completo (full adder),
- somador de 2 bits,
- somador generico por encadeamento,
- somador vetorial comportamental.
"""

from myhdl import *


@block
def halfAdder(a, b, soma, carry):
    "Meio Somador de 1 bit"

    @always_comb

    def comb():
        soma.next = a ^ b
        carry.next = a & b

    return comb

@block
def fullAdder(a, b, c, soma, vaiUm):

    s = [Signal(bool(0)) for _ in range(3)]

    haList = [None for _ in range(2)]

    haList[0] = halfAdder(a, b, s[0], s[1])

    haList[1] = halfAdder(c, s[0], soma, s[2])

    @always_comb
    def comb():
        vaiUm.next = s[1] | s[2]

    return instances()


@block
def adder2bits(x, y, soma, carry):
    c = Signal(bool(0))
    fa0 = fullAdder(x[0], y[0], Signal(bool(0)), soma[0], c)
    fa1 = fullAdder(x[1], y[1], c, soma[1], carry)
    return instances()


@block
def adder(x, y, soma, carry):
    n = len(x)
    c = [Signal(bool(0)) for _ in range(n-1)]
    faList = [None for _ in range(n)]
    for i in range(n):
        if i == 0:
            if n == 1:
                faList[i] = fullAdder(x[i], y[i], Signal(bool(0)), soma[i], carry)
            else:
                faList[i] = fullAdder(x[i], y[i], Signal(bool(0)), soma[i], c[i])

        elif i == n-1:
            faList[i] = fullAdder(x[i], y[i], c[i-1], soma[i], carry)

        else:
            faList[i] = fullAdder(x[i], y[i], c[i-1], soma[i], c[i])

    return instances()


@block
def addervb(x, y, soma, carry):

    n = len(x)

    @always_comb
    def comb():
        total = int(x) + int(y)
        soma.next = total & ((1 << n) - 1)
        carry.next = (total >> n) & 1
    return instances()