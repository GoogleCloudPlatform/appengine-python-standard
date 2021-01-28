# Google App Engine Python 3 Standard Environment API library (alpha)

This is an alpha release of the App Engine SDK for Python 3.  It provides access
to various API endpoints that were previously only available on the Python 2.7
runtime.

## Using the SDK

In your `requirements.txt` file, add the following:

`appengine-python-standard>=0.0.1a`

In your app's `app.yaml`, add the following:

`app_engine_apis: true`

Then deploy your app as usual, with `gcloud app deploy`.  The following modules
are available:

- `google.appengine.api.capabilities`
- `google.appengine.api.memcache`
- `google.appengine.api.urlfetch`
- `google.appengine.api.users`
- `google.appengine.ext.db`
- `google.appengine.ext.ndb`

## Using the development version of the SDK

To install the code from the `main` branch on GitHub rather than the latest
version published to PyPI, put this in your `requirements.txt` file instead of
`appengine-python-standard`:

`https://github.com/GoogleCloudPlatform/appengine-python-standard/archive/main.tar.gz`
