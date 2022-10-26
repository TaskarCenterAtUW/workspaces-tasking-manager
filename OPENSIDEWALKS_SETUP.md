## Changelog

To get the OpenSidewalks instance running via docker, several changes have been
made to the repository. These are stored on the opensidewalks branch.

- Changes are tracked in `opensidewalks` branch. Secrets are stored in version
control but should not be - need to make strategy to hide them.

## Configuration

This repo has been set up so that configuration of the application happens
entirely via an env file, specifically `tasking-manager.env`. This file is
deliberately kept out of version control. To begin configuring the application,
copy `example.env` to `tasking-manager.env` in the root directory of this
repository, then input your settings.

Note: only a subset of the environment variables configured in
`tasking-manager.env` will get passed on to the `frontend`:

- `TM_APP_API_URL`: The URL for the API, this should be the public URL and should
include the protocol, i.e. http://HOST or https://HOST.
- `TM_IMPORT_MAX_FILESIZE`: A project may fail When using a custom GeoJSON to
create task polygons because the default maximum filesize is set very low. This
will set the maximum size in bytes (an integer).
- `TM_CONSUMER_KEY`: This is an OAuth consumer key from OpenStreetMap
- `TM_CONSUMER_SECRET`: This is an OAuth consumer secret from OpenStreetMap
- `TM_ORG_LOGO`: The URL to a custom logo.

Other environment variables defined in `tasking-manager.env` will still be used
to configure the back end of the application.

## Deploying
0. Create a backup of the database (just in case).
1. Create `tasking_manager.env` from `example.env`.
2. Run `docker-compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.opensidewalks.yml pull`
to download all images on which the services depend.
3. Run `docker-compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.opensidewalks.yml --env-file=tasking-manager.env build backend migration frontend`
to build all images on which the services depend. Note the use of
`--env-file=tasking-manager.env` - important settings won't reach the front end
build if this flag isn't used.
4. Run `docker-compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.opensidewalks.yml up -d postgresql`
to start the postgreSQL server.
5. Run `docker-compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.opensidewalks.yml run migration python manage.py db upgrade`
to run any database schema changes that have occurred since the last release.
6. Run `docker-compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.opensidewalks.yml --env-file=tasking-manager.env up -d`
to start all services. Wait a few seconds for everything to finish
initialization. Note the use of `--env-file=tasking.manager.env` again: the
proxy (and HTTPS) won't work without this flag.
7. Visit the host (possibly tasks.opensidewalks.com) with a browser. You did
it!
