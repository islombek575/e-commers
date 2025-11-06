from apps.models import ProductVersion
from django import forms
from django_json_widget.widgets import JSONEditorWidget


class ProductVersionForm(forms.ModelForm):
    class Meta:
        model = ProductVersion

        fields = ('attributes',)

        widgets = {
            'jsonfield': JSONEditorWidget
        }
