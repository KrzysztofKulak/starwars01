# starwars archive
This app consumes StarWars API swapi.dev.
It fetches all the character information and stores the data from the given moment in time in form of csv files.

Main page is accessible at the `/collections` url.

# running locally

required: `python 3.10` (app is using modern typing notation and won't work on older versions), `pip`

in terminal in project's root directory run

```
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

App will be accessible on http://localhost:8000/collections/

# fetching

To fetch copy of characters data press `fetch` button on main page.

# value count

App allows counting occurrences of the combinations of values in any given fields (or a single field).
Unfortunately there's no GUI for selecting specific fields. 

To do that go to:
`/collections/[collection_id]/count?columns=[comma_separated_column_names]`

Example:
`/collections/[collection_id]/count?columns=gender,hair_color` (the most popular `hair_color` for both males and females is `none`!)

If no columns are provided `homeworld` and `birth_year` are used as defaults.

# improvement ideas:

There's a number of improvement ideas that could be introduced written down in comments in the code itself.
To search for them in the code search for `IMPROVEMENT IDEA`.

Ideas not listed inside of the codebase:

- adding GUI for choosing columns in `/count` view.
- decouple specific urls from templates. 
- improving logging and general observability.
- adding linters, package version managers and similiar.

# additional observation:

At first I wasn't sure if the majority of the planets won't be "unpopulated" (won't have any characters assinged) 
and tried lazly fetching only planets that are needed and just reusing them when they reappeared for another character. 
I was wondering if that will be a net gain for url calls efficiency, since multiple pages have to be called for getting 
all planets' pages anyway. I was wrong, time after prefetching all planets at the beginning of character fetching turned 
out to be more than 3 times shorter (around 3 seconds instead of 9 on my connection). I still believe, however, that lazy
prefetching approach could be useful if the data had shown different tendencies or if fetching only some characters 
was an option we'd like to provide. 