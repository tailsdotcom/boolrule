=====
Usage
=====

The entirety of boolrule's functionality is encapsulated in the ``BoolRule``
class.


Getting started
===============

The simplest use case is evaluating simple, self-contained expressions::

    from boolrule import BoolRule

    expression = '5 > 10'
    rule = BoolRule(expression)
    rule.test()  # False

However, the real power of boolrule comes when the expression makes use of
values from the context dict passed to the `test()` method::

    from boolrule import BoolRule

    expression = 'content.is_published = true and user.level in content.allowed_levels'
    rule = BoolRule(expression)

    context = {
        'user': {
            'level': 'super',
        },
        'content': {
            "is_published": True,
            'allowed_levels': [
                'admin',
                'super'
            ]
        },
    }

    if rule.test(context):
        # Let the user see the content
        pass


Lazy compilation
================

By default the expression is compiled when you create a new ``BoolRule``
object. If you're instantiating a lot of ``BoolRule`` instances but are only
likely to call ``test`` on a few of them (because you're looking for just the
first match, for example) then you can use the optional ``lazy``` argument in
the call to ``BoolRule``` to defer compilation until the first call to
``test()``::

    rules = [
        BoolRule(expression, lazy=True)
        for expression in expressions
    ]

    if any(r in rules.test(context)):
        # Do a thing
        pass
