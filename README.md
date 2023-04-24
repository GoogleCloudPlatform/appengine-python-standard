# Google App Engine bundled services SDK for Python 3

This is a release of the App Engine services SDK for Python 3.  It provides access to various services and API endpoints that were previously only available on the Python 2.7 runtime.

See the [documentation](https://cloud.google.com/appengine/docs/standard/python3/services/access) to learn more about using this SDK, and learn more about it in [this product announcement](http://cloud.google.com/blog/products/serverless/support-for-app-engine-services-in-second-generation-runtimes) (Fall 2021).

Additional examples (Datastore [NDB], Task Queues [push tasks], Memcache) can be found in the [App Engine migration repo](https://github.com/googlecodelabs/migrate-python2-appengine). (Specifically look for samples whose folders have a `b` but where the Python 2 equivalent folder does **not** have an `a`, meaning this SDK is required, e.g., Modules 1 [`mod1` and `mod1b`], 7, 12, etc.)


## Using the SDK

In your `requirements.txt` file, add the following:

`appengine-python-standard>=1.0.0`

To use a pre-release version (Eg. `1.0.1-rc1`), modify the above line to `appengine-python-standard>=[insert_version]` (Eg. `appengine-python-standard>=1.0.1-rc1`).

In your app's `app.yaml`, add the following:

`app_engine_apis: true`

In your `main.py`, import `google.appengine.api.wrap_wsgi_app()` and call it on your
WSGI app object.

Example for a standard WSGI app:

    import google.appengine.api

    def app(environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/plain')])
        yield b'Hello world!\n'

    app = google.appengine.api.wrap_wsgi_app(app)

Example for a Flask app:

    import google.appengine.api
    from flask import Flask, request

    app = Flask(__name__)
    app.wsgi_app = google.appengine.api.wrap_wsgi_app(app.wsgi_app)

Then deploy your app as usual, with `gcloud app deploy`. The following modules are available:

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
- `google.appengine.api.search`
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
