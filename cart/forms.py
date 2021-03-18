from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 6)]


class CartAddProductForm(forms.Form):
    """ Форма для добавления товара в корзинку """
    # quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,
    #                                   coerce=int,
    #                                   initial=1,
    #                                   label="Количество")

    quantity = forms.IntegerField(initial=1,
                                  widget=forms.HiddenInput)

    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)


class CartUpdateProductForm(forms.Form):
    """ Форма для обновления количества товара в корзинке """
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,
                                      coerce=int,
                                      initial=1,
                                      label="Количество")

    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)