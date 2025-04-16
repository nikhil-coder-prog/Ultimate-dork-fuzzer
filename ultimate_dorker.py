import webbrowser
import time
import os

def load_wordlist(path):
    try:
        with open(path, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[!] Wordlist not found at {path}")
        return []

def generate_engine_urls(domain, dorks):
    urls = []
    for dork in dorks:
        # Google
        google = f"https://www.google.com/search?q=site:{domain}+{dork.replace(' ', '+')}"
        # GitHub
        github = f"https://github.com/search?q=site:{domain}+{dork.replace(' ', '+')}"
        # Shodan
        shodan = f"https://www.shodan.io/search?query={dork.replace(' ', '+')}+hostname:{domain}"

        urls.append({
            'dork': dork,
            'google': google,
            'github': github,
            'shodan': shodan
        })
    return urls

def save_results(results, out_file):
    with open(out_file, 'w') as f:
        for result in results:
            f.write(f"\n[DORK] {result['dork']}\n")
            f.write(f"[Google ] {result['google']}\n")
            f.write(f"[GitHub ] {result['github']}\n")
            f.write(f"[Shodan ] {result['shodan']}\n")
    print(f"\n[+] Saved multi-engine dork URLs to {out_file}")

def main():
    print("=== Ultimate Multi-Engine Dork Fuzzer ===\n")

    domain = input("Enter target domain (e.g., example.com): ").strip()

    # NEW: Let user choose their own wordlist
    wordlist_path = input("Enter path to your dork wordlist (e.g., wordlists/dorks.txt): ").strip()
    if not os.path.exists(wordlist_path):
        print("[!] Wordlist file not found. Exiting.")
        return

    output_file = f"results/{domain.replace('.', '_')}_dorks.txt"

    dork_list = load_wordlist(wordlist_path)
    if not dork_list:
        return

    results = generate_engine_urls(domain, dork_list)

    print(f"\n[+] Generated {len(results)} dorks for 3 engines each:\n")

    for r in results:
        print(f"[DORK] {r['dork']}")
        print(f" Google: {r['google']}")
        print(f" GitHub: {r['github']}")
        print(f" Shodan: {r['shodan']}\n")
        time.sleep(0.2)  # Delay to avoid being too fast

    save = input("Save all URLs to file? (y/n): ").lower()
    if save == 'y':
        os.makedirs("results", exist_ok=True)
        save_results(results, output_file)

if __name__ == "__main__":
    main()
