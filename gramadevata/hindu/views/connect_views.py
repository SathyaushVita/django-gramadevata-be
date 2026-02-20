from rest_framework import viewsets
from ..models import ConnectModel 
from ..serializers import ConnectModelSerializer,ConnectModelSerializer1 
from rest_framework .response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from ..models.register import Register
from ..enums.member_type_enum import MemberType
from rest_framework import status


class ConnectView(viewsets.ModelViewSet):
    queryset = ConnectModel.objects.all()
    serializer_class = ConnectModelSerializer

    permission_classes = []
    
    def get_permissions(self):
        if self.request.method in ['GET', 'POST', 'PUT']:
            return [IsAuthenticated()]
        return super().get_permissions()



    # def list(self, request):
        
    #     filter_kwargs = {}

    #     for key, value in request.query_params.items():
    #         filter_kwargs[key] = value

        

    #     try:
    #         queryset = ConnectModel.objects.filter(**filter_kwargs)
    #         villagedata = queryset.filter(temple=None)
    #         templedata = queryset.filter(village=None)

    #         village_count = villagedata.count()
    #         temple_count = templedata.count()
            
    #         if not queryset.exists():
    #             return Response({
    #                 'message': 'Data not found',
    #                 'status': 404
    #             })

    #         village_data = ConnectModelSerializer1(villagedata, many=True)
    #         temple_data = ConnectModelSerializer1(templedata, many=True)
    #         return Response({
    #             'village_data': village_count,
    #             "village":village_data.data,
    #             'temple_count': temple_count,
    #             "temple":temple_data.data
    #                          })

    #     except ConnectModel.DoesNotExist:
    #         return Response({
    #             'message': 'Objects not found',
    #             'status': 404
    #         })

    def list(self, request):

        filter_kwargs = dict(request.query_params)

        queryset = (
            ConnectModel.objects
            .filter(**filter_kwargs)
            .select_related('village', 'temple', 'user')
        )

        if not queryset.exists():
            return Response({
                'message': 'Data not found',
                'status': 404
            })

        villagedata = queryset.filter(temple__isnull=True)
        templedata = queryset.filter(village__isnull=True)

        village_data = ConnectModelSerializer1(villagedata, many=True).data
        temple_data = ConnectModelSerializer1(templedata, many=True).data

        return Response({
            'village_data': len(village_data),
            "village": village_data,
            'temple_count': len(temple_data),
            "temple": temple_data
        })

        


    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data.get('user')
            village_data = serializer.validated_data.get('village')
            temple_data = serializer.validated_data.get('temple')

            # If connecting to a village, enforce the 10-village limit
            if village_data:
                existing_village_connections = ConnectModel.objects.filter(user=user_data, village__isnull=False).count()
                if existing_village_connections >= 10:
                    return Response({"error": "You can connect to a maximum of 10 villages."}, status=400)

                # Check if the user is already connected to the specific village
                if ConnectModel.objects.filter(user=user_data, village=village_data).exists():
                    return Response({"error": "You are already connected to this village."}, status=400)

            # Check if the user is already connected to the specific temple
            if temple_data and ConnectModel.objects.filter(user=user_data, temple=temple_data).exists():
                return Response({"error": "You are already connected to this temple."}, status=400)

            # Save the serializer to create the connection
            serializer.save()

            # After saving, retrieve the saved instance
            saved_instance = serializer.instance
            userId = saved_instance.user.id
            connected_as = saved_instance.connected_as

            # Check if the user is connected as 'PUJARI'
            if connected_as == 'PUJARI':
                try:
                    userdata = Register.objects.get(id=userId)
                    userdata.type = MemberType.PUJARI.value
                    userdata.save()
                except Register.DoesNotExist:
                    return Response({"error": "User not found."}, status=404)

            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
        






    def destroy(self, request, pk=None):
        connection = get_object_or_404(ConnectModel, pk=pk)

        # Ensure that only the owner (connected user) can delete
        if connection.user != request.user:
            return Response({"error": "You are not authorized to delete this connection."}, status=status.HTTP_403_FORBIDDEN)

        connection.delete()
        return Response({"message": "Connection deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    

   



