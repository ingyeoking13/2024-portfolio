def default_serializer(obj):
    if hasattr(obj, 'to_serializable_dict'):
        return obj.to_serializable_dict()
    else:
        raise TypeError(
            f'object of Type {obj.__class__.__name__} ' +
            'is not JSON serializable.')

