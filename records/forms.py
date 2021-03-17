from django import forms

from records.models import Product, GroupProduct, Category


class SellForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      label="Категория",
                                      help_text="Необходимо указать категорию товара",
                                      widget=forms.widgets.Select())

    class Meta:
        model = GroupProduct
        fields = ('name', 'description', 'active',)