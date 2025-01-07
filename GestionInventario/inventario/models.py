from django.db import models

class Categoria(models.Model):
    CategoriaID = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=100)
    Descripcion = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'Categorias'
        managed = False

    def __str__(self):
        return self.Nombre


class Proveedor(models.Model):
    ProveedorID = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=100)
    Telefono = models.CharField(max_length=20, null=True, blank=True)
    Correo = models.EmailField(null=True, blank=True)
    Direccion = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'Proveedores'
        managed = False

    def __str__(self):
        return self.Nombre


class Producto(models.Model):
    ProductoID = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=255)
    CategoriaID = models.ForeignKey(Categoria, on_delete=models.CASCADE, db_column='CategoriaID', related_name='productos')
    ProveedorID = models.ForeignKey(Proveedor, on_delete=models.CASCADE, db_column='ProveedorID', related_name='productos')
    Precio = models.DecimalField(max_digits=10, decimal_places=2)
    Stock = models.IntegerField(default=0)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    class Meta:
        db_table = 'Productos'
        managed = False

    def __str__(self):
        return self.Nombre


class Cliente(models.Model):
    ClienteID = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=100)
    Telefono = models.CharField(max_length=20, null=True, blank=True)
    Correo = models.EmailField(null=True, blank=True)
    Direccion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.Nombre


class Orden(models.Model):
    OrdenID = models.AutoField(primary_key=True)
    ClienteID = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    Fecha = models.DateTimeField(auto_now_add=True)
    Total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Orden #{self.OrdenID} - Cliente: {self.ClienteID.Nombre}"


class DetalleOrden(models.Model):
    DetalleID = models.AutoField(primary_key=True)
    OrdenID = models.ForeignKey(Orden, on_delete=models.CASCADE)
    ProductoID = models.ForeignKey(Producto, on_delete=models.CASCADE)
    Cantidad = models.IntegerField()
    PrecioUnitario = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def Subtotal(self):
        return self.Cantidad * self.PrecioUnitario
    



