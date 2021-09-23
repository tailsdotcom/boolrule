# -*- coding: utf-8 -*-
from typing import List, Any
from pyparsing import (  # type: ignore
    CaselessLiteral,
    Word,
    delimitedList,
    Optional,
    Combine,
    Group,
    alphas,
    nums,
    alphanums,
    Forward,
    oneOf,
    quotedString,
    ZeroOrMore,
    Keyword,
    ParseResults,
    removeQuotes,
    Suppress,
)


class SubstituteVal(object):
    """
    Represents a token that will later be replaced by a context value.
    """

    def __init__(self, t):
        # type: (List[Any]) -> None
        self._path = t[0]

    def get_val(self, context):
        # type: (Any) -> Any
        if not context:
            raise MissingVariableException(
                'context missing or empty'
            )

        val = context

        try:
            for part in self._path.split(pathDelimiter):
                val = getattr(val, part) if hasattr(val, part) else val[part]

        except KeyError:
            raise MissingVariableException(
                'no value supplied for {}'.format(self._path)
            )

        return val

    def __repr__(self):
        # type: () -> str
        return 'SubstituteVal(%s)' % self._path


# Grammar definition
pathDelimiter = '.'
identifier = Word(alphas, alphanums + "_")
propertyPath = delimitedList(identifier, pathDelimiter, combine=True)

and_ = Keyword("and", caseless=True)
or_ = Keyword("or", caseless=True)
in_ = Keyword("in", caseless=True)

lparen = Suppress('(')
rparen = Suppress(')')

binaryOp = oneOf(
    "= == != < > >= <= eq ne lt le gt ge in notin is isnot "
    "≠ ≤ ≥ ∈ ∉ ⊆ ⊇ ∩", caseless=True
)('operator')

E = CaselessLiteral("E")
numberSign = Word("+-", exact=1)
realNumber = Combine(
    Optional(numberSign) + (
        Word(nums) + "." + Optional(Word(nums))
        | ("." + Word(nums))
    ) + Optional(E + Optional(numberSign) + Word(nums))
)

integer = Combine(
    Optional(numberSign) + Word(nums) + Optional(
        E + Optional("+") + Word(nums)
    )
)

str_ = quotedString.addParseAction(removeQuotes)
bool_ = oneOf('true false', caseless=True)
none_ = CaselessLiteral('none')

simpleVals = (
    realNumber.setParseAction(lambda toks: float(toks[0]))
    | integer.setParseAction(lambda toks: int(toks[0]))
    | str_
    | bool_.setParseAction(lambda toks: toks[0] == 'true')
    | none_.setParseAction(lambda toks: [None])  # see pyparsing bug 63
    | propertyPath.setParseAction(lambda toks: SubstituteVal(toks))
)  # need to add support for alg expressions

propertyVal = (
    simpleVals
    | (lparen + Group(delimitedList(simpleVals)) + rparen)
)
boolExpression = Forward()
boolCondition = Group(
    (Group(propertyVal)('lval') + binaryOp + Group(propertyVal)('rval'))
    | (lparen + boolExpression + rparen)
)
boolExpression << boolCondition + ZeroOrMore((and_ | or_) + boolExpression)


class BoolRule(object):
    """
    Represents a boolean expression and provides a `test` method to evaluate
    the expression and determine its truthiness.

    :param query: A string containing the query to be evaluated
    :param lazy: If ``True``, parse the query the first time it's tested rather
                 than immediately. This can help with performance if you
                 instantiate a lot of rules and only end up evaluating a
                 small handful.
    """

    _compiled = False
    _tokens = []  # type: List[Any]

    def __init__(self, query, lazy=False):
        # type: (str, bool) -> None
        self._query = query
        if not lazy:
            self._compile()

    def test(self, context=None):
        # type: (Any) -> bool
        """
        Test the expression against the given context and return the result.

        :param context: A dict context to evaluate the expression against.
        :return: True if the expression succesfully evaluated against the
                 context, or False otherwise.
        """
        if self._is_match_all():
            return True

        self._compile()
        return self._test_tokens(self._tokens, context)

    def _is_match_all(self):
        # type: () -> bool
        return True if self._query == '*' else False

    def _compile(self):
        # type: () -> None
        if not self._compiled:

            # special case match-all query
            if self._is_match_all():
                return

            self._tokens = boolExpression.parseString(self._query, True)
            self._compiled = True

    def _expand_val(self, val, context):
        # type: (Any, Any) -> Any
        if type(val) == list:
            val = [self._expand_val(v, context) for v in val]

        if isinstance(val, SubstituteVal):
            ret = val.get_val(context)
            return ret

        if isinstance(val, ParseResults):
            return [self._expand_val(x, context) for x in val.asList()]

        return val

    def _test_tokens(self, tokens, context):
        # type: (List[Any], Any) -> bool
        passed = False

        for token in tokens:
            if not isinstance(token, ParseResults):
                if token == 'or' and passed:
                    return True
                elif token == 'and' and not passed:
                    return False
                continue

            if not token.getName():
                passed = self._test_tokens(token, context)
                continue

            items = token.asDict()

            operator = items['operator']
            lval = self._expand_val(items['lval'][0], context)
            rval = self._expand_val(items['rval'][0], context)

            if operator in ('=', '==', 'eq'):
                passed = lval == rval
            elif operator in ('!=', 'ne', '≠'):
                passed = lval != rval
            elif operator in ('>', 'gt'):
                passed = lval > rval
            elif operator in ('>=', 'ge', '≥'):
                passed = lval >= rval
            elif operator in ('<', 'lt'):
                passed = lval < rval
            elif operator in ('<=', 'le', '≤'):
                passed = lval <= rval
            elif operator in ('in', '∈'):
                passed = lval in rval
            elif operator in ('notin', '∉'):
                passed = lval not in rval
            elif operator == 'is':
                passed = lval is rval
            elif operator == 'isnot':
                passed = lval is not rval
            elif operator == '⊆':
                passed = all((False for x in lval if x not in rval))
            elif operator == '⊇':
                passed = all((False for x in rval if x not in lval))
            elif operator == '∩':
                passed = any((True for x in lval if x in rval))
            else:
                raise UnknownOperatorException(
                    "Unknown operator '{}'".format(operator)
                )

        return passed


class MissingVariableException(Exception):
    """
    Raised when an expression contains a property path that's not supplied in
    the context.
    """
    pass


class UnknownOperatorException(Exception):
    """
    Raised when an expression uses an unknown operator.

    This should never be thrown since the operator won't be correctly parsed as
    a token by pyparsing, but it's useful to have this hanging around for when
    additional operators are being added.
    """
    pass
