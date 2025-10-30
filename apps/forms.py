from django import forms

from .models import Product
from .widgets import KeyValueWidget


class ProductForm(forms.ModelForm):
    attributes = forms.CharField(widget=KeyValueWidget(), required=False)

    class Meta:
        model = Product
        fields = '__all__'

    def clean_attributes(self):
        import json
        data = self.cleaned_data['attributes']
        if isinstance(data, str):
            try:
                return json.loads(data)
            except Exception:
                return {}
        return data
