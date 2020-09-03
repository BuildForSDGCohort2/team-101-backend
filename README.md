# Deploying Django to Heroku With Docker

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/08707ebc64ea46789de0a89b55856a05)](https://app.codacy.com/gh/BuildForSDGCohort2/team-101-backend?utm_source=github.com&utm_medium=referral&utm_content=BuildForSDGCohort2/team-101-backend&utm_campaign=Badge_Grade_Settings)

Uses the Container Registry approach for Heroku deployments.

## Want to learn how to build this

## Want to use this project

### Development

Run locally:

```sh
docker build -t web:latest .
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
docker stop data-africa
$ docker rm data-africa
```

### Production

$ docker build -t registry.heroku.com/frozen-basin-50948/web .

$ docker push registry.heroku.com/frozen-basin-50948/web

$ heroku container:release -a frozen-basin-50948 web
