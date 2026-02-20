from rest_framework import viewsets
from ..serializers import MemberSerializer,MemberSerializer1
from ..models import MemberModel
from rest_framework .response import Response
from rest_framework.permissions import IsAuthenticated



class MemberView(viewsets.ModelViewSet):
    queryset = MemberModel.objects.all()
    # serializer_class = MemberSerializer

    permission_classes = []
    
    def get_permissions(self):
        if self.request.method in ['GET', 'POST', 'PUT']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def create(self,request):
        serializer = MemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        member = serializer.save()
        return Response({
            "message":"you added member in your village",
            "data":MemberSerializer1(member).data,
            "status":200
            })

    
    def list(self, request):  
        queryset = MemberModel.objects.all()
        serializer = MemberSerializer1(queryset, many=True)
        return Response({
            "message": "data get successfully",
            "data": serializer.data
        })
    # def retrieve(self, request, pk=None):  
    #     instance = self.get_object()
    #     serializer = MemberSerializer(instance)  
    #     return Response({
    #         "message": "retrieved successfully",
    #         "data": serializer.data
    #     })
    def retrieve(self, request, pk=None):  
        instance = self.get_object()
        serializer = MemberSerializer1(instance)  
        return Response({
            "message": "retrieved successfully",
            "data": serializer.data
        })

    def update(self, request, pk=None):
        instance = self.get_object()
        serializer = MemberSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_instance = serializer.save()
        return Response({
            "message": "updated successfully",
            "data": MemberSerializer1(updated_instance).data
        })
    
    

    def destroy(self, request, pk=None):
        instance = self.get_object()
        instance.status = 'inactive'  # Marking as inactive instead of actually deleting
        instance.save()
        return Response({"message": "soft deleted successfully"})