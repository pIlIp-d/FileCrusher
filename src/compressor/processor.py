from functools import wraps


def processor(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        for handler in self.event_handlers:
            if hasattr(handler, "preprocess"):
                handler.preprocess(*args, **kwargs)
        ret = method(self, *args, **kwargs)
        for handler in self.event_handlers:
            if hasattr(handler, "postprocess"):
                handler.postprocess(*args, **kwargs)
        return ret

    return wrapper
