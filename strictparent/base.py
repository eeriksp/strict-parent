# Three underscores to avoid potential conflicts with Python's own features
FINALIZED = '___finalized___'
OVERRIDES = '___overrides___'
FORCE_OVERRIDE = '___force_override___'


class EmptyClass:
    # TODO Perhaps it should be an empty ABC class,
    # because ABCMeta adds its own features.
    pass


class InheritanceError(AssertionError):
    pass


class Wrapper:
    """
    Wraps the original object
    to enable assigning attributes to objects with a closed scope
    """
    def __init__(self, obj, name, value):
        self.obj = obj
        setattr(self, name, value)

    def __getattr__(self, name):
        return getattr(self.obj, name)

    def __get__(self, instance, owner):
        return self.obj.fget(self.obj)
    # FIXME Implement setter and deleater as well


def final(obj):
    setattr(obj, FINALIZED, True)
    return obj


def overrides(obj):  # TODO all descriptors should use the same pattern
    try:
        setattr(obj, OVERRIDES, True)
        return obj
    # "AssertionError: '(...)' object has no attribute '___overrides___'"
    except Exception:
        return Wrapper(obj, OVERRIDES, True)


def force_override(obj):
    setattr(obj, FORCE_OVERRIDE, True)
    return obj


class StrictParent:
    def __init_subclass__(cls):
        cls_name = cls.__name__
        bases = cls.__bases__
        namespace = cls.__dict__

        # Check if `@overrides` are valid
        sum_of_base_dicts = {}
        for base in bases:
            sum_of_base_dicts.update(base.__dict__)

        all_base_class_member_names = {name for name in sum_of_base_dicts}

        functions = {name: value for (name, value) in namespace.items()
                     if callable(value) or isinstance(value, (staticmethod, classmethod, property))}
        for name, value in functions.items():
            if getattr(value, OVERRIDES, False) or getattr(value, FORCE_OVERRIDE, False):
                for base in bases:
                    if getattr(base, name, False):
                        break
                else:
                    raise InheritanceError(f'`{name}` of {cls_name} claims to '
                                           'override a parent class method, but no parent class method with that name were found.')
            else:
                # TODO We now exclude all built-in method including `__str__`.
                # Should be so that if they are overridden in parent class (not equal to object.this_method),
                # then they should be taken into account.
                if name in all_base_class_member_names and name not in EmptyClass.__dict__:
                    raise InheritanceError(f'`{name}` of {cls_name} is '
                                           'overriding a parent class method, but does not have `@overrides` decorator.')

        # Check `@final` violations
        for name, value in functions.items():
            if not getattr(value, FORCE_OVERRIDE, False):
                for base in bases:
                    base_class_method = getattr(base, name, False)
                    if not base_class_method:
                        # i.e. this method does not exist in the base class
                        continue
                    if getattr(base_class_method, FINALIZED, False):
                        raise InheritanceError(
                            f'`{base_class_method.__name__}` is finalized in `{base.__name__}`. '
                            'You cannot override it unless you decorate it with `@force_override`.')
