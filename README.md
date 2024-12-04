# PyPinger

**PyPinger** is a lightweight Python application designed to efficiently manage and monitor IP addresses through periodic pings. This tool is ideal for tracking connectivity, maintaining logs, and organizing ping results for quick reference.

---

## 🚀 Features
- **Save IP Addresses**  
  Easily store IP addresses to monitor connectivity.

- **Ping Saved IPs**  
  Continuously ping saved IP addresses and track their status.

- **Log Management**  
  - Automatically save ping results in organized text files.  
  - Each IP address has its own dedicated log file.  
  - Logs are grouped by date in folders for easy tracking.  
  - A new folder is created automatically every 24 hours for long-running sessions.  

---

## 🛠 Requirements
- **Python**  
  - Version: 3.12  
  - [Download Python 3.12 from the official site](https://www.python.org/)

---

## 📖 Instructions

1️⃣ **Clone the Repository**
```bash
git clone https://github.com/your-username/PyPinger.git
cd PyPinger
```

2️⃣ **Run the Application**
```bash
python PyPinger.py
```

---

## 📦 **Package as a Standalone Desktop Application**

**Step 1:** Install PyInstaller
```bash
pip install pyinstaller
```

**Step 2:** Create an Executable
```bash
pyinstaller --onefile --noconsole --name "PyPinger" PyPinger.py
```

**Step 3:** Locate the Executable
After running the command, the .exe file will be located in the dist folder.

---

## 🤝 Contributing
Contributions are welcome! Feel free to fork the repository and submit a pull request with your improvements or ideas.

---

## 📝 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Enjoy seamless IP tracking with PyPinger! 🌐
