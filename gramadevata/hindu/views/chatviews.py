from rest_framework .response import Response
from ..serializers.chat_serializer import ChatSerializer,ChatSerializer1
from ..models.chat import ChatModel,Temple,Register,Village
from rest_framework import viewsets,status
from django.utils.timesince import timesince
from rest_framework.permissions import IsAuthenticated



class ChatViews(viewsets.ModelViewSet):
    queryset = ChatModel.objects.all()
    serializer_class = ChatSerializer

    permission_classes = []
    
    def get_permissions(self):
        if self.request.method in ['GET', 'POST', 'PUT']:
            return [IsAuthenticated()]
        return super().get_permissions()




    def list(self, request):
        filter_kwargs = {}

        # Build filters from query parameters
        for key, value in request.query_params.items():
            filter_kwargs[key] = value

        try:
            # Extract filters
            temple_id = filter_kwargs.get('temple', None)
            village_id = filter_kwargs.get('village', None)

            # Filter for temple-specific messages
            temple_messages = ChatModel.objects.filter(**filter_kwargs, chat_entity_type='temple').order_by('created_at')

            # Query for admin messages for temples
            admin_temple_messages = ChatModel.objects.filter(
                chat_user_type='admin',
                chat_entity_type='temple'
            ).order_by('created_at')

            # Combine temple-specific and admin messages
            combined_temple_queryset = (temple_messages | admin_temple_messages).distinct().order_by('created_at')

            # Filter for village-specific messages
            village_messages = ChatModel.objects.filter(**filter_kwargs, chat_entity_type='village').order_by('created_at')

            # Query for admin messages for villages
            admin_village_messages = ChatModel.objects.filter(
                chat_user_type='admin',
                chat_entity_type='village'
            ).order_by('created_at')

            # Combine village-specific and admin messages
            combined_village_queryset = (village_messages | admin_village_messages).distinct().order_by('created_at')

            # Logic to include messages from any temple or village
            if temple_id:
                # Return temple-related messages, including any from the temple
                temple_queryset = combined_temple_queryset
                if not temple_queryset.exists():
                    return Response({
                        'message': 'Data not found for temple',
                        'status': 404
                    }, status=status.HTTP_404_NOT_FOUND)

                # Update 'posted_time_ago' for display (without saving to the database)
                for chat in temple_queryset:
                    if chat.created_at:
                        chat.posted_time_ago = f"{timesince(chat.created_at)} ago"

                # Serialize the data
                serialized_data = ChatSerializer1(temple_queryset, many=True)
                return Response({'temple_messages': serialized_data.data}, status=status.HTTP_200_OK)

            elif village_id:
                # Return village-related messages, including any from the village
                village_queryset = combined_village_queryset
                if not village_queryset.exists():
                    return Response({
                        'message': 'Data not found for village',
                        'status': 404
                    }, status=status.HTTP_404_NOT_FOUND)

                # Update 'posted_time_ago' for display (without saving to the database)
                for chat in village_queryset:
                    if chat.created_at:
                        chat.posted_time_ago = f"{timesince(chat.created_at)} ago"

                # Serialize the data
                serialized_data = ChatSerializer1(village_queryset, many=True)
                return Response({'village_messages': serialized_data.data}, status=status.HTTP_200_OK)

            else:
                # Return messages for any temple or village if no specific filter is provided
                all_temple_messages = ChatModel.objects.filter(chat_entity_type='temple').order_by('created_at')
                all_village_messages = ChatModel.objects.filter(chat_entity_type='village').order_by('created_at')

                # Combine both temple and village messages
                all_messages = (all_temple_messages | all_village_messages).distinct().order_by('created_at')

                if not all_messages.exists():
                    return Response({
                        'message': 'No messages found',
                        'status': 404
                    }, status=status.HTTP_404_NOT_FOUND)

                # Update 'posted_time_ago' for display (without saving to the database)
                for chat in all_messages:
                    if chat.created_at:
                        chat.posted_time_ago = f"{timesince(chat.created_at)} ago"

                # Serialize the data
                serialized_data = ChatSerializer1(all_messages, many=True)
                return Response({'all_messages': serialized_data.data}, status=status.HTTP_200_OK)

        except ChatModel.DoesNotExist:
            return Response({
                'message': 'Objects not found',
                'status': 404
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            # Generic error handler
            return Response({
                'message': f"An error occurred: {str(e)}",
                'status': 500
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





    def create(self, request):
        user = request.user

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            temple = data.get('temple')  # Specified temple
            village = data.get('village')  # Specified village
            message_content = data.get('message')  # Message content

            # Get user details
            email = getattr(request.user, 'email', None)
            contact_number = getattr(request.user, 'contact_number', None)

            # Find the Register instance
            register_instance = None
            if email:
                register_instance = Register.objects.filter(email=email).first()
            elif contact_number:
                register_instance = Register.objects.filter(contact_number=contact_number).first()

            # If no user found, return error
            if not register_instance:
                return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

            # Determine chat_user_type based on is_staff value
            chat_user_type = 'admin' if register_instance.is_staff else 'user'

            # Determine chat_entity_type based on temple or village ID
            chat_entity_type = None
            if temple:
                chat_entity_type = 'temple'
            elif village:
                chat_entity_type = 'village'

            # Batch size for bulk create
            batch_size = 500  

            # For staff (admin) users, message should be broadcasted to all temples and/or villages
            if register_instance.is_staff:
                if temple:
                    # Store a single message for the specified temple
                    existing_chat = ChatModel.objects.filter(temple=temple, message=message_content).first()
                    if not existing_chat:
                        chat_message = ChatModel.objects.create(
                            user=user,
                            temple=temple,
                            message=message_content,
                            chat_user_type=chat_user_type,
                            chat_entity_type=chat_entity_type
                        )
                        # Link this message to all temples
                        all_temples = Temple.objects.all()
                        

                    return Response({"message": "Message broadcasted to all temples."}, status=status.HTTP_201_CREATED)

                if village:
                    # Store a single message for the specified village
                    existing_chat = ChatModel.objects.filter(village=village, message=message_content).first()
                    if not existing_chat:
                        chat_message = ChatModel.objects.create(
                            user=user,
                            village=village,
                            message=message_content,
                            chat_user_type=chat_user_type,
                            chat_entity_type=chat_entity_type
                        )
                        # Link this message to all villages
                        all_villages = Village.objects.all()
                        
                    return Response({"message": "Message broadcasted to all villages."}, status=status.HTTP_201_CREATED)

            else:
                # For non-staff users, save the message for the specified temple or village
                if temple:
                    # Save the message for the specified temple
                    serializer.save(user=user, temple=temple, chat_user_type=chat_user_type, chat_entity_type=chat_entity_type)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)

                elif village:
                    # Save the message for the specified village (similar to temple)
                    serializer.save(user=user, village=village, chat_user_type=chat_user_type, chat_entity_type=chat_entity_type)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)

                else:
                    return Response({"error": "You must specify a temple or village to send a message."}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
