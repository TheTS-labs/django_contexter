METHODS_THAT_RENTURN_NEW_QUERYSET = set(
    [
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
    ]
)

METHODS_THAT_DO_NOT_RETURN_QUERYSET = set(
    [
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
    ]
)

METHODS_THAT_CHAGES_RECORDS = set(
    [
        "create",
        "get_or_create",
        "update_or_create",
        "bulk_create",
        "bulk_update",
        "update",
        "delete",
    ]
)

ASYNC_METHODS_THAT_DO_NOT_RETURN_QUERYSET = set(
    ["a" + element for element in METHODS_THAT_DO_NOT_RETURN_QUERYSET]
)

ASYNC_METHODS_THAT_CHAGES_RECORDS = set(
    ["a" + element for element in METHODS_THAT_CHAGES_RECORDS]
)

UNSAFE_METHODS = METHODS_THAT_CHAGES_RECORDS.copy()

ASYNC_UNSAFE_METHODS = ASYNC_METHODS_THAT_CHAGES_RECORDS.copy()

ALL_UNSAFE_METHODS = UNSAFE_METHODS.copy()
ALL_UNSAFE_METHODS.update(ASYNC_UNSAFE_METHODS)

ALL_METHODS = METHODS_THAT_RENTURN_NEW_QUERYSET
ALL_METHODS.update(METHODS_THAT_DO_NOT_RETURN_QUERYSET)
ALL_METHODS.update(ASYNC_METHODS_THAT_DO_NOT_RETURN_QUERYSET)

ALL_SAFE_METHODS = ALL_METHODS - ALL_UNSAFE_METHODS
