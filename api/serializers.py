from rest_framework import serializers
from .models import *
from django.db.models import Q
from django.conf import settings

# TODO: Implement token auth


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ('password',)
        depth = 1


class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, label="Username")
    email = serializers.EmailField(required=True, label="Email Address")
    password = serializers.CharField(required=True, label="Password", style={'input_type': 'password'})
    #password_2 = serializers.CharField(required=True, label="Confirm Password", style={'input_type': 'password'})
    first_name = serializers.CharField(required=True, label="First Name")
    last_name = serializers.CharField(required=True, label="Last Name")
    school_name = serializers.CharField(required=True, label="School Name")
    logo = serializers.ImageField(max_length=100, label="Logo")
    description = serializers.CharField(required=True, label="Description")
    address = serializers.CharField(required=True, label="Address")
    tel = serializers.IntegerField(required=True, label="Phone Number")
    region = serializers.CharField(required=True, label="Region")
    #approval = serializers.IntegerField(required=True, label="Approval Number")
    bvn = serializers.CharField(required=True, label="BVN")
    account_number = serializers.IntegerField(required=True, label="Account Number")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'school_name',
                  'description', 'logo', 'address', 'tel', 'region', 'bvn', 'account_number']

        def validate_email(self, value):
            if CustomUser.objects.filter(email=value).exists():
                raise serializers.ValidationError("Email already exists.")
            return value

        def validate_password(self, value):
            if len(value) < getattr(settings, 'PASSWORD_MIN_LENGTH', 8):
                raise serializers.ValidationError(
                    "Password should be at least %s characters long." % getattr(settings, 'PASSWORD_MIN_LENGTH', 8)
                )
            return value

        def validate_password_2(self, value):
            data = self.get_initial()
            password = data.get('password')
            if password != value:
                raise serializers.ValidationError("Passwords doesn't match.")

            return value

        def create(self, validated_data):
            user_data = {
                'email': validated_data.get('email'),
                'username': validated_data.get('username'),
                'password': validated_data.get('password'),
                'first_name': validated_data.get('first_name'),
                'last_name': validated_data.get('last_name'),
                'school_name': validated_data.get('school_name'),
                'description': validated_data.get('description'),
                'logo': validated_data.get('logo'),
                'address': validated_data.get('address'),
                'tel': validated_data.get('tel'),
                'region': validated_data.get('region'),
                'bvn': validated_data.get('bvn'),
                'account_number': validated_data.get('account_number'),
            }

            return validated_data


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False, allow_blank=False, write_only=True, label="Email Address")
    token = serializers.CharField(allow_blank=True, read_only=True)
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'token']

    def validate(self, data):
        username = data['username']
        password = data['password']

        if not username:
            raise serializers.ValidationError('Username required to Login')

        user = CustomUser.objects.filter(Q(username=username)).exclude(username__isnull=True)\
            .exclude(username__iexact='').distinct()

        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise serializers.ValidationError("This email is not valid.")

        if user_obj:
            if not user_obj.check_password(password):
                raise serializers.ValidationError("Invalid credentials.")

        # if user_obj.is_active:
        #     token, created = Token.objects.get_or_create(user=user_obj)
        #     data['token'] = token
        # else:
        #     raise serializers.ValidationError("User not active.")

        return user_obj #data


class PayeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payee
        fields = '__all__'


class FeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fee
        fields = '__all__'
        depth = 1


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        depth = 1
