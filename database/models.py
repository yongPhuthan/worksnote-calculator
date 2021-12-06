from django.db import models
from django import forms
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields import EmailField
from django.db.models.fields.related import ForeignKey
from django.forms import fields, widgets
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, PermissionsMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import UserManager, User


    
class User(AbstractUser):
    pass

class DoorFoldingCost(models.Model):
  
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    
    brand = models.CharField( max_length=50)
    color = models.CharField(max_length=20,choices= [('สีดำ','สีดำ'),('สีขาว','สีขาว'), ('สีเทา','สีเทา'), ('สีลายไม้อ่อน','สีลายไม้อ่อน'), ('สีลายไม้เข้ม','สีลายไม้เข้ม')],default='สีขาว'

    )
    
    thick = models.CharField(max_length= 20,choices=[('1.0 mm','1.0 mm'),('1.2 mm','1.2 mm'),('1.5 mm','1.5 mm'),('1.6 mm','1.6 mm'),('2.0 mm','2.0 mm')],
        default='1.2 mm'
    )
    
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.user)


# ต้นทุนอลูมิเนียมบานเลื่อน
class SlidingDoor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)

    brand = models.CharField( max_length=50)
    color = models.CharField(max_length=20,choices= [('สีดำ','สีดำ'),('สีขาว','สีขาว'), ('สีเทา','สีเทา'), ('สีลายไม้อ่อน','สีลายไม้อ่อน'), ('สีลายไม้เข้ม','สีลายไม้เข้ม')],default='สีขาว'

    )
    
    thick = models.CharField(max_length= 20,choices=[('1.0 mm','1.0 mm'),('1.2 mm','1.2 mm'),('1.5 mm','1.5 mm'),('1.6 mm','1.6 mm'),('2.0 mm','2.0 mm')],
        default='1.2 mm'
    )
    
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
       
            return f'{self.brand}|{self.thick}|{self.color}|{self.price}|str{self.user}'


class SwingDoor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    brand = models.CharField( max_length=50)
    color = models.CharField(max_length=20,choices= [('สีดำ','สีดำ'),('สีขาว','สีขาว'), ('สีเทา','สีเทา'), ('สีลายไม้อ่อน','สีลายไม้อ่อน'), ('สีลายไม้เข้ม','สีลายไม้เข้ม')],default='สีขาว'

    )
    
    thick = models.CharField(max_length= 20,choices=[('1.0 mm','1.0 mm'),('1.2 mm','1.2 mm'),('1.5 mm','1.5 mm'),('1.6 mm','1.6 mm'),('2.0 mm','2.0 mm')],
        default='1.2 mm'
    )
    
    price = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    def __str__(self):
       
            return f'{self.brand}|{self.thick}|{self.color}|{self.price}|str{self.user}'

# ต้นทุนกระจก
class Glasscost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    glassType = models.CharField(
        max_length=20,
        choices=[('กระจกเทมเปอร์','กระจกเทมเปอร์'),('กระจกเขียวตัดแสง','กระจกเขียวตัดแสง'),('กระจกใส','กระจกใส'),('กระจกลามิเนต','กระจกลามิเนต'),('กระจกชาดำ','กระจกชาดำ'),('กระจกอินซูเลท','กระจกอินซูเลท'),('กระจกฝ้า','กระจกฝ้า')],
        default='กระจกใส'
    ) 
    glassThick = models.CharField(
        max_length=20,
        choices=[('4.0 mm','4 mm'),('5.0 mm','5 mm'),('6.0 mm','6 mm'),('8.0 mm','8 mm'),('10.0 mm','10 mm'),('12.0mm','12 mm')],
        default='6.0 mm'
    )
    price = models.FloatField()
    def __str__(self):
       
        return f'{self.glassType}|{self.glassThick}|{self.price}|str{self.user}'
         


 # ต้นทุนขนส่ง ค่าแรง อุปกรณ์เสริม

# ต้นทุนค่าใช้จ่ายอื่นๆ
class OtherCost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    cbm_cost = models.FloatField()
    kg_cost = models.FloatField()
    labor_cost = models.IntegerField()
    transport_cost = models.IntegerField()
    tools_cost = models.IntegerField()
    other_cost = models.FloatField()

    def __str__(self):
        return f'{self.cbm_cost}|{self.kg_cost}|{self.labor_cost}|{self.transport_cost}|{self.tools_cost}|{self.other_cost}|str{self.user}'