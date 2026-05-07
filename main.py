from twitchAPI.chat import Chat, EventData, ChatMessage, ChatCommand
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.oauth import UserAuthenticator 
from twitchAPI.twitch import Twitch
import asyncio
import pyttsx3
import dontleak
import time

# --- CONFIGURACIÓN ---
TARGET_CHANNEL = 'player_blackstar'
COOLDOWN_SECONDS = 5
MAX_CHARACTERS = 120
last_use_time = 0

# Lista de palabras prohibidas
BLACKLIST = ['groseria1', 'insulto2', 'palabra3']

# --- FUNCIÓN DE VOZ (TTS) ---
def hablar(texto):
    """Crea un motor temporal para evitar el error 'run loop already started'"""
    try:
        nuevo_engine = pyttsx3.init()
        
        # Configurar voz en español
        voices = nuevo_engine.getProperty('voices')
        for voice in voices:
            if 'spanish' in voice.name.lower() or 'espanol' in voice.name.lower():
                nuevo_engine.setProperty('voice', voice.id)
                break
        
        nuevo_engine.setProperty('rate', 160)
        nuevo_engine.setProperty('volume', 1.0)
        
        nuevo_engine.say(texto)
        nuevo_engine.runAndWait()
        nuevo_engine.stop()
    except Exception as e:
        print(f"Error en el motor de voz: {e}")

# --- EVENTOS ---
async def on_message(msg: ChatMessage):
    print(f'[{msg.user.display_name}]: {msg.text}')

async def on_ready(ready_event: EventData):
    await ready_event.chat.join_room(TARGET_CHANNEL)
    print(f'--- Bot Conectado a {TARGET_CHANNEL} ---')

# --- COMANDO !habla ---
async def habla_command(cmd: ChatCommand):
    global last_use_time
    
    # 1. Verificar Cooldown
    current_time = time.time()
    if current_time - last_use_time < COOLDOWN_SECONDS:
        print(f"Cooldown: faltan {int(COOLDOWN_SECONDS - (current_time - last_use_time))}s")
        return

    # 2. Verificar si el mensaje está vacío
    if len(cmd.parameter) == 0:
        await cmd.reply("¡Dime qué quieres que diga! Uso: !habla [texto]")
        return

    # 3. Verificar límite de caracteres
    if len(cmd.parameter) > MAX_CHARACTERS:
        await cmd.reply(f"Mensaje muy largo (máx {MAX_CHARACTERS} caracteres).")
        return

    # 4. Filtro de Groserías
    mensaje_minus = cmd.parameter.lower()
    if any(palabra in mensaje_minus for palabra in BLACKLIST):
        await cmd.reply("No puedo decir eso, mantén el respeto.")
        return

    # 5. Identificar usuario y ejecutar
    usuario = cmd.user.display_name
    texto_final = f"{usuario} dice: {cmd.parameter}"
    
    print(f'Leyendo: "{texto_final}"')
    last_use_time = current_time 
    
    # Ejecutar en hilo separado para no bloquear el chat
    await asyncio.to_thread(hablar, texto_final)

# --- FUNCIÓN PRINCIPAL ---
async def run_bot():
    # Inicialización
    bot = await Twitch(dontleak.client_id, dontleak.client_secret)
    scopes = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT, AuthScope.CHANNEL_MANAGE_BROADCAST]
    
    # Autenticación
    auth = UserAuthenticator(bot, scopes)
    token, refresh_token = await auth.authenticate()
    await bot.set_user_authentication(token, scopes, refresh_token)

    # Configurar Chat
    chat = await Chat(bot)
    chat.register_event(ChatEvent.READY, on_ready)
    chat.register_event(ChatEvent.MESSAGE, on_message)
    chat.register_command('habla', habla_command)

    chat.start()

    try:
        # Espera asíncrona infinita
        await asyncio.Event().wait()
    except (asyncio.CancelledError, KeyboardInterrupt):
        # Captura el cierre para que no salte el error rojo
        print("\n[!] Deteniendo el bot...")
    finally:
        await chat.stop()
        await bot.close()
        print("[v] Bot desconectado correctamente.")

if __name__ == '__main__':
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        # Manejo final para salir a la consola de Windows sin rastro de error
        pass