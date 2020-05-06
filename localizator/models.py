from django.contrib.postgres.fields import JSONField
from django.db import migrations, models
from datetime import date

class LocalizationsData(models.Model):
    name = models.CharField(max_length=200)
    data = JSONField()
    pub_date = models.DateField(default=date.today)

    def __str__(self):
        return self.name

    def date(self):
        return str(self.pub_date)

class HealthStatus(models.Model):
    name = models.CharField(max_length=200)
    status = models.BooleanField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

    def covid_status(self):
        return self.status

    def covid_start_date(self):
        return str(self.start_date)

    def covid_end_date(self):
        return str(self.end_date)

