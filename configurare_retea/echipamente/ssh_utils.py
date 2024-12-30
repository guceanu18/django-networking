import time

import paramiko
from paramiko.ssh_exception import AuthenticationException, SSHException


def conecteaza_si_executa_comanda(ip, utilizator, parola, comanda):
    """
    Conectează-te la un echipament de rețea prin SSH și execută o comandă.

    :param ip_adresa: Adresa IP a echipamentului
    :param utilizator: Numele de utilizator pentru autentificare
    :param parola: Parola pentru autentificare
    :param comanda: Comanda care urmează să fie executată
    :return: Răspunsul comenzii executate sau mesaj de eroare
    """
    try:
        # Crearea unui client SSH
        ssh_client = paramiko.SSHClient()

        # Permite conexiuni la echipamentele de rețea care nu au cheia publică în known_hosts
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Conectarea la echipament
        ssh_client.connect(ip, username=utilizator, password=parola)

        # Executarea comenzii
        stdin, stdout, stderr = ssh_client.exec_command(comanda)

        # Obținerea rezultatului comenzii
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')

        # Închide conexiunea
        ssh_client.close()

        if error:
            return f"Error: {error}"
        return output
    except AuthenticationException:
        return "Autentificare eșuată. Verifică utilizatorul și parola."
    except SSHException as e:
        return f"Eroare SSH: {str(e)}"
    except Exception as e:
        return f"Eroare necunoscută: {str(e)}"


def trimite_configuratie(host, username, password, configuratie):
    """
    Trimite o configurație generată unui echipament folosind Paramiko.

    :param host: Adresa IP a echipamentului
    :param username: Numele de utilizator pentru SSH
    :param password: Parola pentru SSH
    :param configuratie: Configurația completă sub formă de string
    :return: Output-ul de la echipament
    """
    try:
        # Conectează-te prin SSH
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=host, username=username, password=password, look_for_keys=False, allow_agent=False)

        # Deschide un shell interactiv
        remote_conn = ssh_client.invoke_shell()
        time.sleep(1)

        # Intră în modul de configurare
        remote_conn.send("enable\n")
        time.sleep(1)
        remote_conn.send("conf t\n")
        time.sleep(1)

        # Trimite configurația linie cu linie
        for linie in configuratie.splitlines():
            remote_conn.send(linie + "\n")
            time.sleep(0.5)  # Așteaptă un timp între comenzi

        # Ieși din modul de configurare
        remote_conn.send("end\n")
        time.sleep(1)
        remote_conn.send("write memory\n")  # Salvează configurația
        time.sleep(1)

        # Citește output-ul final
        output = remote_conn.recv(65535).decode('utf-8')
        print(output)

        # Închide conexiunea
        ssh_client.close()

        return output
    except Exception as e:
        print(f"A apărut o eroare: {e}")
        return None