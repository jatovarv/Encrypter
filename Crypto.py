 import streamlit as st
import string

# Configuración de la aplicación
st.set_page_config(page_title="Encriptador de Mensajes", layout="centered")

# Definimos el alfabeto
ALPHABET = string.ascii_uppercase
ALPHABET_SIZE = len(ALPHABET)
NUM_GEARS = 6
GEAR_RATIO = 4

# Función para desplazar letras
def shift_letter(letter, shift):
    if letter.upper() not in ALPHABET:
        return letter  # Mantener caracteres no alfabéticos sin cambios
    index = ALPHABET.index(letter.upper())
    new_index = (index + shift) % ALPHABET_SIZE
    return ALPHABET[new_index] if letter.isupper() else ALPHABET[new_index].lower()

# Función para encriptar
def encrypt(message, gear3_position, gear4_position):
    encrypted_message = ""
    gear_positions = [0] * NUM_GEARS
    gear_positions[2] = gear3_position
    gear_positions[3] = gear4_position

    for char in message:
        shift = sum(gear_positions)
        encrypted_message += shift_letter(char, shift)

        gear_positions[0] = (gear_positions[0] + 1) % ALPHABET_SIZE
        for i in range(1, NUM_GEARS):
            if gear_positions[i - 1] % GEAR_RATIO == 0 and gear_positions[i - 1] != 0:
                gear_positions[i] = (gear_positions[i] + 1) % ALPHABET_SIZE

    return encrypted_message

# Función para desencriptar
def decrypt(message, gear3_position, gear4_position):
    decrypted_message = ""
    gear_positions = [0] * NUM_GEARS
    gear_positions[2] = gear3_position
    gear_positions[3] = gear4_position

    for char in message:
        shift = sum(gear_positions)
        decrypted_message += shift_letter(char, -shift)

        gear_positions[0] = (gear_positions[0] + 1) % ALPHABET_SIZE
        for i in range(1, NUM_GEARS):
            if gear_positions[i - 1] % GEAR_RATIO == 0 and gear_positions[i - 1] != 0:
                gear_positions[i] = (gear_positions[i] + 1) % ALPHABET_SIZE

    return decrypted_message

# Interfaz de usuario
st.title("🔐 Encriptador de Mensajes")
st.markdown("Este encriptador utiliza un sistema de sextuple encriptación, con ajustes manuales para 676 posibilidades adicionales de encriptación.")

# Ajuste de los engranajes
gear3_position = st.slider("Posición del Engranaje 3", min_value=0, max_value=25, value=0)
gear4_position = st.slider("Posición del Engranaje 4", min_value=0, max_value=25, value=0)

# Sección para encriptar
st.header("✉️ Encriptar un Mensaje")
message_to_encrypt = st.text_input("Ingresa el mensaje a encriptar")
if st.button("Encriptar"):
    encrypted_message = encrypt(message_to_encrypt, gear3_position, gear4_position)
    st.success(f"Mensaje Encriptado: {encrypted_message}")

# Sección para desencriptar
st.header("🔓 Desencriptar un Mensaje")
message_to_decrypt = st.text_input("Ingresa el mensaje encriptado")
if st.button("Desencriptar"):
    decrypted_message = decrypt(message_to_decrypt, gear3_position, gear4_position)
    st.success(f"Mensaje Desencriptado: {decrypted_message}")

# Footer
st.markdown("---")
st.caption("Developed JATV ❤️ using Python & Streamlit JATV all rights reserved. Contact admin to use source code ;)")
