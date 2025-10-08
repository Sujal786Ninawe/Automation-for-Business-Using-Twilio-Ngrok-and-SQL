from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os
import sqlite3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# ✅ Initialize DB and create table (without redundant sender column)
def init_db():
    conn = sqlite3.connect('customer_responses.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mobile_number TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# ✅ Save incoming message to database
def save_to_db(mobile_number, message):
    conn = sqlite3.connect('customer_responses.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO responses (mobile_number, message)
        VALUES (?, ?)
    ''', (mobile_number, message))
    conn.commit()
    conn.close()

# ✅ WhatsApp webhook endpoint
@app.route("/webhook", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.form.get('Body', '').strip().lower()
    sender = request.form.get('From')                      # e.g., whatsapp:+919876543210
    mobile_number = sender.replace("whatsapp:", "")        # Clean number only

    # ✅ Save to DB
    save_to_db(mobile_number, incoming_msg)
    print(f"Message from {mobile_number}: {incoming_msg}")

    resp = MessagingResponse()
    msg = resp.message()

    # ✅ Chatbot logic
    if 'hi' in incoming_msg or 'hello' in incoming_msg:
        msg.body("👋 Welcome to Bombaywala Sweets!\n\nSend any of the following options:\n- 'official_link'\n- 'catalogue'\n- 'view_cart'\n- 'nearest_location'")
    elif 'official_link' in incoming_msg:
        msg.body("💰 Check out our products here:\nhttps://bombaywalassweets.com/")
    elif 'catalogue' in incoming_msg or 'catalouge' in incoming_msg:  
        msg.body("📄 Here's our Bombaywala Catalogue:")
        msg.media("https://7f03-2401-4900-881c-3fed-e966-c2eb-cf50-b019.ngrok-free.app/static/SweetsCorner.pdf")
    elif 'view_cart' in incoming_msg:
        msg.body("🛒 Here’s your cart:\nhttps://bombaywalassweets.com/wishlist/WOOSW/")
    elif 'nearest_location' in incoming_msg:
        msg.body("📍 Find us here:\nhttps://www.google.com/maps/search/bombaywala/@21.1151583,79.0590503,12z?entry=ttu&g_ep=EgoyMDI1MDQzMC4xIKXMDSoASAFQAw%3D%3D")
    else:
        msg.body("❓ Sorry, I didn't understand that. Please try one of these:\n- 'official_link'\n- 'catalogue'\n- 'view_cart'\n- 'nearest_location'")
    return str(resp)

if __name__ == "__main__":
    init_db()
    app.run(port=8000, debug=True)
