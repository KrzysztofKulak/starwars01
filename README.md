# starwars archive
This app consumes StarWars API swapi.dev.
It fetches all the character informations and stores the data from the given moment in time in form of csv files.

Main page is accessible at the `/collections` url.

# fetching

To fetch copy of characters data press `fetch` button on main page.

# value count

App allows to count occurences of the combinations of values in any given fields (or a single field).
Unfortunatelly there's no GUI for selecting specific fields. 

To do that go to:
`/collections/[collection_id]/count?columns=[comma_separated_column_names]`

example:
`/collections/[collection_id]/count?columns=homeworld,hair_color`

If no colums are provided `homeworld` and `birth_year` are used as defaults.

# improvement ideas:

There's a number of improvement ideas that could be introduced written down in comments in the code itself.
To search for them in the code search for `IMPROVEMENT IDEA`.

Ideas not listed inside of the codebase:

- adding GUI for choosing columns in `/count` view.
- decouple specific urls from templates. 
- improving logging and general observability.