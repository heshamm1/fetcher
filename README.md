# Fetcher - DNS Subdomain Brute Forcer

![Fetcher](https://img.shields.io/badge/Version-1.0-blue.svg) ![License](https://img.shields.io/badge/License-MIT-green.svg) ![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-yellow.svg)

Fetcher is a **high-performance, DNS-based subdomain brute-forcing tool** that helps discover valid subdomains efficiently.

## 🚀 Features
✅ **Fast & Multi-threaded** - Uses Python's ThreadPoolExecutor  
✅ **DNS-Based** - No HTTP requests, bypasses web firewalls  
✅ **Custom Output File Support** (`-o filename.txt`)  

---

## 🔧 Installation

### **1️⃣ Install via Python (Linux & Windows)**
```bash
pip install -r requirements.txt
```

### **2️⃣ Install as a Package**
```bash
pip install .
```

### **3️⃣ Run the Tool**
```bash
python fetcher.py -d example.com -w wordlist.txt -o results.txt
```

---

## 🔹 Usage Examples

### **Basic Usage**
```bash
python fetcher.py -d example.com -w wordlist.txt
```

### **Enable Fast Mode (More Threads)**
```bash
python fetcher.py -d example.com -w wordlist.txt -f
```

### **Save Output to a Specific File**
```bash
python fetcher.py -d example.com -w wordlist.txt -o output.txt
```

### **Use the Default Timestamped Filename**
```bash
python fetcher.py -d example.com -w wordlist.txt -o
```

### **Scan Multiple Domains from a List**
```bash
python fetcher.py -tl domains.txt -w wordlist.txt
```

---

## 💻 Running as an Executable (No Python Required)

### **🔹 Windows (.exe)**
```powershell
pyinstaller --onefile fetcher.py
./dist/fetcher.exe -d example.com -w wordlist.txt -o results.txt
```

### **🔹 Linux (Shell Script)**
```bash
chmod +x fetcher.sh
./fetcher.sh -d example.com -w wordlist.txt -o results.txt
```

---

## 🛠 Development & Contribution
Want to contribute? Feel free to **fork the repo** and submit a **pull request!**

### **Clone & Setup**
```bash
git clone https://github.com/heshamm1/fetcher.git
cd fetcher
pip install -r requirements.txt
```

### **Run Tests**
```bash
python -m unittest tests/test_fetcher.py
```

---

## 📜 License
This project is licensed under the **MIT License**. See `LICENSE` for details.

---

## 🌟 Support & Issues
Have any issues or suggestions? **Open an issue** on GitHub!

🔗 **GitHub Repo:** [https://github.com/heshamm1/fetcher](https://github.com/heshamm1/fetcher.git)

