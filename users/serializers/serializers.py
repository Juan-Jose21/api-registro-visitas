from rest_framework import serializers
from ..models.models import Usuario, Visita, Ingreso


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'password_hash', 'created_at', 'updated_at']


class VisitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visita
        fields = ['id', 'nombre_completo', 'cedula', 'foto_anverso', 'foto_reverso', 'created_at', 'updated_at']


class IngresoSerializer(serializers.ModelSerializer):
    visita = VisitaSerializer(read_only=True)
    visita_id = serializers.PrimaryKeyRelatedField(queryset=Visita.objects.all(), write_only=True, source='visita')

    class Meta:
        model = Ingreso
        fields = ['id', 'visita', 'visita_id', 'fecha_entrada', 'hora_entrada', 'created_at']
