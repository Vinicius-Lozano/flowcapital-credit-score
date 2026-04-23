from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Usuario
from .validators import validar_cpf


class RegistrarSerializer(serializers.Serializer):
    cpf = serializers.CharField()
    senha = serializers.CharField(write_only=True)
    confirmar_senha = serializers.CharField(write_only=True)

    def validate_cpf(self, value):
        cpf = ''.join(filter(str.isdigit, value))
        if not validar_cpf(cpf):
            raise serializers.ValidationError('CPF inválido.')
        if Usuario.objects.filter(cpf=cpf).exists():
            raise serializers.ValidationError('CPF já cadastrado.')
        return cpf

    def validate_senha(self, value):
        validate_password(value)
        return value

    def validate(self, attrs):
        if attrs['senha'] != attrs['confirmar_senha']:
            raise serializers.ValidationError({'confirmar_senha': 'As senhas não conferem.'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirmar_senha')
        return Usuario.objects.create_user(
            cpf=validated_data['cpf'],
            password=validated_data['senha'],
        )


class LoginSerializer(serializers.Serializer):
    cpf = serializers.CharField()
    senha = serializers.CharField(write_only=True)

    def validate(self, attrs):
        cpf = ''.join(filter(str.isdigit, attrs.get('cpf', '')))
        senha = attrs.get('senha')
        user = authenticate(username=cpf, password=senha)
        if not user:
            raise serializers.ValidationError('CPF ou senha inválidos.')
        if not user.is_active:
            raise serializers.ValidationError('Conta desativada.')
        attrs['user'] = user
        return attrs
