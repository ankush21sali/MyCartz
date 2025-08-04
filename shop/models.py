from django.db import models

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=300)
    pub_date = models.DateField()
    image = models.ImageField(upload_to="shop/images",default="")

    def __str__(self):
        return self.product_name


class ContactUs(models.Model):
    contact_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default="")
    email = models.EmailField(max_length=254, blank=False, null=False)
    phone = models.CharField(max_length=20)
    desc = models.CharField(max_length=500, default="")

    def __str__(self):
        return self.name


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, default="")
    last_name = models.CharField(max_length=50, default="")
    email = models.EmailField(max_length=245, blank=False, null=False)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=6)

    cart_data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    price = models.FloatField()
    quantity = models.IntegerField()