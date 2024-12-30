import os

from django.shortcuts import render

# Create your views here.
from jinja2 import Template
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Echipament, Router, InterfataRouter
from .forms import EchipamentForm, ConfigurareInterfataForm, EditareInterfataForm
from .ssh_utils import conecteaza_si_executa_comanda, trimite_configuratie


def adauga_echipament(request):
    if request.method == "POST":
        form = EchipamentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_echipamente')
    else:
        form = EchipamentForm()
    return render(request, 'echipamente/adauga_echipament.html', {'form': form})

def lista_echipamente(request):
    echipamente = Echipament.objects.all()
    return render(request, 'echipamente/lista_echipamente.html', {'echipamente': echipamente})


def actiune_echipament(request):
    echipament_id = request.GET.get('echipament_id')
    actiune = request.GET.get('actiune')

    if echipament_id and actiune:
        # Obține echipamentul pe baza ID-ului
        echipament = Echipament.objects.get(id=echipament_id)
        router = Router.objects.filter(router=echipament).first()

        if actiune == 'configurare_interfete':
            # Redirecționează către pagina de configurare interfețe
            return redirect(reverse('configurare_interfata', args=[router.id]))

        elif actiune == 'stergere_ip':
            # Redirecționează către pagina de ștergere IP
            return redirect(reverse('stergere_ip', args=[echipament.id]))

        elif actiune == 'vizualizare_interfete':
            # Redirecționează către pagina de vizualizare interfețe
            return redirect(reverse('lista_interfete', args=[router.id]))

        elif actiune == 'configureaza_echipament':
            # Redirecționează către pagina de introducere comandă manuală
            return redirect(reverse('configureaza_echipament', args=[echipament.id]))

        elif actiune == 'stergere_echipament':
            # Redirecționează către pagina de stergere echipament
            return redirect(reverse('stergere_echipament', args=[echipament.id]))

    return redirect('lista_echipamente')  # Redirecționează la lista echipamentelor dacă nu sunt parametri validați

def configureaza_echipament(request, echipament_id):
    echipament = Echipament.objects.get(id=echipament_id)

    if request.method == "POST":
        comanda = request.POST.get('comanda')
        if comanda:
            rezultat = conecteaza_si_executa_comanda(
                echipament.ip,
                echipament.utilizator,
                echipament.parola,
                comanda
            )
            return render(request, 'echipamente/configureaza_echipament.html', {
                'echipament': echipament,
                'rezultat': rezultat
            })

    return render(request, 'echipamente/configureaza_echipament.html', {'echipament': echipament})

def configurare_interfata(request, router_id):
    router = Router.objects.get(id=router_id)

    if request.method == "POST":
        form = ConfigurareInterfataForm(request.POST)
        if form.is_valid():
            # Preluarea datelor din formular

            nume_interfata = form.cleaned_data['nume_interfata']
            ip_adresa = form.cleaned_data['ip_adresa']
            masca_retea = form.cleaned_data['masca_retea']

            # Generarea configurației cu Jinja2
            template_path = os.path.join(os.path.dirname(__file__), 'templates', 'config_interfata.j2')
            with open(template_path) as template_file:
                template = Template(template_file.read())
            configuratie = template.render(
                nume_interfata=nume_interfata,
                ip_adresa=ip_adresa,
                masca_retea=masca_retea
            )

            # Trimiterea configurației la echipament cu Paramiko
            try:
                trimite_configuratie(
                    router.ip_mgmt,
                    router.router.utilizator,
                    router.router.parola,
                    configuratie
                )

                # Salvarea în baza de date
                InterfataRouter.objects.create(
                    nume_interfata=nume_interfata,
                    ip=ip_adresa,
                    router=router
                )

                # Mesaj de succes
                messages.success(request, "Configurația a fost aplicată cu succes!")
                # return redirect('lista_interfete', )  # Înlocuiește cu ruta dorită
                return HttpResponseRedirect(reverse('lista_interfete', kwargs={'router_id': router.id}))

            except Exception as e:
                messages.error(request, f"Eroare la configurarea echipamentului: {str(e)}")
                return redirect(reverse('configurare_interfata', args=[router.id]))  # Înlocuiește cu ruta dorită

    else:
        form = ConfigurareInterfataForm()

    return render(request, 'echipamente/configurare_interfata.html', {'form': form, 'router': router})

