import os
from jinja2 import Template

from configurare_retea.echipamente.ssh_utils import trimite_configuratie, conecteaza_si_executa_comanda

template_path = os.path.join(os.path.dirname(__file__), 'templates', 'config_interfata.j2')

with open(template_path) as template_file:
    template = Template(template_file.read())

configuratie = template.render(
    nume_interfata='lo0',
    ip_adresa='1.1.1.1'
)
print(configuratie)

conecteaza_si_executa_comanda(
                    '192.168.72.188',
                    'admin',
                    'admin',
                    configuratie
                )