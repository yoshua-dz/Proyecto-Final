import streamlit as st
from birthday_manager import BirthdayManager, Birthday
from message_manager import MessageManager
from email_sender import EmailSender
from datetime import datetime, date
import random

st.set_page_config(page_title="Gestor de Cumpleaños")
st.title("🎉 Gestor de Cumpleaños")

b_manager = BirthdayManager("data/birthdays.csv")
m_manager = MessageManager(filepath="data/messages.txt")

def is_today(birthdate):
    """Verifica si hoy es el cumpleaños"""
    today = date.today()
    return birthdate.day == today.day and birthdate.month == today.month

def get_message_for_birthday(birthday):
    if hasattr(birthday, "message") and birthday.message:
        return birthday.message
    else:
        msgs = m_manager.load_messages()
        if msgs:
            return random.choice(msgs)
        else:
            return "¡Feliz cumpleaños!" 

# Configuración del email
with st.sidebar:
    st.header("🔐 Configurar Email")
    smtp_server = st.text_input("SMTP Server", value="smtp.gmail.com")
    smtp_port = st.number_input("Puerto SMTP", value=465)
    sender_email = st.text_input("Tu correo")
    sender_password = st.text_input("Contraseña", type="password")

# Registrar cumpleaños
with st.form("add_birthday"):
    name = st.text_input("Nombre")
    birthdate = st.date_input(
        "Fecha de nacimiento",
        min_value=date(1950, 1, 1),
        max_value=date.today()
    )
    email = st.text_input("Correo electrónico")

    messages = m_manager.load_messages()
    selected_message = st.selectbox(
        "Selecciona un mensaje de cumpleaños (o se enviará uno aleatorio)",
        options=["Elegir al azar"] + messages
    )   

    submitted = st.form_submit_button("Guardar")
    if submitted:
        message_to_save = "" if selected_message == "Elegir al azar" else selected_message
        new_birthday = Birthday(name, birthdate.strftime("%Y-%m-%d"), email, message_to_save)
        b_manager.save_birthday(new_birthday)
        st.success(f"Cumpleaños de {name} guardado correctamente.")

st.subheader("🗑️ Eliminar cumpleaños")

birthdays = b_manager.load_birthdays()
if birthdays:
    for i, b in enumerate(birthdays):
        cols = st.columns([8, 1])
        cols[0].write(f"{b.name} - {b.birthdate.strftime('%d/%m/%Y')} - {b.email}")
        if cols[1].button("Eliminar", key=f"del_birthday_{i}"):
            b_manager.delete_birthday(b.email)
            st.success(f"Cumpleaños de {b.name} eliminado.")
            st.rerun()  # Recarga la app para actualizar la lista
else:
    st.info("No hay cumpleaños registrados.")



# Mostrar próximos cumpleaños
st.subheader("📅 Próximos cumpleaños")
birthdays = b_manager.load_birthdays()
if not birthdays:
    st.info("No hay cumpleaños registrados aún.")
else:
    for b in birthdays:
        days = b.days_until_birthday()
        if is_today(b.birthdate):
            st.success(f"🎂 ¡Hoy es el cumpleaños de {b.name}!")
        else:
            st.write(f"{b.name} ({b.birthdate.strftime('%d/%m')}) - Faltan {days} días")

st.subheader("📨 Enviar felicitaciones automáticamente")
if st.button("Enviar felicitaciones de hoy"):
    sender = EmailSender(smtp_server, smtp_port, sender_email, sender_password)
    any_sent = False
    for b in birthdays:
        if is_today(b.birthdate):
            try:
                # Obtener mensaje personalizado o aleatorio
                if b.message:
                    message = b.message
                else:
                    messages = m_manager.load_messages()
                    message = random.choice(messages) if messages else "¡Feliz cumpleaños!"
                message = message.replace("{nombre}", b.name)

                sender.send_email(b.email, "🎉 ¡Feliz cumpleaños!", message)
                st.success(f"✅ Correo enviado a {b.name} ({b.email})")
                any_sent = True
            except Exception as e:
                st.error(f"❌ No se pudo enviar el correo a {b.name}: {e}")

    if not any_sent:
        st.info("No hay cumpleaños hoy o no se enviaron correos.")



st.subheader("💬 Mensajes de cumpleaños")

new_msg = st.text_area("Agregar nuevo mensaje (usa {nombre} para personalizar)")
if st.button("Guardar mensaje"):
    m_manager.save_message(new_msg)
    st.success("Mensaje guardado correctamente.")

st.write("Mensajes disponibles:")

messages = m_manager.load_messages()

for i, msg in enumerate(messages):
    cols = st.columns([8, 1])
    cols[0].code(msg)
    if cols[1].button("Eliminar", key=f"del_{i}"):
        m_manager.delete_message(msg)
        st.experimental_rerun()  # Recarga la app para actualizar la lista
