from sqlalchemy import inspect

def to_pydantic(obj):
    return {
        c.key: getattr(obj, c.key)
        for c in inspect(obj).mapper.column_attrs
    }