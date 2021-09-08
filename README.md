# Google App Engine Python 3 Standard Environment API library (private preview)

This is a private preview release of the App Engine SDK for Python 3.  It provides access
to various API endpoints that were previously only available on the Python 2.7
runtime.

To sign up for the private preview, visit https://docs.google.com/forms/d/e/1FAIpQLSd1hFLA2UFSYwIMxm9ZI3pwigORZBgjJRH0qrnhtE7nvhhRCQ/viewform.

## Using the SDK

In your `requirements.txt` file, add the following:

`appengine-python-standard>=0.2.0`

In your app's `app.yaml`, add the following:

`app_engine_apis: true`

In your `main.py`, import google.appengine.api.wrap_wsgi_app and call it on your
WSGI app object.

Example for a standard WSGI app:

~~~
  import google.appengine.api

  app = google.appengine.api.wrap_wsgi_app(app)
~~~

Example for a Flask app:

~~~
  import google.appengine.api
  from flask import Flask, request

  app = Flask(__name__)
  app.wsgi_app = google.appengine.api.wrap_wsgi_app(app.wsgi_app)
~~~

Then deploy your app as usual, with `gcloud beta app deploy` (currently only the Beta version has the capability to enable these APIs). The following modules are available:
- `google.appengine.api.app_identity`
- `google.appengine.api.background_thread`
- `google.appengine.api.blobstore`
- `google.appengine.api.capabilities`
- `google.appengine.api.croninfo`
- `google.appengine.api.dispatchinfo`
- `google.appengine.api.images`
- `google.appengine.api.mail`
- `google.appengine.api.memcache`
- `google.appengine.api.modules`
- `google.appengine.api.oauth`
- `google.appengine.api.runtime`
- `google.appengine.api.taskqueue`
- `google.appengine.api.urlfetch`
- `google.appengine.api.users`
- `google.appengine.ext.blobstore`
- `google.appengine.ext.db`
- `google.appengine.ext.gql`
- `google.appengine.ext.key_range`
- `google.appengine.ext.ndb`
- `google.appengine.ext.testbed`

## Using the development version of the SDK

To install the code from the `main` branch on GitHub rather than the latest
version published to PyPI, put this in your `requirements.txt` file instead of
`appengine-python-standard`:

`https://github.com/GoogleCloudPlatform/appengine-python-standard/archive/main.tar.gz`
