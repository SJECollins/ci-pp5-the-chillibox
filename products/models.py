from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile

from django.db import models


class Category(models.Model):
    """
    Category model.
    Order by name.
    String representation returns name.
    """
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    """
    Subcategory model.
    Order by name.
    String representation returns name.
    """
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Subcategories'

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    """
    ProductVariant model. To manage options for sizes and prices.
    String representation returns variant size.
    """
    size = models.CharField(max_length=80)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.size


class Product(models.Model):
    """
    Product model.
    With method to create a thumbnail from uploaded image.
    In_stock boolean updates on save according to current_stock.
    String representation returns name.
    """
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, blank=True, related_name='product')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL,
                                    null=True, blank=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    excerpt = models.TextField(null=True, blank=True)
    ingredients = models.CharField(max_length=140, null=True, blank=True)
    growth_time = models.CharField(max_length=140, null=True, blank=True)
    heat_level = models.CharField(max_length=140, null=True, blank=True)
    box_contents = models.ManyToManyField('self', blank=True)
    variants = models.ManyToManyField(ProductVariant, blank=True,
                                      related_name='products')
    image = models.ImageField(upload_to='uploads/', null=True, blank=True)
    thumbnail = models.ImageField(upload_to='uploads/', null=True, blank=True)
    current_stock = models.PositiveIntegerField(default=0)
    in_stock = models.BooleanField(default=False)
    added_on = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('name',)
        get_latest_by = ('added_on',)

    def __str__(self):
        return self.name

    def make_thumbnail(self, image):
        """
        Create thumbnail from uploaded image
        https://gist.github.com/valberg/2429288
        """
        if not self.image:
            return
        size = 160, 160
        img = Image.open(BytesIO(image.read()))
        img.thumbnail(size)

        temp_thumb = BytesIO()
        img.save(temp_thumb, 'PNG')
        temp_thumb.seek(0)

        thumbnail = SimpleUploadedFile(image.name, temp_thumb.read())
        print(thumbnail)

        return thumbnail

    def save(self, *args, **kwargs):
        if self.current_stock < 1:
            self.in_stock = False
        elif self.current_stock >= 1:
            self.in_stock = True
        print(self.image)
        print(self.thumbnail)  # Check thumbnail -- don't forget to delete!!
        super(Product, self).save(*args, **kwargs)
        if not self.thumbnail:  # Is this super hacky?! Find better solution??
            self.thumbnail = self.make_thumbnail(self.image)
        super(Product, self).save(*args, **kwargs)