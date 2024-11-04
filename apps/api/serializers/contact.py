from rest_framework import serializers
from ..models.contact import ContactModel

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactModel
        fields = ['name', 'email', 'phone', 'message']
