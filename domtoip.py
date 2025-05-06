import socket
from multiprocessing.dummy import Pool as ThreadPool
from colorama import Fore, init, Style
import os

# Inisialisasi colorama
init(autoreset=True)

# Banner
print(Fore.YELLOW + Style.BRIGHT + "\n[+] MASS DOMAIN TO IP LOOKUP [+]\n")

# Minta nama file dari user
file_path = input(Fore.RED + Style.BRIGHT + "[>] Masukkan nama file daftar domain (contoh: domains.txt): ").strip()

# Cek apakah file ada
if not os.path.isfile(file_path):
    print(Fore.RED + f"[!] File '{file_path}' tidak ditemukan.")
    exit()

# Baca domain dari file
with open(file_path, 'r') as f:
    domain_list = f.read().replace('http://', '').replace('https://', '').splitlines()

# Minta jumlah thread
thread_count = input(Fore.WHITE + '[>] Jumlah thread:~# ').strip()
try:
    thread_count = int(thread_count)
except ValueError:
    print(Fore.RED + "[!] Jumlah thread harus berupa angka.")
    exit()

# Pastikan file hasil ada
output_file = 'ips.txt'
if not os.path.exists(output_file):
    open(output_file, 'w').close()

# Fungsi untuk konversi domain ke IP
def domain_to_ip(domain):
    try:
        ip = socket.gethostbyname(domain.strip())
        with open(output_file, 'r') as f:
            if ip in f.read():
                return  # Skip jika sudah ada
        print(Fore.GREEN + f"[✓] Results: {ip} ({domain})")
        with open(output_file, 'a') as f:
            f.write(ip + '\n')
    except socket.gaierror:
        print(Fore.RED + f"[✖] Vailed: {domain}")
    except Exception as e:
        print(Fore.RED + f"[!] Error {domain}: {e}")

# Jalankan dengan threading
pool = ThreadPool(thread_count)
pool.map(domain_to_ip, domain_list)
pool.close()
pool.join()

print(Fore.CYAN + f"\n[✔] Semua IP berhasil disimpan ke file: {output_file}")
