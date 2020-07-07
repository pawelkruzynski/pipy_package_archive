
# Pypi package archive

The application downloads information about packages from 
https://pypi.org/rss/packages.xml once a day.

After downloading, the information are stored in db as 
well as in elasticsearch.

Application frontend allows browsing paginated results 
collected in es. You can find following package info:
- author, 
- author's email, 
- description,
- package name, 
- keywords
- latest version
- maintainers' info

You can also filter results.

## Running project:

`docker-compose up --build -d`

After start the application will download first batch of 
pypi packages and will continue doing it every 24 hours. 
If you can't see any results, wait upto 1 minute and the 
celery task will fetch data. 

## Pagination

The pagination can be set in environment variable. To 
change it, modify  `FRONT_PAGINATION` variable in 
`environmemt` file and restart following docker 
containers:
- optimo-web
- optimo-celery
- optimo-celery-beat

## Admin panel

The admin panel is not available in the application.

## Rebuilding es index
To rebuild index in case of elasticsearch failure, run 
following command inside optimo-web container:

`python manage.py search_index –rebuild`

It will be recreated from project's database. 

## OS dependency

The application is intended to be OS independent. Just 
use docker-compose on your OS to run.

## Presentation in web browser

`http://0.0.0.0:8080/`

## API

`http://0.0.0.0:8080/api/v1/package/`

To search through the API, add parameters corresponding 
to the columns from the browser view. Optionally add `page` 
attribute to paginate. ie:

`http://0.0.0.0:8080/api/v1/package/?title__contains=djang&page=1`

 