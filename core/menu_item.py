import re
from urllib.parse import urlparse

from django.urls import resolve, Resolver404
from menu import MenuItem

class PermissionsMenuItem(MenuItem):
    """Custom MenuItem that checks permissions based on the view associated
    with a URL"""
    permission = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.permissions = kwargs.get('permissions', None)
        print (self.permissions)

    def check(self, request):
         """Check permissions based on our view"""
         if not request.user.is_authenticated:
             return False

         permissions = self.permissions or []
         try:
            parsed = urlparse(self.url)
            match = resolve(parsed.path)
            if hasattr(match.func.view_class, 'permission_required'):
                permissions.append(match.func.view_class.permission_required)
         except Resolver404:
             pass

         visible = len(permissions) == 0
         for perm in permissions:
             visible = visible or request.user.has_perm(perm)
             print(request.user.has_perm(perm))

         self.visible = visible


    def match_url(self, request):
        """
        match url determines if this is selected
        """
        matched = False
        if self.exact_url:
            if re.match("%s$" % (self.url,), request.path):
                matched = True
        elif re.match("%s" % self.url, request.path):
            matched = True
        return matched