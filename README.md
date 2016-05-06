## Quimby

![Quimby](https://i.imgur.com/9H5GiTJ.jpg)

Microservice to allow users to easily and securely send each other secrets over a possibly untrusted
network. Fill in a secret (password, secret key, love letter) and hit the button. A random one-time
URL is generated and provided to the user. Send this link to anyone and when they open it the secret
will be visible just that one time, being destroyed on the service after viewing.

Although it doesn't prevent people from intercepting the secrets, the receiving party will be aware
of the fact that the secret was intercepted and can act accordingly.

Secrets are stored in memory, so they will not survive a restart of the application.

### Requirements

* Python 3
* An upstream load balancer with SSL termination

### Deployment

This application is designed to be distributed as a Docker container, and accessed via a load
balancer that provides SSL termination. It can be run outside a container as well, if desired.

### Original Project

This project was originally forked from https://github.com/Achiel/SecretSexChange with some major
changes:

* Modified for use in a Docker container
* Removed the Flash applet
* Switched from Redis to an in-memory datastore so the secrets won't be written to disk
* Force all connections to HTTPS
* Theme support

### Development Mode

The [Flask SSLify module](https://github.com/kennethreitz/flask-sslify) ensures that all incoming
requests are redirected to HTTPS, which is somewhat important for this type of application. This is
disabled when running in debug mode. To enable debug mode, pass the following environment variable:

```
DEBUG=True
```

### Themes

There are currently two themes available, `light` and `dark`. You can choose which one to use with
the following environment variable:

```
THEME=dark
```
