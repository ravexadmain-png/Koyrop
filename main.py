import os
import socket
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor

# Color codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
WHITE = "\033[97m"
RESET = "\033[0m"

def banner():
    print(f"""{CYAN}
       ▄██████▄
      ██ ◣   ◢ ██
     ██    ▄▄  ██
      ██ ████ ██
       ▀██████▀ 

{WHITE}==================================================
{GREEN}       Wolfer tools - koyrop [PRO v3.2]
{YELLOW}       Operator : Algriom
{CYAN}       Channel  : @algriomhake44
{WHITE}=================================================={RESET}
""")

def get_recon(url):
    print(f"{YELLOW}[*] Target er basic info collect kora hocche...{RESET}")
    parsed = urlparse(url)
    domain = parsed.netloc
    try:
        ip = socket.gethostbyname(domain)
        print(f"{GREEN}[+] Target Domain: {domain}{RESET}")
        print(f"{GREEN}[+] Server IP: {ip}{RESET}")
    except:
        print(f"{RED}[!] IP resolve kora jayni. Sothik URL din.{RESET}")

def get_local_path(url, output_dir):
    parsed = urlparse(url)
    path = parsed.path.lstrip('/')
    if not path or path.endswith('/'):
        path += "index.html"
    
    path = path.split('?')[0]
    local_file_path = os.path.join(output_dir, path)
    return local_file_path, path

def save_file(url, content, output_dir, is_binary=False):
    try:
        local_file_path, relative_path = get_local_path(url, output_dir)
        local_dir = os.path.dirname(local_file_path)

        if local_dir and not os.path.exists(local_dir):
            os.makedirs(local_dir, exist_ok=True)

        mode = "wb" if is_binary else "w"
        encoding = None if is_binary else "utf-8"
        
        with open(local_file_path, mode, encoding=encoding) as f:
            f.write(content)
        return relative_path
    except Exception as e:
        return None

def generate_dashboard(output_dir, domain_name, all_files):
    dashboard_path = os.path.join(output_dir, "wolfer_dashboard.html")
    
    files_html = ""
    for file_path in sorted(all_files):
        is_asset = file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.mp4', '.mp3', '.zip', '.pdf', '.woff', '.ttf', '.ico'))
        
        if is_asset:
            action_btn = f'''
                <a href="{file_path}" download class="action-btn download-btn">
                    📥 Download
                </a>
            '''
        else:
            action_btn = f'''
                <button onclick="copyCode(this, '{file_path}')" class="action-btn copy-btn">
                    📋 Copy Code
                </button>
            '''

        files_html += f'''
        <div class="file-card">
            <span class="file-name">📁 {file_path}</span>
            <div class="actions">
                <a href="{file_path}" target="_blank" class="view-btn">👁️ View</a>
                {action_btn}
            </div>
        </div>
        '''

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wolfer Pro Dashboard - {domain_name}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>⚡ Wolfer Pro Architecture Cloner</h1>
        <p class="sub">Target: {domain_name}</p>
        <div class="file-list">
            {files_html}
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>
"""
    with open(dashboard_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    # Copy style.css and script.js to output dir so dashboard looks good
    try:
        if os.path.exists("style.css"):
            with open("style.css", "r") as sf:
                with open(os.path.join(output_dir, "style.css"), "w") as df:
                    df.write(sf.read())
        if os.path.exists("script.js"):
            with open("script.js", "r") as sf:
                with open(os.path.join(output_dir, "script.js"), "w") as df:
                    df.write(sf.read())
    except:
        pass

    print(f"\n{GREEN}[✨ DASHBOARD CREATED] Browser e open korun: {dashboard_path}{RESET}")

def start_cloning(start_url):
    if not start_url.startswith("http"):
        start_url = "https://" + start_url

    get_recon(start_url)
    
    parsed_start = urlparse(start_url)
    domain_name = parsed_start.netloc.replace(":", "_")
    output_dir = f"WolferPro_{domain_name}"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    visited_urls = set()
    urls_to_visit = [start_url]
    asset_urls = set()
    saved_files_list = set()

    print(f"\n{YELLOW}[*] Crawling and file download start hoyeche...{RESET}")

    max_pages = 25
    page_count = 0

    while urls_to_visit and page_count < max_pages:
        current_url = urls_to_visit.pop(0)
        if current_url in visited_urls:
            continue

        visited_urls.add(current_url)
        page_count += 1
        print(f"{CYAN}[Crawling {page_count}] -> {current_url}{RESET}")

        try:
            res = session.get(current_url, headers=headers, timeout=10)
            if res.status_code != 200:
                continue

            content_type = res.headers.get("Content-Type", "")
            if "text/html" in content_type:
                path = save_file(current_url, res.text, output_dir, is_binary=False)
                if path:
                    saved_files_list.add(path)
                
                soup = BeautifulSoup(res.text, 'html.parser')
                for tag in soup.find_all(['a', 'img', 'script', 'link', 'source', 'video', 'audio']):
                    attr = 'href' if tag.name in ['a', 'link'] else 'src'
                    if tag.name == 'source':
                        attr = 'srcset'
                    
                    file_url = tag.get(attr)
                    if file_url:
                        absolute_url = urljoin(current_url, file_url)
                        parsed_abs = urlparse(absolute_url)

                        if parsed_abs.netloc == parsed_start.netloc:
                            if tag.name == 'a':
                                clean_url = absolute_url.split('#')[0]
                                if clean_url not in visited_urls and clean_url not in urls_to_visit and not clean_url.endswith(('.png', '.jpg', '.jpeg', '.pdf', '.zip', '.mp4')):
                                    urls_to_visit.append(clean_url)
                            else:
                                asset_urls.add(absolute_url)
            else:
                path = save_file(current_url, res.content, output_dir, is_binary=True)
                if path:
                    saved_files_list.add(path)
        except Exception as e:
            continue

    def download_asset(asset_url):
        try:
            r = session.get(asset_url, headers=headers, timeout=7)
            if r.status_code == 200:
                is_bin = not asset_url.lower().endswith(('.css', '.js', '.html', '.txt', '.json'))
                path = save_file(asset_url, r.content if is_bin else r.text, output_dir, is_binary=is_bin)
                if path:
                    saved_files_list.add(path)
        except:
            pass

    print(f"\n{YELLOW}[*] Total {len(asset_urls)} ti asset download hocche...{RESET}")
    with ThreadPoolExecutor(max_workers=10) as executor:
        for asset in asset_urls:
            executor.submit(download_asset, asset)

    generate_dashboard(output_dir, domain_name, saved_files_list)
    print(f"\n{GREEN}[🎉] Kaj complete! Folder: '{output_dir}'{RESET}")

if __name__ == "__main__":
    banner()
    target = input(f"{CYAN}Target website er link din (e.g. https://example.com) -> {RESET}").strip()
    if target:
        start_cloning(target)
    else:
        print(f"{RED}[!] Bhul link! Doya kore thik moto URL din.{RESET}")
