from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.core.validators import EmailValidator,MinLengthValidator,RegexValidator

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self,email,password=None,**kwargs):
        if not email :
            return ValueError('Email is required')
        
        email = self.normalize_email(email)
        user = self.model(email=email,**kwargs)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,email,password=None,**kwargs):
        kwargs.setdefault('is_admin',True)
        return self.create_user(email,password,**kwargs)


class CustomUser(AbstractBaseUser):
    email = models.EmailField(max_length=255,unique = True,validators=[EmailValidator()])
    password = models.CharField(
        max_length = 225,
        validators = [
            MinLengthValidator(limit_value=8,message='Password Should be atleast 8 charatcter'),
            RegexValidator(regex='^(?=.*[a-z])(?=.*[A-Z]).+',message='Password contain atleast 1 upper and 1 lower case')
        ]
    )
    full_name = models.CharField(max_length = 255)
    phone = models.CharField(max_length = 10,unique=True,validators = [RegexValidator(regex='^[0-9]{10}$',message='phone no. must be 10 digits')])
    address = models.CharField(max_length = 250,null = True)
    city = models.CharField(max_length = 100, null = True)
    state = models.CharField(max_length=100,null = True)
    country = models.CharField(max_length=100,null = True)
    pincode = models.CharField(max_length=6, validators=[RegexValidator(regex='^[0-9]{6}$', message="Pincode must be 6 digits.")])
    is_admin = models.BooleanField(default=False)
    last_login = None
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['full_name','phone','pincode']
    objects = CustomUserManager()

class ContentItem(models.Model):
    title = models.CharField(max_length=30)
    body = models.CharField(max_length=300)
    summary = models.CharField(max_length=300)
    document = models.FileField(upload_to='documents/' )
    categories = models.CharField(max_length=255,null = True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)