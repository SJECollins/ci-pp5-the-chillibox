from django import forms
from products.models import Variant


class StockForm(forms.ModelForm):
    """
    ModelForm for current_stock so staff can update.
    """
    class Meta:
        """
        Only want current_stock field.
        """
        model = Variant
        fields = ['current_stock', ]
