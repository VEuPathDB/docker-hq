from django.http import HttpResponseRedirect
from django.conf import settings
from re import compile


class LoginRequiredMiddleware(object):
  """
  Adapted for Django 1.10 from
  https://python-programming.courses/recipes/django-require-authentication-pages/

  Middleware that requires a user to be authenticated to view any page other
  than LOGIN_URL. Exemptions to this requirement can optionally be specified
  in settings via a list of regular expressions in LOGIN_EXEMPT_URLS (which
  you can copy from your urls.py).

  Requires authentication middleware and template context processors to be
  loaded. You'll get an error if they aren't.
  """


  def __init__(self, get_response):
    self.get_response = get_response
    self.exempt_urls = [compile(settings.LOGIN_URL.lstrip('/'))]
    if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
      self.exempt_urls += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]

  def __call__(self, request):
    print("LoginRequiredMiddleware __call__ with request %s" % request)
    assert hasattr(request, 'user'), "The Login Required middleware\
 requires authentication middleware to be installed. Edit your\
 MIDDLEWARE setting to insert\
 'django.contrib.auth.middlware.AuthenticationMiddleware'. If that doesn't\
 work, ensure your TEMPLATE_CONTEXT_PROCESSORS setting includes\
 'django.core.context_processors.auth'."
    if not request.user.is_authenticated():
      path = request.path_info.lstrip('/')
      if not any(m.match(path) for m in self.exempt_urls):
        print("REDIRECT with %s" % path)
        return HttpResponseRedirect('{0}?next=/{1}'.format(settings.LOGIN_URL, path))
    response = self.get_response(request)
    return response
