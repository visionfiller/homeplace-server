import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from homeplaceapi.models import Property, Swapper, Area, PropertyType, Reservation


class PropertyTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['properties','areas', 'cities','propertytypes','ratings', 'reservations','swappers', 'users', 'tokens']

    def setUp(self):
       
        self.user = User.objects.first()
        token = Token.objects.get(user=self.user)
        self.swapper = Swapper.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_property(self):
        """
        Ensure the user can create a new property.
        """
        # Define the endpoint in the API to which
        # the request will be sent
        url = "/properties"

        # Define the request body
        owner= self.swapper
        area = Area.objects.first()
        property_type= PropertyType.objects.first()
        data = {
                "owner": owner.id,
                "area": area.id,
                "property_type": property_type.id,
                "address" : "100 test way",
                "image": "image.jpg",
                "description": "a beautiful test home",
                "bedrooms":2,
                "bathrooms": 2, 
                "yard": True,
                "pool": False,
                "square_footage": 1000
              
        }

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["address"], "100 test way")
        self.assertEqual(json_response["square_footage"], 1000)
        self.assertEqual(json_response["area"], {'id': 1, 'neighborhood': 'Green Hills', 'city': 1})
        self.assertEqual(json_response["owner"], {'id': 1, 'full_name': 'Vision Filler'})
        self.assertEqual(json_response["property_type"], {'id': 1, 'name': 'Single Family Home'})
        self.assertEqual(json_response["bathrooms"], 2)

    def test_edit_property(self):

        url = "/properties"
        owner= self.swapper
        property_type= PropertyType.objects.last()
        property_= Property.objects.get(owner=owner)
        data2 = {
            "area": property_.area.id,
            "property_type": property_type.id,
            "address" : "300 test way",
            "image": property_.image,
            "description": property_.description,
            "bedrooms":property_.bedrooms,
            "bathrooms": property_.bathrooms, 
            "yard": False,
            "pool": property_.pool,
            "square_footage": property_.square_footage
    }
        response = self.client.put(f'{url}/{property_.id}', data2, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        property_updated = Property.objects.get(pk=property_.id)
        self.assertEqual(property_updated.address, data2['address'])
        self.assertEqual(property_updated.property_type.id, data2['property_type'])
        self.assertEqual(property_updated.yard, data2['yard'])

    def test_get_all_properties(self):
        response = self.client.get('/properties')
        # checks to make sure a user that is not logged on can still get all properties
        unauthorizedclient = APIClient()
        response2 = unauthorizedclient.get('/properties')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Property.objects.count())
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response2.data), Property.objects.count())


    def test_delete_property(self):
   
        property_ = Property.objects.get(owner=self.swapper)
        response = self.client.delete(f'/properties/{property_.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    # user cannot delete property that they didnt create
        notowner=Swapper.objects.last()
        secondproperty_ = Property.objects.get(owner=notowner)
        response = self.client.delete(f'/properties/{secondproperty_.id}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_make_reservation(self):
       
        property_ = Property.objects.first()
        data ={
            "start_date" : "2023-07-02",
            "end_date": "2023-08-01"
        }
        response = self.client.post(f'/properties/{property_.id}/make_reservation',data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        reservation= Reservation.objects.get(swapper=self.swapper)
        response2 = self.client.get(f'/reservations/{reservation.id}')
        json_response = json.loads(response2.content)
        self.assertEqual(json_response['swapper']['id'], self.swapper.id)
def test_cancel_reservation(self):
        property_ = Property.objects.first()
        swapper = self.swapper
        data ={
            "start_date" : "2023-07-02",
            "end_date": "2023-08-01"
        }
        response = self.client.post(f'/properties/{property_.id}/make_reservation',data, format='json')
        response2 = self.client.delete(f'/properties/{property_.id}/cancel_reservation')
        self.assertEqual(response2.status_code, status.HTTP_204_NO_CONTENT)
        
