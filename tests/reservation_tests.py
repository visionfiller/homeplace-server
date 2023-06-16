import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from homeplaceapi.models import Property, Swapper, Area, PropertyType, Reservation


class ReservationTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['properties','areas', 'cities','propertytypes','ratings', 'reservations','swappers', 'users', 'tokens']

    def setUp(self):
       
        self.user = User.objects.first()
        token = Token.objects.get(user=self.user)
        self.swapper = Swapper.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")


    def test_get_all_reservations(self):
        response = self.client.get('/reservations')
   
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Reservation.objects.count())
       

    def test_approve_reservation(self):
        owner = Swapper.objects.get(user=self.user)
        reservation_ = Reservation.objects.filter(property__owner=owner).first()
        response = self.client.put(f'/reservations/{reservation_.id}/approve')
   
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        reservation_updated = Reservation.objects.get(pk=reservation_.id)
        self.assertEqual(reservation_updated.status, "Approved")
        
    def test_deny_reservation(self):
        owner = Swapper.objects.get(user=self.user)
        reservation_ = Reservation.objects.filter(property__owner=owner).first()
        response = self.client.put(f'/reservations/{reservation_.id}/deny')
   
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        reservation_updated = Reservation.objects.get(pk=reservation_.id)
        self.assertEqual(reservation_updated.status, "Denied")