from django import forms
from .models import Echipament, Router, InterfataRouter

class EchipamentForm(forms.ModelForm):
    class Meta:
        model = Echipament
        fields = ['tip', 'nume', 'ip', 'utilizator', 'parola']

    parola = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'  # Adaugă clasa CSS pentru stilizare
    }))

class ConfigurareInterfataForm(forms.Form):
    # router_id = forms.ModelChoiceField(
    #     queryset=Router.objects.all(),
    #     label="Echipament",
    #     help_text="Selectează echipamentul din baza de date."
    # )
    nume_interfata = forms.CharField(
        max_length=50,
        label="Nume Interfață",
        help_text="Exemplu: GigabitEthernet0/1"
    )
    ip_adresa = forms.GenericIPAddressField(
        label="Adresă IP",
        required=True,
        help_text="Introdu adresa IP (format IPv4)."
    )
    masca_retea = forms.GenericIPAddressField(
        label="Masca de retea",
        required=True,
        help_text="Introdu masca de retea (format dotted decimal)."
    )

class EditareInterfataForm(forms.Form):
    new_ip = forms.GenericIPAddressField(
        label="Adresă IP",
        required=True,
        help_text="Introdu adresa IP (format IPv4)."
    )
    masca_retea = forms.GenericIPAddressField(
        label="Masca de retea",
        required=True,
        help_text="Introdu masca de retea (format dotted decimal)."
    )