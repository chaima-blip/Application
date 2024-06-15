from django.db import models
from django.contrib.auth.hashers import make_password

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    @classmethod
    def get_user_by_id(cls, user_id):
        try:
            return cls.objects.get(id=user_id)
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_user_by_email(cls, email):
        try:
            return cls.objects.get(email=email)
        except cls.DoesNotExist:
            return None

    def update_user(self, name=None, password=None, email=None):
        if name:
            self.name = name
        if password:
            self.password = make_password(password)  # Hash the password
        if email:
            self.email = email
        self.save()
    @classmethod
    def delete_user(cls, user_id):
        try:
            user = cls.objects.get(id=user_id)
            user.delete()
            return True
        except cls.DoesNotExist:
            return False

    @classmethod
    def add_user(cls, email, name, password):
        hashed_password = make_password(password)
        user = cls(email=email, name=name, password=hashed_password)
        user.save()
        return user

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
