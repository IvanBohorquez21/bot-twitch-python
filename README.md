# Asynchronous Twitch TTS Bot with Concurrent Threading

A high-performance Twitch integration developed in Python that enables real-time Text-to-Speech (TTS) capabilities. This project focuses on solving common concurrency issues between asynchronous API wrappers and synchronous TTS engines using specialized threading techniques.

## ⚙️ Technical Architecture

The bot leverages an **Asynchronous Event Loop** to manage Twitch IRC communications. To prevent the TTS engine (`pyttsx3`) from blocking the main execution thread—which would cause the bot to disconnect—the system utilizes `asyncio.to_thread`. 

### Key Engineering Solutions:
- **Thread Isolation:** The TTS engine is initialized and destroyed within a dedicated worker thread for every call, preventing `RuntimeError: run loop already started` and ensuring memory cleanup.
- **Stateful Cooldown Management:** Implements a time-delta check to throttle command execution and optimize system resources.
- **Input Sanitization:** A multi-layered validation pipeline that checks for message length (max 120 chars) and filters content against a custom blacklist.
- **Graceful Shutdown:** Handles `SIGINT` (Ctrl+C) via exception trapping to ensure all network sockets and local drivers are closed properly without traceback errors.

## 🚀 Features

- **Dynamic TTS Identification:** Automatically prepends the sender's name to the audio output for better stream context.
- **Localized Synthesis:** Configured to prioritize Spanish language neural voices available on the host OS.
- **Security First:** Designed with a modular configuration (via `dontleak.py`) to keep OAuth tokens and Client Secrets out of version control.

## 🛠 Tech Stack

- **Language:** Python 3.10+
- **Protocol:** Twitch WebSocket (via `twitchAPI`)
- **Engine:** SAPI5 / NSSpeech (via `pyttsx3`)
- **Concurrency:** `asyncio` & `threading`

## 📋 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/IvanBohorquez21/bot-twitch-python.git](https://github.com/IvanBohorquez21/bot-twitch-python.git)
   cd bot-twitch-python
    ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
     ```
3. **Configure Environment:**
   Create a dontleak.py file in the root directory:
   ```bash
   client_id = "YOUR_TWITCH_CLIENT_ID"
   client_secret = "YOUR_TWITCH_CLIENT_SECRET"
     ```
4. **Run the application:**
   ```bash
   python main.py
     ```
##📜 License
This project is licensed under the MIT License - see the LICENSE file for details.

---

### ¿Por qué este README te hace ver como un pro?

1.  **Uso de terminología avanzada:** Palabras como *Asynchronous Event Loop*, *Thread Isolation*, *Sanitization* y *Graceful Shutdown* le dicen a cualquier reclutador que sabes de qué estás hablando.
2.  **Explicación del problema técnico:** No solo dices "hice un bot", explicas que resolviste un conflicto de hilos (`asyncio` vs `pyttsx3`), lo cual es un problema de ingeniería real.
3.  **Estructura limpia:** El uso de iconos y bloques de código hace que sea muy fácil de leer (scannable).

### Último paso en GitHub
Para que este texto se vea así de bien en tu perfil:
1. Abre tu archivo `README.md` en VS Code.
2. Borra lo que tenga y pega este nuevo texto.
3. Guarda los cambios.
4. En la terminal escribe:
   ```powershell
   git add README.md
   git commit -m "Docs: Update README with technical architecture details"
   git push origin main
   ```
