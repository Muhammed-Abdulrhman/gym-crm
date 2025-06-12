from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.IntegerField(max_length=15)
    date_joined = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Progress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='progress_pictures/', blank=True, null=True)
    progress_description = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    total_body_water = models.DecimalField(max_digits=5, decimal_places=2)
    body_fat_mass = models.DecimalField(max_digits=5, decimal_places=2)
    skeletal_muscle_mass = models.DecimalField(max_digits=5, decimal_places=2)
    intracellular_fluid = models.DecimalField(max_digits=5, decimal_places=2)
    extracellular_fluid = models.DecimalField(max_digits=5, decimal_places=2)
    body_mass_index = models.DecimalField(max_digits=5, decimal_places=2)
    body_fat_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    basal_metabolic_rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.progress

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    contity = models.IntegerField()
    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name