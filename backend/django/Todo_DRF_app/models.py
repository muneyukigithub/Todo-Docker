from django.db import models
import uuid
from django.db import models
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)
class UserManager(BaseUserManager):

    def create(self, **kwargs):
        
        kwargs["password"] = make_password(kwargs["password"])
        """
        Create a new object with the given kwargs, saving it to the database
        and returning the created object.
        """
        obj = self.model(**kwargs)
        self._for_write = True
        obj.save(force_insert=True, using=self.db)
        return obj
    
    def create_user(self, email, password=None):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            password=password
        )

        # user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=make_password(password),
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):

    email = models.EmailField(verbose_name='メールアドレス',max_length=255,unique=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) 
    admin = models.BooleanField(default=False) 

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    objects = UserManager()

    def __str__(self):             
        return self.email

    def has_perm(self, perm, obj=None):
        return self.admin

    def has_module_perms(self, app_label):
        return self.admin

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

class Project(models.Model):
    project = models.CharField(verbose_name="プロジェクト名",max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.project

    
class TaskList(models.Model):

    tasklist_id = models.UUIDField(verbose_name="タスクリストID",default=uuid.uuid4)
    edit = models.BooleanField(verbose_name="編集ステータス")
    status = models.CharField(verbose_name="作業ステータス",max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # project = models.ForeignKey(Project, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='projectData')

    def __str__(self):
        return str(self.tasklist_id)

class Task(models.Model):

    task = models.CharField(verbose_name="タスク",max_length=255)
    tasktype = models.CharField(verbose_name="タスク分類",max_length=255)
    created_at = models.DateTimeField(verbose_name="作成日",auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tasklist = models.ForeignKey(TaskList, on_delete=models.CASCADE,related_name='tasklist')
    def __str__(self):
        return self.task
