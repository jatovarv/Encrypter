import streamlit as st
import string
import hashlib

# Configuración de la aplicación
st.set_page_config(page_title="Encriptador Avanzado de Mensajes", layout="centered")

# Definimos el alfabeto extendido (A-Z + 0-9)
ALPHABET = string.ascii_uppercase + string.digits
ALPHABET_SIZE = len(ALPHABET)
NUM_GEARS = 6

# Función para desplazar letras
def shift_letter(letter, shift):
    if letter.upper() not in ALPHABET:
        return letter  # Mantener caracteres no alfabéticos sin cambios
    index = ALPHABET.index(letter.upper())
    new_index = (index + shift) % ALPHABET_SIZE
    return ALPHABET[new_index] if letter.isupper() else ALPHABET[new_index].lower()

# Generar configuración de engranajes basada en una clave secreta
def generate_gear_positions(passphrase, num_gears):
    hash_value = hashlib.sha256(passphrase.encode()).hexdigest()
    return [int(hash_value[i:i+2], 16) % ALPHABET_SIZE for i in range(0, num_gears * 2, 2)]

# Función para encriptar
def encrypt(message, gear_positions, passphrase=""):
    if passphrase:
        gear_positions = [(gp + offset) % ALPHABET_SIZE for gp, offset in zip(gear_positions, generate_gear_positions(passphrase, NUM_GEARS))]

    encrypted_message = ""
    for char in message:
        shift = sum(gear_positions)
        encrypted_message += shift_letter(char, shift)

        # Rotación no lineal basada en la suma de posiciones
        gear_positions = [(gp + (shift % (i + 2))) % ALPHABET_SIZE for i, gp in enumerate(gear_positions)]

    return encrypted_message

# Función para desencriptar
def decrypt(message, gear_positions, passphrase=""):
    if passphrase:
        gear_positions = [(gp + offset) % ALPHABET_SIZE for gp, offset in zip(gear_positions, generate_gear_positions(passphrase, NUM_GEARS))]

    decrypted_message = ""
    for char in message:
        shift = sum(gear_positions)
        decrypted_message += shift_letter(char, -shift)

        # Rotación no lineal basada en la suma de posiciones
        gear_positions = [(gp + (shift % (i + 2))) % ALPHABET_SIZE for i, gp in enumerate(gear_positions)]

    return decrypted_message

# Interfaz de usuario
st.title("🔐 Encriptador Avanzado de Mensajes")
st.markdown("Este encriptador utiliza un sistema de 6 engranajes con rotación no lineal y una clave secreta opcional para mayor seguridad.")

# Ingreso manual de las posiciones de los engranajes
st.header("⚙️ Configuración de Engranajes")
gear_positions = []
for i in range(NUM_GEARS):
    position = st.number_input(f"Posición del Engranaje {i + 1}", min_value=0, max_value=35, value=0)
    gear_positions.append(position)

# Ingreso de la clave secreta
passphrase = st.text_input("Frase Clave (opcional para mayor seguridad)", type="password")

# Sección para encriptar
st.header("✉️ Encriptar un Mensaje")
message_to_encrypt = st.text_input("Ingresa el mensaje a encriptar")
if st.button("Encriptar"):
    encrypted_message = encrypt(message_to_encrypt, gear_positions, passphrase)
    st.success(f"Mensaje Encriptado: {encrypted_message}")

# Sección para desencriptar
st.header("🔓 Desencriptar un Mensaje")
message_to_decrypt = st.text_input("Ingresa el mensaje encriptado")
if st.button("Desencriptar"):
    decrypted_message = decrypt(message_to_decrypt, gear_positions, passphrase)
    st.success(f"Mensaje Desencriptado: {decrypted_message}")
    
# Footer
st.markdown("---")
st.caption("Developed JATV ❤️ using Python & Streamlit JATV all rights reserved. Contact admin to use source code ;)")
