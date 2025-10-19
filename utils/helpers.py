# You can add helper functions here that are used across different apps.
# For this project, the search logic was integrated directly into BookListView
# for simplicity, but more complex filtering could go here.

def custom_filter_example(queryset, param_value):
    """
    Example of a helper function to apply a custom filter.
    """
    if param_value:
        return queryset.filter(some_field__iexact=param_value)
    return queryset

# You can import and use functions from here in your views, e.g.:
# from .utils.helpers import custom_filter_example
# queryset = custom_filter_example(queryset, request.GET.get('genre'))
