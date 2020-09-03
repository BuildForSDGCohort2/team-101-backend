# Deploying Django to Heroku With Docker

Uses the Container Registry approach for Heroku deployments.

## Want to learn how to build this?



## Want to use this project?

### Development

Run locally:

```sh
$ docker build -t web:latest .
$ docker run -d --name data-africa -e "PORT=8765" -e "DEBUG=1" -p 8007:8765 web:latest
```

Verify [http://localhost:8007](http://localhost:8007) works as expected:

```json
{
  "ping": "pong!"
}
```

Stop then remove the running container once done:

```sh
$ docker stop data-africa
$ docker rm data-africa
```

### Production

```sh
$ docker build -t registry.heroku.com/frozen-basin-50948/web .

$ docker push registry.heroku.com/frozen-basin-50948/web

$ heroku container:release -a frozen-basin-50948 web
```
