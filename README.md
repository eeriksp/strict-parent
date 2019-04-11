# StrictParent

Python is built to be as dynamic and permissive as possible. However, especially in case of larger applications it is beneficial to establish some stricter principles. StrictParent helps you to make your Python classes more structured and enforcing contracts while still leaving the opportunity to break the rules if necessary.

light-weighted and dependency free 😊

## Features

- `StrictParent` -- parent class for all your custom classes using these functionalities
- `@final` -- makes a method finalized, raises `InheritanceError` if subclasses try to override this method
- `@overrides` -- decorator for methods, states that this subclass method is overriding a method in parent class. If parent class does not have such a method, raises an `InheritanceError`. Also, if a subclass is overriding a parent class method without making it explicit by using this decorator, an exception is risen.
- `@force_override` -- decorator for overriding finalized parent class methods.

The purpose of this approach is to make the code more understandable and to protect the developer against accidentally overriding a method, which served an important role in the parent class. However all methods can still be overridden if explicitly stated by `@force_override` decorator. This way we can wright a more readable code without loosing any freedom.

Since you might need to use these functionalities together with ABC classes, `StrictParent`'s metaclass inherits from `ABCMeta` to prevent metaclass conflict. This means that once you inherit from `StrictParent`, you have access to all the features of ABC as well.

```py
from strictparent import StrictParent, final, overrides
from abc import abstractmethod


class Parent(StrictParent):

    def overrideable_method(self):
        return 'I do not mind being overridden'

    @final
    def final_method(self):
        return 'Knowledge & vision arose in me: this is the last birth. There is now no further becoming.'

    @abstractmethod  # You can use all the ABC features here
    def abstract_method(self):
        pass


class ObedientChild(Parent):

    @overrides  # It is now easy to see, that the method has a meaning in the `Parent` class
    def overrideable_method(self):
        return 'Hey'

    @force_override  # Finalized methods can be overridden if explicitly stated
    def final_method(self):
        return 'I am aware I have broken the convention'

    @overrides
    def abstract_method(self):
        return 'Not abstract any more'


class RebelChild(Parent):

    @overrides  # Will raise an exception, because `Parent` class has no such method
    def my_heretic_method(self):
        return 'I claim to be be authentic, but I am just a faker'

    # Will raise an exception, because `@overrides` decorator is missing
    def overrideable_method(self):
        return 'I am hiding my lineage'

    # Will raise an exception, because `final_method` has been finalized in `Parent` class
    def final_method(self):
        return 'I am against the machine!'

```

Please let us know if there are any other features that should be added to this package.

## Contributing

There is no need for a virtual environment since you do not need to install any dependencies.

### Running tests

Being in the root directory:

```sh
cd strictparent/
./tests.py
```
