from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers, status
from homeplaceapi.models import PaymentType, Reservation, Property, Swapper
from homeplaceapi.serializers import ReservationSerializer


class ReservationView(ViewSet):
    """HomePlace Reservation View"""

    def retrieve(self, request, pk):
        """Handle GET requests for single PaymentType
        
        Returns:
            Response -- JSON serialized PaymentType
        """
        try:
            reservation = Reservation.objects.get(pk=pk)
            serializer = ReservationSerializer(reservation)
            return Response(serializer.data)
        except Reservation.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all properties

        Returns:
            Response -- JSON serialized list of properties
        """
        reservations = Reservation.objects.all()
        swapper_id = request.query_params.get('swapper', None)
        property_id = request.query_params.get('property', None)
        swapper_property=request.query_params.get('swapper_property', None)

        if swapper_id is not None:
            reservations = reservations.filter(swapper=swapper_id)
        if property_id is not None:
            reservations = reservations.filter(property=property_id)
        if swapper_property is not None:
            reservations = reservations.filter(swapper__property=swapper_property)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)
    def destroy(self, request, pk):
            """delete property"""
            
            try:
                reservation = Reservation.objects.get(pk=pk)
                reservation.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            except Reservation.DoesNotExist as ex:
                    return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        
    @action(methods=['get'], detail=False)       
    def my_swaps(self, request):
        """find the swaps that the user signed has been sent"""
        
        properties = Property.objects.filter(owner__user=request.auth.user)
        swaps = Reservation.objects.filter(property__in=properties)
        status_id = request.query_params.get('status', None)

        if status_id is not None:
            swaps = swaps.filter(status__icontains = status_id)

        serializer = ReservationSerializer(swaps, many=True)
        return Response(serializer.data)
    @action(methods=['put'], detail=True)       
    def approve(self, request, pk):
        """approve a submitted request"""
        try:
            swapper = Swapper.objects.get(user=request.auth.user)
            reservation= Reservation.objects.get(pk=pk, property__owner = swapper)
            reservation.status = "Approved"
            reservation.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Reservation.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['put'], detail=True)       
    def deny(self, request, pk):
        """approve a submitted request"""
        try:
            swapper = Swapper.objects.get(user=request.auth.user)
            reservation= Reservation.objects.get(pk=pk, property__owner = swapper)
            reservation.status = "Denied"
            reservation.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Reservation.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    @action(methods=['put'], detail=True)       
    def complete(self, request, pk):
        """approve a submitted request"""
        try:
            swapper = Swapper.objects.get(user=request.auth.user)
            reservation= Reservation.objects.get(pk=pk, property__owner = swapper)
            reservation.status = "Denied"
            reservation.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Reservation.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        