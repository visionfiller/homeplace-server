"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View
from homeplacereports.views.helpers import dict_fetch_all


class SwapperPropertyList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # TODO: Write a query to get all games along with the gamer first name, last name, and id
            db_cursor.execute("""
            SELECT p.id , p.address, p.square_footage, a.neighborhood, pt.name, p.owner_id, au.first_name  || ' ' || au.last_name as full_name
            FROM homeplaceapi_property as p 
            JOIN homeplaceapi_swapper as s ON s.id = p.owner_id
            JOIN homeplaceapi_area as a ON a.id = p.area_id
            JOIN homeplaceapi_propertytype as pt ON pt.id = p.property_type_id
            JOIN auth_user as au ON au.id = s.user_id
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)

            # Take the flat data from the dataset, and build the
            # following data structure for each gamer.
            # This will be the structure of the games_by_user list:
            #
            # [
            #   {
            #     "id": 1,
            #     "full_name": "Admina Straytor",
            #     "games": [
            #       {
            #         "id": 1,
            #         "title": "Foo",
            #         "maker": "Bar Games",
            #         "skill_level": 3,
            #         "number_of_players": 4,
            #         "game_type_id": 2
            #       },
            #       {
            #         "id": 2,
            #         "title": "Foo 2",
            #         "maker": "Bar Games 2",
            #         "skill_level": 3,
            #         "number_of_players": 4,
            #         "game_type_id": 2
            #       }
            #     ]
            #   },
            # ]

            properties_by_swapper = []

            for row in dataset:
                # TODO: Create a dictionary called game that includes
                # the name, description, number_of_players, maker,
                # game_type_id, and skill_level from the row dictionary
                property_ = {
                    'id': row['id'],
                    'address': row['address'],
                    'square_footage': row['square_footage'],
                    'neighborhood': row['neighborhood'],
                    'property_type': row['name'],
                    'owner': row['owner_id']
                }

                # See if the gamer has been added to the games_by_user list already
                swapper_dict = None
                for swapper_property in properties_by_swapper:
                    if swapper_property['owner_id'] == row['owner_id']:
                        swapper_dict = swapper_property

                if swapper_dict:
                    # If the user_dict is already in the games_by_user list, append the game to the games list
                    swapper_dict['property_'].append(property_)
                else:
                    # If the user is not on the games_by_user list, create and add the user to the list
                    properties_by_swapper.append({
                        "owner_id": row['owner_id'],
                        "full_name": row['full_name'],
                        "property_": [property_]
                    })

        # The template string must match the file name of the html template
        template = 'swappers/swapper_properties_list.html'

        # The context will be a dictionary that the template can access to show data
        context = {
            "swapper_properties_list": properties_by_swapper
        }

        return render(request, template, context)
