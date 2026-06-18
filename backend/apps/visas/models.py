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
    tips = models.TextField(blank=True, help_text="General tips, e.g., fees in Naira, booking advice.")
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
        ('conditional', 'Conditional'),
    ]

    ICON_CATEGORY_CHOICES = [
        ('passport', 'Passport'),
        ('photo', 'Photograph'),
        ('financial', 'Financial Document'),
        ('employment', 'Employment Document'),
        ('accommodation', 'Accommodation Proof'),
        ('travel', 'Travel History'),
        ('medical', 'Medical Document'),
        ('educational', 'Educational Certificate'),
        ('other', 'Other'),
    ]

    visa_type = models.ForeignKey(VisaType, on_delete=models.CASCADE, related_name='document_requirements')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    icon_category = models.CharField(max_length=50, choices=ICON_CATEGORY_CHOICES, default='other')
    importance = models.CharField(max_length=20, choices=IMPORTANCE_CHOICES, default='mandatory')
    condition_note = models.CharField(max_length=255, blank=True)
    # sample_image = models.URLField(blank=True)         # link to example image
    sample_description = models.TextField(blank=True)  # plain English what it should contain
    common_mistakes = models.TextField(blank=True, help_text="Frequent errors leading to rejection.")
    official_source_url = models.URLField(blank=True)  # link to embassy/official page
    order = models.PositiveIntegerField(default=0)
    last_verified = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} ({self.visa_type})"