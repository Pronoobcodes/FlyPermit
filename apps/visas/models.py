from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=3, unique=True)  # e.g. "GBR", "USA"
    flag_emoji = models.CharField(max_length=10, blank=True)

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ['name']

    def __str__(self):
        return self.name


class VisaType(models.Model):
    CATEGORY_CHOICES = [
        ('tourist', 'Tourist'),
        ('student', 'Student'),
        ('work', 'Work'),
        ('business', 'Business'),
        ('transit', 'Transit'),
        ('family', 'Family/Spousal'),
    ]

    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name='visa_types'
    )
    name = models.CharField(max_length=150)         # e.g. "UK Standard Visitor Visa"
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    processing_time = models.CharField(max_length=100, blank=True)  # e.g. "3-6 weeks"
    fee_usd = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    validity = models.CharField(max_length=100, blank=True)  # e.g. "6 months"
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['country', 'name']

    def __str__(self):
        return f"{self.country.name} — {self.name}"


class DocumentRequirement(models.Model):
    IMPORTANCE_CHOICES = [
        ('mandatory', 'Mandatory'),
        ('optional', 'Optional'),
        ('conditional', 'Conditional'),  # e.g. only if self-employed
    ]

    visa_type = models.ForeignKey(
        VisaType, on_delete=models.CASCADE, related_name='document_requirements'
    )
    name = models.CharField(max_length=200)           # e.g. "International Passport"
    description = models.TextField(blank=True)        # extra guidance
    importance = models.CharField(max_length=20, choices=IMPORTANCE_CHOICES, default='mandatory')
    condition_note = models.CharField(max_length=255, blank=True)  # e.g. "Required if self-employed"
    order = models.PositiveIntegerField(default=0)    # controls display order

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} ({self.visa_type})"