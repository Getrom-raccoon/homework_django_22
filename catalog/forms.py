from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    """Форма для создания и редактирования продукта"""

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название продукта'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Введите описание продукта', 'rows': 5}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Введите цену', 'step': '0.01'}),
        }

    FORBIDDEN_WORDS = [
        'казино',
        'криптовалюта',
        'крипта',
        'биржа',
        'дешево',
        'бесплатно',
        'обман',
        'полиция',
        'радар'
    ]

    def __init__(self, *args, **kwargs):
        """Стилизация формы через __init__"""
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name == 'is_published':
                continue

            if field_name == 'description':
                field.widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': 'Введите описание продукта',
                    'rows': 5
                })
            elif field_name == 'category':
                field.widget.attrs.update({
                    'class': 'form-select'
                })
            elif field_name == 'image':
                field.widget.attrs.update({
                    'class': 'form-control'
                })
            elif field_name == 'price':
                field.widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': 'Введите цену',
                    'step': '0.01',
                    'min': '0.01'
                })
            else:
                field.widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': f'Введите {field.label}'
                })

    def clean_name(self):
        """Валидация поля name"""
        name = self.cleaned_data['name']

        for word in self.FORBIDDEN_WORDS:
            if word.lower() in name.lower():
                raise forms.ValidationError(f'Название не может содержать слово "{word}"')

        return name

    def clean_description(self):
        """Валидация поля description"""
        description = self.cleaned_data['description']

        for word in self.FORBIDDEN_WORDS:
            if word.lower() in description.lower():
                raise forms.ValidationError(f'Описание не может содержать слово "{word}"')

        return description

    def clean_price(self):
        """Кастомная валидация для поля price"""
        price = self.cleaned_data['price']

        if price <= 0:
            raise forms.ValidationError('Цена не может быть отрицательной или равной нулю')

        if price > 1000000:
            raise forms.ValidationError('Цена не может превышать 1,000,000 руб.')

        return price