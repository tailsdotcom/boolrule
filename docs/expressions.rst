===========================
Writing boolean expressions
===========================

The grammar supported by boolrule is fairly simple but powerful.


Whitespace
==========

Except within string literals, all whitespace is ignored.

Literals
========

Numeric literls are written as bare numbers. Floating point and exponent-based
numbers are supported::

 10       # int
 -10      # int with optional sign
 10.5     # float (without optional sign)
 10.5E-3  # equivalent to 0.0105

String literls can be single or double quoted::

 "Hello, world"
 'boolrule rulez"

Boolean literals are the bare values ``true`` and ``false``


Property paths
==============

In order to reference values from the context passed into the ``test()``
method you specify the path to the property as a dot-separated identifier::

 foo
 foo.bar
 foo.bar.baz

At evaluation time, these will map to either object attributes or dict keys in
that order.


Basic comparison operators
==========================

=======================  ========================  ===========
Operator                 Description               Example
=======================  ========================  ===========
``=``, ``==``, ``eq``    Equality                  ``foo == 5``
``!=``, ``!==``, ``ne``  Inequality                ``bar != 5``
``>``, ``gt``            Greater than              ``foo > 5``
``>=``, ``gte``          Greater than or equal to  ``foo >= 5``
``<``, ``lt``            Less than                 ``foo < 5``
``<=``, ``lte``          Less than or equal to     ``foo <= 5``
=======================  ========================  ===========


Logical operators
=================

=======================  ========================  =========================
Operator                 Description               Example
=======================  ========================  =========================
``and``                  Logical and               ``foo == 5 and bar < 10``
``oe``                   Logical or                ``bar == 5 or bar < 10``
=======================  ========================  =========================


Membership operators
====================

=======================  ========================  =========================
Operator                 Description               Example
=======================  ========================  =========================
``in``                   Is a member of            ``foo in ("a","b","c")``
``notin``                Is not a member of        ``foo not in ("a","b")``
=======================  ========================  =========================


Nested expressions
==================

You can use parentheses to next expressions::

 foo > 5 and (10 < bar or bar > 20)
