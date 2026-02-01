"""
Project config. Apply Python 3.14 compatibility patch for Django template context.
"""
import sys

# Python 3.14+: Django's BaseContext.__copy__ can fail with:
# AttributeError: 'super' object has no attribute 'dicts' and no __dict__ for setting new attributes
# Patch BaseContext and Context so the admin changelist (and other template views) work.
if sys.version_info >= (3, 14):
    import copy as _copy_mod
    from django.template.context import BaseContext, Context

    def _patched_base_context_copy(self):
        duplicate = BaseContext()
        duplicate.__class__ = self.__class__
        duplicate.dicts = self.dicts[:]
        for key, value in self.__dict__.items():
            if key != "dicts":
                try:
                    setattr(duplicate, key, value)
                except AttributeError:
                    pass
        return duplicate

    def _patched_context_copy(self):
        duplicate = _patched_base_context_copy(self)
        if hasattr(self, "render_context"):
            duplicate.render_context = _copy_mod.copy(self.render_context)
        return duplicate

    BaseContext.__copy__ = _patched_base_context_copy
    Context.__copy__ = _patched_context_copy
