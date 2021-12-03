class Error(Exception):
    """Base class for cutsom exceptions."""
    
    def __init__(self, message=None):
        # self.expression = expression
        self.message = message
        self.type = self.__class__.__name__


class ModuleError(Error):
    """
    Exception raised for errors which occurs inside modules.

    :param str message: explanation of the error
    :param dictionary *args:  any additional parameters Service may
        need, can be an empty dictionary
    :param dictionary **kwargs: any additional parameters Service may
        need, can be an empty dictionary
    """

    def __init__(self, message='error which occurs inside modules', *args, **kwargs):
        # self.expression = expression
        self.message = message
        self.type = self.__class__.__name__
        
        
class ValidationError(Error):
    """
    Exception raised for input validation errors.

    :param str message: explanation of the error
    :param dictionay errors: validation error key and values
    """

    def __init__(self, message, errors):
        # self.expression = expression
        self.message = message
        self.type = self.__class__.__name__
        self.errors = errors
        

class InterModuleError(Error):
    """
    Exception raised for errors which occurs inside a module
    and the error cause is in another module.

    :param str message: explanation of the error
    :param str source: source of the error
    :param str destination: destination of the error
    :param dictionary *args:  any additional parameters Service may
        need, can be an empty dictionary
    :param dictionary **kwargs: any additional parameters Service may
        need, can be an empty dictionary
    """

    def __init__(self, source, destination, message='errors which occurs inside modules', *args, **kwargs):
        # self.expression = expression
        self.message = message
        self.type = self.__class__.__name__
        self.source = source
        self.destination = destination
