from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_countries.fields import CountryField

from products.models import Product


class UserProfile(models.Model):
    """
    A user profile model for maintaining delivery information and order history
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=40, null=True, blank=True)
    last_name = models.CharField(max_length=80, null=True, blank=True)
    display_name = models.CharField(max_length=40, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    street_address1 = models.CharField(max_length=80, null=True, blank=True)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    country = CountryField(blank_label='Country', null=True, blank=True)
    postcode = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return self.display_name

    def save(self, *args, **kwargs):
        """
        Override save to save display_name as username in case user hasn't
        added
        """
        if not self.display_name:
            self.display_name = self.user.username
        super(UserProfile, self).save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile.
    """
    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.userprofile.save()


class Reviews(models.Model):
    """
    User reviews for products
    """
    reviewer = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                 null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='reviews')
    content = models.TextField()
    rating = models.PositiveIntegerField()
    added_on = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateField(auto_now=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.content
