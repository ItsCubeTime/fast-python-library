import typing


class Base:
    "Generic baseclass that reduces common boilerplate code"
    def __init_subclass__(cls) -> None:

        # Implement __repr__ BEGIN
        # if hasattr(cls, "__str__") and not hasattr(cls, "__repr__"):
        def __repr__(self) -> str:
            """__repr__ is used instead of __str__ in scenarios where 'less ambiguity' is desired, 
            for instance, __repr__ is used for the elements in a list when printing the list."""
            # Why not just return self.__str__() you might ask? Because if __str__ is not implemented on the object the default __str__ implementation will point back
            # to __repr__ causing an endless loop, so we need to prevent that.
            if self.__repr_internal_calltimes__ > 0:
                return self.__repr_legacy__()
            else:
                self.__repr_internal_calltimes__ += 1
                returnVal = self.__str__()
                return returnVal
        if hasattr(cls, "__repr__"):
            cls.__repr_legacy__ = cls.__repr__
        cls.__repr_internal_calltimes__ = 0
        cls.__repr__ = __repr__
        # Implement __repr__ END

    def __init__(self) -> None:
        # For every attribute of this class instance, confirm that the attribute is a class & if it is,
        # instanciate it & give it a outerClassInstance attribute pointing to this class instance. BEGIN
        super().__init__()
        children = dir(self)
        for childName in children:
            child = eval(f"self.{childName}")
            if isinstance(child, type):
                child.outerClassInstance = self
                exec(f"self.{childName} = child(); self.{childName}.outerClassInstance = self")
        # For every attribute of this class instance, confirm that the attribute is a class & if it is,
        # instanciate it & give it a outerClassInstance attribute pointing to this class instance. END


# class InstanciatableBase(Base):
class _propertyNone:
    pass
class property():
    """A compatible replacement for Pythons built in @property decorator class that enables 
    combined getter/setter methods and convenient storing of data on the property itself.

    Go to definition for example usage
"""
    if False:
        class MyCls():
            @property
            def method(self, value=None):
                if value != None:
                    self.value = value
                return self.value
            method.value = "default"
        classInstance = MyCls()
        print(MyCls.method)
        print(classInstance.method)
        MyCls.method = 4
        classInstance.method = 5
        print(MyCls.method)
        print(classInstance.method)

    def __init__(self,
                 fget: typing.Callable | None = None,
                 fset: typing.Callable | None = None,
                 fdel: typing.Callable | None = None,
                 doc: str | None = ...,
                 ):
        self.getter = fget
        if fset == None and fget.__code__.co_argcount > 1:
            self.setter = fget
        else:
            if fset == None:
                def s(s1=None,v=None):
                    import inspect
                    if inspect.isfunction(s1):
                        self.setter = s1
                        print(f"new setter of {self} is {s1}")
                    else:
                        raise Exception("Property has no setter")
                self.setter = s
            else:
                self.setter = fset
        self.deleter = fdel

    def __setAndGet__(prop, value=None, parent=None):
        print(f"self: {prop}")
        if not hasattr(prop, 'value'):
            prop.value = None
        if value != None:
            prop.value = value

        if prop.getter.__code__.co_argcount == 1:
            print(1)
            return prop.getter(parent)
        if prop.getter.__code__.co_argcount == 2:
            print(2)
            return prop.getter(parent, value)
        print(3)
        return prop.getter(parent, value, prop)


    def getter(prop):
        return prop.value

    def setter(prop, value):
        print('setter')
        prop.value = value
        return prop.getter()

    def __get__(prop, __obj, __type: type | None = ...):
        print("__get")
        return prop.__setAndGet__()

    def __set__(prop, parent, __value):
        print("__set")
        return prop.__setAndGet__(__value, parent)

# class property(): # @todo fix this, it isnt supposed to give a reference to the property as first param to the getters/setters but a ref to the parent obj
#     """A compatible replacement for Pythons built in @property decorator class that enables 
#     combined getter/setter methods and convenient storing of data on the property itself.

#     Go to definition for example usage
# """
#     if False:
#         class MyCls():
#             @property
#             def method(self, value=None):
#                 if value != None:
#                     self.value = value
#                 return self.value
#             method.value = "default"
#         classInstance = MyCls()
#         print(MyCls.method)
#         print(classInstance.method)
#         MyCls.method = 4
#         classInstance.method = 5
#         print(MyCls.method)
#         print(classInstance.method)

#     def __init__(self,
#                  fget: typing.Callable | None = None,
#                  fset: typing.Callable | None = None,
#                  fdel: typing.Callable | None = None,
#                  doc: str | None = ...,
#                  ):
#         self.getter = fget
#         if fset == None and fget.__code__.co_argcount > 1:
#             self.setter = fget
#         else:
#             self.setter = fset
#         self.deleter = fdel

#     def __setAndGet__(self, value=None):
#         if not hasattr(self, 'value'):
#             self.value = None
#         if value != None:
#             self.value = value
#         return self.getter(self)

#     def getter(self):
#         return self.value

#     def setter(self, value):
#         self.value = value
#         return self.getter()

#     def __get__(self, __obj, __type: type | None = ...):
#         return self.__setAndGet__()

#     def __set__(self, __obj, __value):
#         return self.__setAndGet__(__value)


