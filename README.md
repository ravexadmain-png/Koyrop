# ⚡ Wolfer Ultra Web Cloner & Architecture Extractor

**Wolfer tools - koyrop (Ultra v2.0)** হলো একটি হাই-পারফরম্যান্স পাইথন টুল যা যেকোনো ওয়েবসাইটের সম্পূর্ণ সোর্স কোড, সাব-পেজ আর্কিটেকচার এবং হাজার হাজার অ্যাসেট সুপার-ফাস্ট স্পিডে টার্মক্সে ডাউনলোড করতে পারে। 

## 🚀 Ultra Features
* **High-Speed Multi-threading (15 Workers):** দ্রুত ফাইল ডাউনলোডের জন্য এডভান্সড থ্রেডিং ইঞ্জিন।
* **Deep Recursive Crawling:** ব্যাকগ্রাউন্ডের সাব-পেজ ও ফোল্ডারগুলো স্বয়ংক্রিয়ভাবে খুঁজে বের করে।
* **Interactive GUI Dashboard:** এক ক্লিকে কোড কপি করার জন্য **Copy Button** এবং মিডিয়া বা অ্যাসেট ডাউনলোডের জন্য **Download Icon** যুক্ত চমৎকার ড্যাশবোর্ড।
* **Smart Recon:** টার্গেট ডোমেইনের সার্ভার আইপি ও নেটওয়ার্ক স্ট্যাটাস চেক।

## 🛠️ Installation & Usage in Termux

টার্মক্সে টুলটি রান করতে নিচের কমান্ডগুলো দিন:

```bash
pkg update && pkg install git python -y
git clone [https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git](https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git)
cd YOUR-REPO-NAME
pip install -r requirements.txt
python main.py
