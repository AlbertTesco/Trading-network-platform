from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    model = models.CharField(max_length=100, verbose_name='Модель')
    release_date = models.DateField(verbose_name='Дата выпуска')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class NetworkNode(models.Model):
    NODE_CHOICES = (
        ('Factory', 'Завод'),
        ('RetailNetwork', 'Розничная сеть'),
        ('IndividualEntrepreneur', 'Индивидуальный предприниматель')
    )

    level = models.IntegerField(verbose_name='Уровень в торговой сети')
    name = models.CharField(max_length=100, verbose_name='Название')
    email = models.EmailField(verbose_name='Email', help_text='Введите действующий email')
    city = models.CharField(max_length=100, verbose_name='Город')
    street = models.CharField(max_length=100, verbose_name='Улица')
    house_number = models.CharField(max_length=20, verbose_name='Номер дома')
    node_type = models.CharField(max_length=50, choices=NODE_CHOICES, verbose_name='Тип')
    supplier = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='suppliers',
                                 verbose_name='Поставщик')
    products = models.ManyToManyField('Product', related_name='network_nodes', verbose_name='Продукты')
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Долг поставщику')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Звено'
        verbose_name_plural = 'Звенья'
