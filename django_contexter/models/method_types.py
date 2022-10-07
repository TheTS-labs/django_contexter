"""Lists with classified Django QuerySet API methods."""

from functools import reduce

METHODS_THAT_RENTURN_NEW_QUERYSET = frozenset((
    "filter",
    "exclude",
    "annotate",
    "alias",
    "order_by",
    "reverse",
    "distinct",
    "values",
    "values_list",
    "dates",
    "datetimes",
    "none",
    "all",
    "union",
    "intersection",
    "difference",
    "select_related",
    "prefetch_related",
    "extra",
    "defer",
    "only",
    "using",
    "select_for_update",
    "raw",
))

METHODS_THAT_DO_NOT_RETURN_QUERYSET = frozenset((
    "get",
    "create",
    "get_or_create",
    "update_or_create",
    "bulk_create",
    "bulk_update",
    "count",
    "in_bulk",
    # "iterator",
    "latest",
    "earliest",
    "first",
    "last",
    "aggregate",
    "exists",
    "contains",
    "update",
    "delete",
    "as_manager",
    "explain",
))

METHODS_THAT_CHAGES_RECORDS = frozenset((
    "create",
    "get_or_create",
    "update_or_create",
    "bulk_create",
    "bulk_update",
    "update",
    "delete",
))

ASYNC_METHODS_THAT_DO_NOT_RETURN_QUERYSET = frozenset((
    "a{0}".format(element) for element in METHODS_THAT_DO_NOT_RETURN_QUERYSET
))

ASYNC_METHODS_THAT_CHAGES_RECORDS = frozenset((
    "a{0}".format(element) for element in METHODS_THAT_CHAGES_RECORDS
))

UNSAFE_METHODS = METHODS_THAT_CHAGES_RECORDS.copy()

ASYNC_UNSAFE_METHODS = ASYNC_METHODS_THAT_CHAGES_RECORDS.copy()

ALL_UNSAFE_METHODS = reduce(frozenset.union, [UNSAFE_METHODS, ASYNC_UNSAFE_METHODS])

ALL_METHODS = reduce(frozenset.union, [
    METHODS_THAT_RENTURN_NEW_QUERYSET,
    METHODS_THAT_DO_NOT_RETURN_QUERYSET,
    ASYNC_METHODS_THAT_DO_NOT_RETURN_QUERYSET,
])

ALL_SAFE_METHODS = reduce(frozenset.union, [ALL_METHODS, ALL_UNSAFE_METHODS])
