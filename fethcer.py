import argparse
import socket
import concurrent.futures
import datetime
import sys
import os
import random
from rich.console import Console
from rich.table import Table
from rich.progress import Progress

console = Console()

def clear_terminal():
    """Clear the terminal screen before running"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Display a colorful randomized banner"""
    colors = ["bold blue", "bold green", "bold red", "bold yellow", "bold magenta", "bold cyan"]
    color = random.choice(colors)
    banner = """
    ░▒▓████████▓▒░▒▓████████▓▒░▒▓████████▓▒░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓███████▓▒░  
    ░▒▓█▓▒░      ░▒▓█▓▒░         ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
    ░▒▓█▓▒░      ░▒▓█▓▒░         ░▒▓█▓▒░  ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
    ░▒▓██████▓▒░ ░▒▓██████▓▒░    ░▒▓█▓▒░  ░▒▓█▓▒░      ░▒▓████████▓▒░▒▓██████▓▒░ ░▒▓███████▓▒░  
    ░▒▓█▓▒░      ░▒▓█▓▒░         ░▒▓█▓▒░  ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
    ░▒▓█▓▒░      ░▒▓█▓▒░         ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
    ░▒▓█▓▒░      ░▒▓████████▓▒░  ░▒▓█▓▒░   ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░ 
                    "Curiosity is the spark behind every great discovery."
                                         Made by sh1vv
    """
    console.print(banner, style=color)

def check_subdomain_dns(subdomain, debug, output_file=None):
    """Check if a subdomain exists via DNS resolution"""
    try:
        if not subdomain or subdomain.startswith(".") or ".." in subdomain:
            return None  # Skip invalid subdomains
        
        ip = socket.gethostbyname(subdomain)
        console.print(f"[+] Found: {subdomain} -> {ip}", style="bold green")

        # Write to file in real-time if output file is provided
        if output_file:
            with open(output_file, 'a') as f:
                f.write(f"{subdomain} ({ip})\n")

        return subdomain, ip
    except socket.gaierror:
        if debug:
            console.print(f"[DEBUG] {subdomain} -> NXDOMAIN", style="bold red")
    return None

def brute_force(domain, wordlist, fast, debug, output_file=None):
    """Perform DNS brute forcing on a domain using a wordlist"""
    with open(wordlist, 'r') as file:
        words = [line.strip() for line in file if line.strip() and not line.startswith(".")]
    
    found_subdomains = []
    
    with Progress() as progress:
        task = progress.add_task(f"[cyan]Brute-forcing {domain}...", total=len(words))

        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=50 if fast else 10) as executor:
                futures = {}
                
                for word in words:
                    if not word or "." in word:
                        continue  # Prevent malformed subdomains
                    
                    subdomain = f"{word}.{domain}"
                    futures[executor.submit(check_subdomain_dns, subdomain, debug, output_file)] = subdomain
                
                for future in concurrent.futures.as_completed(futures):
                    try:
                        result = future.result()
                        if result:
                            found_subdomains.append(result)
                    except Exception as e:
                        console.print(f"[ERROR] Thread error: {e}", style="bold red")
                    
                    progress.update(task, advance=1)
        except KeyboardInterrupt:
            console.print("\n[!] Scan interrupted by user. Exiting cleanly...", style="bold red")
            sys.exit(0)

    return found_subdomains

def main():
    clear_terminal()
    print_banner()
    parser = argparse.ArgumentParser(description='fetcher - A professional DNS-based subdomain brute forcer')
    parser.add_argument('-d', '--domain', type=str, help='Target domain')
    parser.add_argument('-w', '--wordlist', type=str, required=True, help='Path to wordlist')
    parser.add_argument('-o', '--output', type=str, nargs='?', const=True, help='Save output to a file (default: timestamped file)')
    parser.add_argument('-tl', '--target-list', type=str, help='File containing multiple domains')
    parser.add_argument('-f', '--fast', action='store_true', help='Enable fast brute forcing')
    parser.add_argument('--debug', action='store_true', help='Enable debugging mode')
    args = parser.parse_args()
    
    domains = []
    if args.target_list:
        with open(args.target_list, 'r') as file:
            domains = [line.strip() for line in file if line.strip()]
    elif args.domain:
        domains.append(args.domain)
    else:
        console.print("[ERROR] You must specify a target domain (-d) or a target list (-tl)", style="bold red")
        sys.exit(1)
    
    # Determine output file name
    if args.output:
        output_file = args.output if isinstance(args.output, str) else f"{domains[0]}_subdomains_{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
        console.print(f"[INFO] Output file: {output_file}", style="bold cyan")
        open(output_file, 'w').close()  # Clear previous content
    else:
        output_file = None

    for domain in domains:
        console.print(f"[INFO] Brute-forcing {domain}", style="bold yellow")
        brute_force(domain, args.wordlist, args.fast, args.debug, output_file)

    console.print("[✔] Brute-force completed.", style="bold green")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[!] Scan interrupted by user. Exiting cleanly...", style="bold red")
        sys.exit(0)
