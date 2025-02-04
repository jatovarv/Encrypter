import streamlit as st
import string
import hashlib
import random

# Configuración de la aplicación
st.set_page_config(page_title="Encriptador Avanzado de Mensajes", layout="centered")

# Definimos el alfabeto
ALPHABET = string.ascii_uppercase
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

# Generar configuración aleatoria de engranajes
def random_gear_positions():
    return [random.randint(0, ALPHABET_SIZE - 1) for _ in range(NUM_GEARS)]

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

# Generar configuración de engranajes aleatoria
if st.button("🔄 Generar Configuración Aleatoria"):
    gear_positions = random_gear_positions()
    st.success(f"Configuración de Engranajes: {gear_positions}")
else:
    gear_positions_input = st.text_input("Ingresa la Configuración de Engranajes (separada por comas)", "0,0,0,0,0,0")
    gear_positions = [int(pos.strip()) for pos in gear_positions_input.split(",") if pos.strip().isdigit()]
    if len(gear_positions) != NUM_GEARS:
        st.warning("Debe haber exactamente 6 posiciones de engranajes.")

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
