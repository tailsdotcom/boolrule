=======
History
=======

0.3.5 (2024-02-09)
==================

* Introduce not∩ operator


0.3.4 (2021-09-24)
==================

* Fixed error caused by early return when evaluating nested expressions.


0.3.3 (2021-07-15)
==================

* Upgrade dependencies.


0.3.2 (2020-09-23)
==================

* Add Type hinting.


0.3.1 (2020-09-09)
==================

* Raise an exception when the whole expression cannot be parsed. Previous behaviour would discard the segment
  that didn't match the expression grammar.


0.3.0 (2018-01-15)
==================

* Add None type and is/isnot operators (contributed by ocurero)


0.2.0 (2016-10-27)
==================

* Fixed error caused by refactor from internal codebase that was preventing deep context level values from being
  referenced in a substitution value


0.1.2 (2016-09-30)
==================

* Improved documentation


0.1.1 (2016-09-30)
==================

* Made ``context`` optional
* Improved documentation


0.1.0 (2016-09-30)
==================

* First release on PyPI.
