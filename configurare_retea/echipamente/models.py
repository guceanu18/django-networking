from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
from django.db import models


class Echipament(models.Model):
    TIP_ECHIPAMENT = [
        ('router', 'Router'),
        ('switch', 'Switch'),
    ]

    tip = models.CharField(max_length=50, choices=TIP_ECHIPAMENT)
    nume = models.CharField(max_length=100)
    ip = models.GenericIPAddressField()
    utilizator = models.CharField(max_length=50)
    parola = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nume} ({self.tip})"

    def sterge_echipament(self):
        self.delete()

    def save(self, *args, **kwargs):
        # Salvăm obiectul Echipament
        super().save(*args, **kwargs)

        # Dacă tipul este "router", creăm un obiect de tip Router
        if self.tip == 'router':
            Router.objects.get_or_create(
                router=self,  # Asociem Echipamentul la Router
                nume=self.nume,
                ip_mgmt=self.ip
            )


class InterfataRouter(models.Model):
    # Numele interfeței (ex.: GigabitEthernet0/1, FastEthernet0/0)
    nume_interfata = models.CharField(max_length=50, verbose_name="Numele Interfetei")

    # IP-ul configurat pe interfață (opțional)
    ip = models.GenericIPAddressField(
        verbose_name="Adresa IP",
        blank=True,  # Permite câmpuri necompletate în formular
        null=True,  # Permite salvarea ca NULL în baza de date
    )

    # Routerul de care aparține interfața (legătură cu un model de tip Router)
    router = models.ForeignKey(
        'Router',  # Referință la un model de tip Router (vezi mai jos)
        on_delete=models.CASCADE,  # Șterge interfețele dacă routerul este șters
        related_name='interfete',
        verbose_name="Router"
    )

    def sterge_interfata(self):
        self.delete()

    def editare_interfata(self, new_ip):
        self.ip = new_ip
        self.save()

    def __str__(self):
        return f"{self.nume_interfata} - {self.ip or 'N/A'}"


class Router(models.Model):
    # Numele routerului (ex.: Router1)
    nume = models.CharField(max_length=100, verbose_name="Numele Routerului")

    # Adresa IP de mgmt a routerului
    ip_mgmt = models.GenericIPAddressField(verbose_name="IP Management")

    router = models.ForeignKey(
        'Echipament',  # Referință la un model de tip Echipament
        on_delete=models.CASCADE,
        related_name='echipament',
        verbose_name="Router",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.nume