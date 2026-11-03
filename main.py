import os
import socket
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor

# কালার কোড
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
WHITE = "\033[97m"
RESET = "\033[0m"

def banner():
    print(f"""{CYAN}
       ▄██████▄
      ██ ◣    ◢    ██
     ██     ▄▄     ██
      ██ ████ ██
       ▀██████▀ 

{WHITE}==================================================
{GREEN}       Wolfer tools - koyrop [ULTRA v2.0]
{YELLOW}       Operator : Algriom
{CYAN}       Channel  : @algriomhake44
{WHITE}=================================================={RESET}
""")

def get_recon(url):
    print(f"{YELLOW}[*] টার্গেটের বেসিক ইনফো ও নেটওয়ার্ক রিকন চলছে...{RESET}")
    parsed = urlparse(url)
    domain = parsed.netloc
    try:
        ip = socket.gethostbyname(domain)
        print(f"{GREEN}[+] টার্গেট ডোমেইন: {domain}{RESET}")
        print(f"{GREEN}[+] সার্ভার আইপি: {ip}{RESET}")
    except:
        print(f"{RED}[!] আইপি রেজলভ করা যায়নি।{RESET}")

def save_file(url, content, output_dir, is_binary=False):
    try:
        parsed_path = urlparse(url)
        file_path_relative = parsed_path.path.lstrip('/')
        if not file_path_relative or file_path_relative.endswith('/'):
            file_path_relative += "index.html"
        
        local_file_path = os.path.join(output_dir, file_path_relative)
        local_dir = os.path.dirname(local_file_path)

        if local_dir and not os.path.exists(local_dir):
            os.makedirs(local_dir, exist_ok=True)

        mode = "wb" if is_binary else "w"
        encoding = None if is_binary else "utf-8"
        
        with open(local_file_path, mode, encoding=encoding) as f:
            f.write(content)
        return file_path_relative
    except:
        return None

def generate_interactive_dashboard(output_dir, domain_name, all_files):
    dashboard_path = os.path.join(output_dir, "wolfer_dashboard.html")
    
    files_html = ""
    for file_path in sorted(all_files):
        is_asset = file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.mp4', '.mp3', '.zip', '.pdf', '.woff', '.ttf', '.css', '.js'))
        
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.mp4', '.mp3', '.zip', '.pdf', '.woff', '.ttf')):
            action_btn = f'''
                <a href="{file_path}" download class="action-btn download-btn" title="Download Asset">
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
    <title>Wolfer Ultra Dashboard - {domain_name}</title>
    <style>
        body {{ background-color: #0f172a; color: #f8fafc; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; }}
        .container {{ max-width: 950px; margin: auto; background: #1e293b; padding: 30px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }}
        h1 {{ color: #38bdf8; text-align: center; margin-bottom: 5px; }}
        p.sub {{ text-align: center; color: #94a3b8; margin-bottom: 30px; }}
        .file-card {{ background: #334155; padding: 15px 20px; margin-bottom: 12px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; border-left: 4px solid #38bdf8; }}
        .file-name {{ font-family: monospace; font-size: 14px; color: #cbd5e1; word-break: break-all; max-width: 500px; }}
        .actions {{ display: flex; gap: 10px; }}
        .action-btn, .view-btn {{ padding: 8px 14px; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; text-decoration: none; font-size: 13px; transition: 0.2s; }}
        .view-btn {{ background: #0284c7; color: white; }}
        .copy-btn {{ background: #10b981; color: white; }}
        .download-btn {{ background: #8b5cf6; color: white; display: inline-flex; align-items: center; }}
        .action-btn:hover, .view-btn:hover {{ opacity: 0.85; transform: translateY(-1px); }}
        .toast {{ position: fixed; bottom: 20px; right: 20px; background: #10b981; color: white; padding: 10px 20px; border-radius: 6px; display: none; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>⚡ Wolfer Ultra Cloned Architecture</h1>
        <p class="sub">Target: {domain_name}</p>
        <div class="file-list">
            {files_html}
        </div>
    </div>
    <div id="toast" class="toast">Copied to Clipboard!</div>

    <script>
        async function copyCode(btn, filePath) {{
            try {{
                const response = await fetch(filePath);
                const text = await response.text();
                navigator.clipboard.writeText(text);
                
                let originalText = btn.innerText;
                btn.innerText = "✔ Copied!";
                btn.style.background = "#059669";
                setTimeout(() => {{
                    btn.innerText = originalText;
                    btn.style.background = "#10b981";
                }}, 2000);
            }} catch (err) {{
                alert("Failed to copy file content.");
            }}
        }}
    </script>
</body>
</html>
"""
    with open(dashboard_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"\n{GREEN}[✨ ULTRA DASHBOARD CREATED] ব্রাউজারে ওপেন করুন: {dashboard_path}{RESET}")

def crawl_and_mirror(start_url):
    if not start_url.startswith("http"):
        start_url = "https://" + start_url

    get_recon(start_url)
    
    parsed_start = urlparse(start_url)
    domain_name = parsed_start.netloc.replace(":", "_")
    output_dir = f"WolferUltra_{domain_name}"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    visited_urls = set()
    urls_to_visit = [start_url]
    asset_urls = set()
    saved_files_list = set()

    print(f"\n{YELLOW}[*] হাই-স্পিড ফুল-সাইট ক্রলিং শুরু হয়েছে...{RESET}")

    max_pages = 35  # আগের চেয়ে বেশি পেজ ক্রল করার ক্ষমতা
    page_count = 0

    while urls_to_visit and page_count < max_pages:
        current_url = urls_to_visit.pop(0)
        if current_url in visited_urls:
            continue

        visited_urls.add(current_url)
        page_count += 1
        print(f"{CYAN}[Crawling {page_count}] -> {current_url}{RESET}")

        try:
            res = requests.get(current_url, headers=headers, timeout=10)
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
        except:
            continue

    def download_asset(asset_url):
        try:
            r = requests.get(asset_url, headers=headers, timeout=7)
            if r.status_code == 200:
                path = save_file(asset_url, r.content, output_dir, is_binary=True)
                if path:
                    saved_files_list.add(path)
        except:
            pass

    print(f"\n{YELLOW}[*] মাল্টি-থ্রেডিং এর মাধ্যমে মোট {len(asset_urls)} টি অ্যাসেট হাই-স্পিডে নামানো হচ্ছে...{RESET}")
    with ThreadPoolExecutor(max_workers=15) as executor:  # থ্রেড সংখ্যা বাড়িয়ে স্পিড দ্বিগুণ করা হয়েছে
        for asset in asset_urls:
            executor.submit(download_asset, asset)

    generate_interactive_dashboard(output_dir, domain_name, saved_files_list)
    print(f"\n{GREEN}[🎉] আল্টিমেট ক্রলিং ও মিররিং সফলভাবে সম্পন্ন হয়েছে! ফোল্ডার: '{output_dir}'{RESET}")

if __name__ == "__main__":
    banner()
    target = input(f"{CYAN}টার্গেট ওয়েবসাইটের লিংক দিন -> {RESET}")
    crawl_and_mirror(target)