def lista_interfete(request, router_id):
    router = get_object_or_404(Router, id=router_id)
    interfete = router.interfete.all()  # Accesăm relația inversă

    if request.method == "POST":
        interfeta_selectata = request.POST.get('interfete_selectate')
        actiune = request.POST.get('actiune')

        if not interfeta_selectata:
            # Dacă nu sunt selectate interfețe
            return redirect('lista_interfete', router_id=router_id)

        if actiune == "stergere":
            # Șterge interfețele selectate
            return redirect(reverse('stergere_interfata', args=[router_id, interfeta_selectata]))
        elif actiune == "editare":
            # Redirecționează la o pagină de editare
            return redirect(reverse('editare_interfata', args=[router_id, interfeta_selectata]))

    return render(request, 'echipamente/lista_interfete.html', {'router': router, 'interfete': interfete})

def stergere_interfata(request, router_id, interfata_id):
    interfata = get_object_or_404(InterfataRouter, id=interfata_id)
    router = get_object_or_404(Router, id=router_id)

    # Generarea configurației cu Jinja2
    template_path = os.path.join(os.path.dirname(__file__), 'templates', 'sterge_interfata.j2')
    with open(template_path) as template_file:
        template = Template(template_file.read())
    configuratie = template.render(
        nume_interfata=interfata.nume_interfata
    )

    # Trimiterea configurației la echipament cu Paramiko
    try:
        trimite_configuratie(
            router.ip_mgmt,
            router.router.utilizator,
            router.router.parola,
            configuratie
        )

        # Mesaj de succes
        messages.success(request, "Configurația a fost aplicată cu succes!")
        interfata.sterge_interfata()
        return HttpResponseRedirect(reverse('lista_interfete', kwargs={'router_id': router.id}))

    except Exception as e:
        messages.error(request, f"Eroare la configurarea echipamentului: {str(e)}")
        return redirect(reverse('stergere_interfata', args=[router.id, interfata_id]))  # Înlocuiește cu ruta dorită


def editare_interfata(request, router_id, interfata_id):
    interfata = get_object_or_404(InterfataRouter, id=interfata_id)
    router = get_object_or_404(Router, id=router_id)

    if request.method == "POST":
        form = EditareInterfataForm(request.POST)
        if form.is_valid():
            # Preluarea datelor din formular
            new_ip = form.cleaned_data['new_ip']
            masca_retea = form.cleaned_data['masca_retea']
            # Generarea configurației cu Jinja2
            template_path = os.path.join(os.path.dirname(__file__), 'templates', 'editare_interfata.j2')
            with open(template_path) as template_file:
                template = Template(template_file.read())
            configuratie = template.render(
                nume_interfata=interfata.nume_interfata,
                new_ip=new_ip,
                masca_retea=masca_retea
            )
            # Trimiterea configurației la echipament cu Paramiko
            try:
                trimite_configuratie(
                    router.ip_mgmt,
                    router.router.utilizator,
                    router.router.parola,
                    configuratie
                )

                # Mesaj de succes
                messages.success(request, "Configurația a fost aplicată cu succes!")
                interfata.editare_interfata(new_ip)
                return HttpResponseRedirect(reverse('lista_interfete', kwargs={'router_id': router.id}))

            except Exception as e:
                messages.error(request, f"Eroare la configurarea echipamentului: {str(e)}")
                return redirect(reverse('editare_interfata', args=[router.id, interfata_id]))  # Înlocuiește cu ruta dorită

    else:
        form = EditareInterfataForm()

        return render(request, 'echipamente/editare_interfata.html',
                      {'form': form, 'router': router, 'interfata': interfata})

def stergere_echipament(request, echipament_id):
    echipament = get_object_or_404(Echipament, id=echipament_id)
    echipament.sterge_echipament()
    return redirect('lista_echipamente')
