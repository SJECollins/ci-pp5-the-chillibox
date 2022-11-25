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
    description = models.TextField(null=True, blank=True,
                                   help_text='Include a description for the \
                                   product\'s page.')
    excerpt = models.TextField(null=True, blank=True, help_text='Include a \
                               brief summary of the product.')
    ingredients = models.CharField(max_length=140, null=True, blank=True,
                                   help_text='For sauces, please include the \
                                   ingredients.')
    growth_time = models.CharField(max_length=140, null=True, blank=True,
                                   help_text='For seeds, please include the \
                                   growth time to maturity.')
    heat_level = models.CharField(max_length=140, null=True, blank=True,
                                  help_text='In scovilles or more generally \
                                  (eg \'hot\') where appropriate.')
    box_contents = models.ManyToManyField('self', blank=True, help_text='Add \
                                          products for seed and sauce boxes.')
    image = models.ImageField(upload_to='uploads/', null=True, blank=True)
    thumbnail = models.ImageField(upload_to='uploads/', null=True, blank=True,
                                  help_text='If not added, will be \
                                  auto-generated from image.')
    added_on = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('name',)
        get_latest_by = ('added_on',)

    def __str__(self):
        return self.name

    def check_stock(self, *args, **kwargs):
        in_stock = False
        for variant in self.variants.all():
            if variant.in_stock:
                in_stock = True
        return in_stock

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
        print(self.image)
        print(self.thumbnail)  # Check thumbnail -- don't forget to delete!!
        super(Product, self).save(*args, **kwargs)
        if self.image:
            if not self.thumbnail:  # Is this super hacky?! Find better solution??
                self.thumbnail = self.make_thumbnail(self.image)
        super(Product, self).save(*args, **kwargs)


class Variant(models.Model):
    """
    ProductVariant model. To manage options for sizes and prices.
    String representation returns variant size.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    size = models.CharField(max_length=80)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    current_stock = models.PositiveIntegerField(default=0,
                                                help_text='Default is 0.')
    in_stock = models.BooleanField(default=False,
                                   help_text='Updates when current stock \
                                   updated.')

    class Meta:
        verbose_name_plural = 'Variants'

    def __str__(self):
        return self.size

    def save(self, *args, **kwargs):
        if self.current_stock < 1:
            self.in_stock = False
        elif self.current_stock >= 1:
            self.in_stock = True
        super(Variant, self).save(*args, **kwargs)
