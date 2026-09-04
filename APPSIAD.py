import streamlit as st
import sqlite3
import hashlib
import random
import pandas as pd
import numpy as np
import plotly.express as px
import requests
import textwrap
VIP_BADGE_B64 = "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"

from datetime import datetime, timedelta

try:
    from streamlit_autorefresh import st_autorefresh
except ImportError:
    st_autorefresh = None

def clean_html(html_str):
    import re
    # Remove escaped quotes
    cleaned = html_str.replace('\\"', '"').replace('\"', '"')
    # Replace newlines with space
    cleaned = cleaned.replace('\n', ' ').replace('\r', ' ')
    # Replace multiple spaces with a single space
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned.strip()



# Configuración de página de Streamlit
st.set_page_config(
    page_title="Alianza CryptoWallet v64",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

if st_autorefresh is not None:
    st_autorefresh(interval=10000, key="datarefresh") # Auto-refresh every 10 seconds





# --- BASE DE DATOS Y CONFIGURACIÓN ---

def init_db():
    conn = sqlite3.connect("wallet_pro.db", timeout=30)
    cursor = conn.cursor()
    # Tabla de usuarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            fullname TEXT,
            email TEXT,
            wallet_code TEXT UNIQUE,
            balance REAL DEFAULT 0.0,
            is_admin INTEGER DEFAULT 0,
            balance_cop REAL DEFAULT 0.0,
            is_vip INTEGER DEFAULT 0,
            nequi_number TEXT DEFAULT '',
            referred_by TEXT
        )
    """)
    # Tabla de transacciones
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_code TEXT,
            receiver_code TEXT,
            amount REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Tabla de configuraciones del token personalizado
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS token_settings (
            id INTEGER PRIMARY KEY DEFAULT 1,
            token_name TEXT DEFAULT 'SIAD',
            token_symbol TEXT DEFAULT 'SD',
            token_contract TEXT DEFAULT '0xC324649213ec1757190bc4b78bcD41Cc1545C264',
            token_price_usd REAL DEFAULT 0.50,
            nequi_number TEXT DEFAULT '3001234567'
        )
    """)
    # Tabla de solicitudes de compra (Comprobantes)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS purchase_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_code TEXT,
            amount_cop REAL,
            amount_sd REAL,
            proof_image BLOB,
            status TEXT DEFAULT 'PENDING',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Tabla de comisiones por referidos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS referral_rewards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            referrer_code TEXT,
            referred_code TEXT,
            purchase_id INTEGER,
            purchase_amount_sd REAL,
            reward_amount_sd REAL,
            status TEXT DEFAULT 'PENDING',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Tabla de solicitudes de retiro (Withdrawals)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS withdrawal_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_code TEXT,
            amount_cop REAL,
            fee_cop REAL,
            net_cop REAL,
            nequi_number TEXT,
            receipt_image BLOB,
            status TEXT DEFAULT 'PENDING',
            fee_status TEXT DEFAULT 'UNCLAIMED',
            approved_at DATETIME,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tabla de notificaciones del usuario
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_code TEXT,
            message TEXT,
            status TEXT DEFAULT 'UNREAD',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tabla de pagos de móviles (Mensajería)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movil_payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_code TEXT,
            payment_type TEXT,
            amount_sd REAL,
            amount_cop REAL,
            target_code TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tabla de artículos de la tienda (Store)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS store_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            price_sd REAL,
            item_type TEXT
        )
    """)
    
    # Tabla de compras en la tienda
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS store_purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_code TEXT,
            item_id INTEGER,
            price_sd REAL,
            status TEXT DEFAULT 'PENDING',
            code_delivered TEXT DEFAULT '',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(item_id) REFERENCES store_items(id)
        )
    """)
    
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN balance_cop REAL DEFAULT 0.0")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE users ADD COLUMN referred_by TEXT")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE users ADD COLUMN is_vip INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE movil_payments ADD COLUMN message TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE users ADD COLUMN nequi_number TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass
        
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS store_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                description TEXT,
                price_sd REAL,
                item_type TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS store_purchases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_code TEXT,
                item_id INTEGER,
                price_sd REAL,
                status TEXT DEFAULT 'PENDING',
                code_delivered TEXT DEFAULT '',
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(item_id) REFERENCES store_items(id)
            )
        """)
    except Exception:
        pass

    try:
        cursor.execute("ALTER TABLE withdrawal_requests ADD COLUMN approved_at DATETIME")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE withdrawal_requests ADD COLUMN fee_status TEXT DEFAULT 'UNCLAIMED'")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE users ADD COLUMN bsc_address TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass

    # Migraciones inteligentes en caso de que ya existan las tablas sin las nuevas columnas o tablas
    try:
        cursor.execute("ALTER TABLE token_settings ADD COLUMN nequi_number TEXT DEFAULT '3001234567'")
    except sqlite3.OperationalError:
        pass 
        
    try:
        
        cursor.execute("UPDATE token_settings SET token_name = 'SIAD', token_symbol = 'SD', token_contract = '0xC324649213ec1757190bc4b78bcD41Cc1545C264' WHERE id = 1")

    except Exception:
        pass

    # Insertar artículos de la tienda por defecto si está vacía
    try:
        cursor.execute("SELECT COUNT(*) FROM store_items")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO store_items (name, description, price_sd, item_type) VALUES 
                ('Membresía VIP Alianza', '🔒 Reduce comisión de retiros a Nequi al 1% y aumenta tu bono de referidos al 25% de por vida.', 50.0, 'MEMBERSHIP'),
                ('Netflix Premium (1 Mes)', '🎬 Pin digital para canjear 1 mes de Netflix Premium en cualquier cuenta.', 30.0, 'GIFT_CARD'),
                ('Spotify Premium (1 Mes)', '🎵 Código oficial de 1 mes de Spotify Premium para tu cuenta.', 15.0, 'GIFT_CARD'),
                ('Free Fire (100 Diamantes)', '🔥 Recarga inmediata de 100 diamantes de Free Fire usando tu ID de jugador.', 8.0, 'GIFT_CARD'),
                ('Roblox (400 Robux)', '🎮 Código de tarjeta de regalo digital de Roblox de 400 Robux.', 12.0, 'GIFT_CARD')
            """)
    except Exception:
        pass

    # Insertar configuración por defecto si está vacía
    cursor.execute("SELECT COUNT(*) FROM token_settings")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO token_settings (id, token_name, token_symbol, token_contract, token_price_usd, nequi_number)
            VALUES (1, 'SIAD', 'SD', '0xC324649213ec1757190bc4b78bcD41Cc1545C264', 0.50, '3001234567')
        """)
    
    # Crear un administrador por defecto si no existe
    
    # Tabla: game_settings (para configuraciones de los juegos)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS game_settings (
            setting_key TEXT PRIMARY KEY,
            value_text TEXT,
            value_numeric REAL
        )
    """)
    # Tabla: trivias (para trivias dinámicas activas)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trivias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            option_a TEXT,
            option_b TEXT,
            option_c TEXT,
            correct_option TEXT,
            entry_fee REAL,
            prize_sd REAL,
            active INTEGER DEFAULT 1
        )
    """)
    # Tabla: intentos de trivia del usuario para evitar spam
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_trivia_attempts (
            user_code TEXT,
            trivia_id INTEGER,
            is_correct INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_code, trivia_id)
        )
    """)
    # Tabla: sports_bets (para predicciones deportivas)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sports_bets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            match_name TEXT,
            ticket_cost REAL,
            prize_sd REAL,
            status TEXT DEFAULT 'ACTIVE',
            winner_option TEXT DEFAULT '',
            local_team TEXT DEFAULT '',
            visitor_team TEXT DEFAULT '',
            match_time TEXT DEFAULT '',
            ends_at TEXT DEFAULT '',
            current_score TEXT DEFAULT '0 - 0',
            match_status TEXT DEFAULT 'No iniciado'
        )
    """)
    try:
        cursor.execute("ALTER TABLE sports_bets ADD COLUMN local_team TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE sports_bets ADD COLUMN visitor_team TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE sports_bets ADD COLUMN match_time TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE sports_bets ADD COLUMN ends_at TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE sports_bets ADD COLUMN current_score TEXT DEFAULT '0 - 0'")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE sports_bets ADD COLUMN match_status TEXT DEFAULT 'No iniciado'")
    except sqlite3.OperationalError:
        pass
    # Tabla: user_predictions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_code TEXT,
            match_id INTEGER,
            prediction TEXT,
            status TEXT DEFAULT 'PENDING',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(match_id) REFERENCES sports_bets(id)
        )
    """)
    # Tabla: penny_auctions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS penny_auctions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT,
            description TEXT,
            current_price REAL,
            highest_bidder TEXT,
            ends_at DATETIME,
            bid_fee_sd REAL,
            bid_increment REAL,
            status TEXT DEFAULT 'ACTIVE'
        )
    """)
    # Tabla: user_unlocked_tips
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_unlocked_tips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_code TEXT,
            tip_id TEXT,
            unlocked_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    try:
        cursor.execute("ALTER TABLE store_items ADD COLUMN delivery_fee_sd REAL DEFAULT 0.0")
    except sqlite3.OperationalError:
        pass

    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        hashed_pw = hashlib.sha256("admin123".encode()).hexdigest()
        cursor.execute("""
            INSERT INTO users (username, password, fullname, email, wallet_code, balance, is_admin)
            VALUES ('admin', ?, 'Propietario de la App', 'admin@cryptowallet.com', '99999', 10000000.0, 1)
        """, (hashed_pw,))
    
    # Insertar artículos de la tienda adicionales (FOOD, CARRIER_RECHARGE) si están vacíos
    try:
        cursor.execute("SELECT COUNT(*) FROM store_items WHERE item_type = 'FOOD'")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO store_items (name, description, price_sd, item_type, delivery_fee_sd) VALUES 
                ('Combo Tinto y Empanada Express', '☕ Un tinto bien caliente con una deliciosa empanada crujiente de carne. El tinto perfecto para la calle.', 3.0, 'FOOD', 1.0),
                ('Almuerzo Corriente Alianza', '🍲 Sopa del día, bandeja con fríjol, arroz, ensalada, carne asada, pollo frito o cerdo, y jugo natural bien helado.', 8.0, 'FOOD', 2.0)
            """)
    except Exception:
        pass

    try:
        cursor.execute("SELECT COUNT(*) FROM store_items WHERE item_type = 'CARRIER_RECHARGE'")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO store_items (name, description, price_sd, item_type, delivery_fee_sd) VALUES 
                ('Paquete Claro Todo Incluido 3 Días', '📱 Minutos ilimitados, WhatsApp y redes sociales incluidas + 2GB de navegación para trabajar sin parar.', 4.0, 'CARRIER_RECHARGE', 0.0),
                ('Paquete Tigo Datos Express 1 Día', '⚡ Navegación ilimitada por 24 horas consecutivas para conductores en moto.', 2.5, 'CARRIER_RECHARGE', 0.0)
            """)
    except Exception:
        pass

    # Insertar configuración por defecto para juegos
    try:
        cursor.execute("SELECT COUNT(*) FROM game_settings")
        if cursor.fetchone()[0] == 0:
            cursor.executemany("""
                INSERT OR IGNORE INTO game_settings (setting_key, value_text, value_numeric) VALUES (?, ?, ?)
            """, [
                ('ruleta_cost', '', 1.0),
                ('ruleta_prizes', '0.1,0.5,1.0,2.0,5.0,0.0', 0.0),
                ('ruleta_prob', '20,30,25,15,5,5', 0.0),
                ('ppt_multiplier', '', 1.90),
                ('scratch_cost', '', 0.5),
                ('scratch_prizes', '0.0,0.2,0.5,1.0,3.0,10.0', 0.0),
                ('scratch_prob', '50,25,15,7,2,1', 0.0),
                ('crypto_tip_cost', '', 0.2),
                ('crypto_tip', '🔑 Consejo Cripto del Día: ¡No guardes todas tus criptomonedas en un solo exchange! Diversifica usando MetaMask y billeteras frías para tener el control total de tus llaves privadas.', 0.0)
            ])
    except Exception:
        pass

    try:
        cursor.execute("SELECT COUNT(*) FROM trivias WHERE question LIKE '%volar%'")
        if cursor.fetchone()[0] == 0:
            cursor.execute("UPDATE trivias SET active = 0")
            cursor.execute("""
                INSERT INTO trivias (question, option_a, option_b, option_c, correct_option, entry_fee, prize_sd, active) VALUES 
                ('¿Qué mamífero es conocido por ser el único capaz de volar de forma activa y sostenida?', 'La ardilla voladora', 'El murciélago', 'El ornitorrinco', 'B', 0.50, 1.50, 1)
            """)
    except Exception:
        pass

    try:
        cursor.execute("SELECT COUNT(*) FROM sports_bets")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT OR IGNORE INTO sports_bets (match_name, ticket_cost, prize_sd, status, local_team, visitor_team, match_time, ends_at, current_score, match_status) VALUES 
                ('Colombia vs. Brasil (Clasificatorias)', 1.0, 3.0, 'ACTIVE', 'Colombia', 'Brasil', 'Hoy 18:00', 'Hoy 20:00', '0 - 0', 'No iniciado')
            """)
    except Exception:
        pass

    try:
        cursor.execute("SELECT COUNT(*) FROM penny_auctions")
        if cursor.fetchone()[0] == 0:
            ends_at_str = (datetime.utcnow() + timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("""
                INSERT OR IGNORE INTO penny_auctions (item_name, description, current_price, highest_bidder, ends_at, bid_fee_sd, bid_increment, status) VALUES 
                ('Tarjeta Regalo Netflix 1 Mes', '🎬 Pin digital de Netflix Premium para disfrutar de series y películas.', 1.0, '99999', ?, 0.1, 0.05, 'ACTIVE')
            """, (ends_at_str,))
    except Exception:
        pass

    conn.commit()
    conn.close()

init_db()

# Funciones auxiliares de base de datos
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_db_connection():
    return sqlite3.connect("wallet_pro.db", timeout=30)

def generate_unique_wallet_code():
    conn = get_db_connection()
    cursor = conn.cursor()
    while True:
        code = str(random.randint(10000, 99999))
        cursor.execute("SELECT 1 FROM users WHERE wallet_code = ?", (code,))
        if not cursor.fetchone():
            conn.close()
            return code

def get_token_settings():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT token_name, token_symbol, token_contract, token_price_usd, nequi_number FROM token_settings WHERE id = 1")
    settings = cursor.fetchone()
    conn.close()
    if settings:
        return {
            "name": settings[0],
            "symbol": settings[1],
            "contract": settings[2],
            "price_usd": settings[3],
            "nequi_number": settings[4]
        }
    return {
        "name": "SIAD",
        "symbol": "SD",
        "contract": "0xC324649213ec1757190bc4b78bcD41Cc1545C264",
        "price_usd": 0.50,
        "nequi_number": "3001234567"
    }

def update_token_settings(name, symbol, contract, price_usd, nequi_number):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE token_settings 
        SET token_name = ?, token_symbol = ?, token_contract = ?, token_price_usd = ?, nequi_number = ?
        WHERE id = 1
    """, (name, symbol, contract, price_usd, nequi_number))
    conn.commit()
    conn.close()

def update_store_item_price(item_id, price_sd, name, description, delivery_fee_sd=0.0):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE store_items 
        SET price_sd = ?, name = ?, description = ?, delivery_fee_sd = ? 
        WHERE id = ?
    """, (price_sd, name, description, delivery_fee_sd, item_id))
    conn.commit()
    conn.close()
    return True

# Gestión de solicitudes de compra
def submit_purchase_request(user_code, amount_cop, amount_sd, image_bytes):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO purchase_requests (user_code, amount_cop, amount_sd, proof_image, status)
        VALUES (?, ?, ?, ?, 'PENDING')
    """, (user_code, amount_cop, amount_sd, image_bytes))
    conn.commit()
    conn.close()

def get_pending_purchases():
    conn = get_db_connection()
    df = pd.read_sql_query("""
        SELECT p.id, p.user_code, p.amount_cop, p.amount_sd, p.proof_image, p.timestamp, u.fullname, u.username
        FROM purchase_requests p
        JOIN users u ON p.user_code = u.wallet_code
        WHERE p.status = 'PENDING'
        ORDER BY p.timestamp ASC
    """, conn)
    conn.close()
    return df

# Gestión de Comisiones por Referidos
def get_pending_referral_rewards():
    conn = get_db_connection()
    df = pd.read_sql_query("""
        SELECT r.id, r.referrer_code, r.referred_code, r.purchase_amount_sd, r.reward_amount_sd, r.timestamp,
               u1.fullname as referrer_name, u2.fullname as referred_name
        FROM referral_rewards r
        JOIN users u1 ON r.referrer_code = u1.wallet_code
        JOIN users u2 ON r.referred_code = u2.wallet_code
        WHERE r.status = 'PENDING'
        ORDER BY r.timestamp ASC
    """, conn)
    conn.close()
    return df

def approve_referral_reward(reward_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT referrer_code, reward_amount_sd, referred_code FROM referral_rewards WHERE id = ?", (reward_id,))
    res = cursor.fetchone()
    if res:
        referrer_code, reward_amount_sd, referred_code = res
        cursor.execute("UPDATE referral_rewards SET status = 'APPROVED' WHERE id = ?", (reward_id,))
        conn.commit()
        conn.close()
        
        # Enviar comisiones desde la billetera maestra (99999)
        success, msg = send_points("99999", referrer_code, reward_amount_sd)
        if success:
            # Obtener nombre del referido
            conn2 = get_db_connection()
            cursor2 = conn2.cursor()
            cursor2.execute("SELECT fullname FROM users WHERE wallet_code = ?", (referred_code,))
            ref_user = cursor2.fetchone()
            referred_name = ref_user[0] if ref_user else "Tu referido"
            conn2.close()
            
            add_notification(
                referrer_code,
                f"💰 <b>¡Comisión de Referido Recibida!</b> El administrador ha liberado tu comisión de "
                f"<b>{format_num(reward_amount_sd)} SD</b> por la compra de tu referido <b>{referred_name}</b>. ¡Gracias por expandir nuestra comunidad!"
            )
            
            # Enviar notificación al admin de que ya la pagó
            add_notification(
                "99999",
                f"👥 <b>Comisión Pagada:</b> Se han transferido con éxito <b>{format_num(reward_amount_sd)} SD</b> de comisión al referidor <b>{referrer_code}</b>."
            )
        return success, msg
    conn.close()
    return False, "No se encontró el registro de la comisión."

def reject_referral_reward(reward_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE referral_rewards SET status = 'REJECTED' WHERE id = ?", (reward_id,))
    conn.commit()
    conn.close()
    return True

# Sistema de Notificaciones
def add_notification(user_code, message):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notifications (user_code, message) VALUES (?, ?)", (user_code, message))
    conn.commit()
    conn.close()

def broadcast_notification(message):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT wallet_code FROM users WHERE is_admin = 0")
    users = cursor.fetchall()
    for user in users:
        user_code = user[0]
        cursor.execute("INSERT INTO notifications (user_code, message) VALUES (?, ?)", (user_code, message))
    conn.commit()
    conn.close()


def get_unread_notifications_count(user_code):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM notifications WHERE user_code = ? AND status = 'UNREAD'", (user_code,))
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_user_notifications(user_code):
    conn = get_db_connection()
    df = pd.read_sql_query("""
        SELECT id, message, status, timestamp 
        FROM notifications 
        WHERE user_code = ? 
        ORDER BY timestamp DESC
    """, conn, params=(user_code,))
    conn.close()
    return df

def mark_notifications_as_read(user_code):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE notifications SET status = 'READ' WHERE user_code = ?", (user_code,))
    conn.commit()
    conn.close()

# --- FUNCIONES DE LA TIENDA Alianza ---

def get_user_purchases(user_code):
    conn = get_db_connection()
    df = pd.read_sql_query("""
        SELECT id, amount_cop, amount_sd, proof_image, status, timestamp as Fecha
        FROM purchase_requests
        WHERE user_code = ?
        ORDER BY timestamp DESC
    """, conn, params=(user_code,))
    conn.close()
    return df

def buy_store_item(user_code, item_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Obtener precio, tipo y costo de envío del artículo
    try:
        cursor.execute("SELECT name, price_sd, item_type, delivery_fee_sd FROM store_items WHERE id = ?", (item_id,))
        item = cursor.fetchone()
    except Exception:
        cursor.execute("SELECT name, price_sd, item_type, 0.0 as delivery_fee_sd FROM store_items WHERE id = ?", (item_id,))
        item = cursor.fetchone()
    if not item:
        conn.close()
        return False, "El artículo seleccionado no existe."
    
    item_name, price_sd, item_type, delivery_fee_sd = item
    if delivery_fee_sd is None:
        delivery_fee_sd = 0.0
        
    total_cost_sd = price_sd
    if item_type == 'FOOD':
        total_cost_sd = price_sd + delivery_fee_sd
    
    # 2. Verificar si ya es VIP si intenta comprar membresía VIP
    if item_type == 'MEMBERSHIP':
        cursor.execute("SELECT is_vip FROM users WHERE wallet_code = ?", (user_code,))
        user_vip = cursor.fetchone()
        if user_vip and user_vip[0] == 1:
            conn.close()
            return False, "Ya eres un miembro VIP de Alianza."
            
    # 3. Verificar saldo del usuario
    cursor.execute("SELECT balance FROM users WHERE wallet_code = ?", (user_code,))
    balance_row = cursor.fetchone()
    if not balance_row or balance_row[0] < total_cost_sd:
        conn.close()
        return False, f"Saldo de tokens SIAD (SD) insuficiente para realizar esta compra (Se requiere {format_num(total_cost_sd)} SD)."
        
    try:
        # 4. Descontar balance de SD del usuario, sumarlo al del admin (99999)
        cursor.execute("UPDATE users SET balance = balance - ? WHERE wallet_code = ?", (total_cost_sd, user_code))
        cursor.execute("UPDATE users SET balance = balance + ? WHERE wallet_code = '99999'", (total_cost_sd,))
        
        # 5. Registrar la compra en store_purchases
        cursor.execute("""
            INSERT INTO store_purchases (user_code, item_id, price_sd, status)
            VALUES (?, ?, ?, 'PENDING')
        """, (user_code, item_id, total_cost_sd))
        purchase_id = cursor.lastrowid
        
        # 6. Registrar la transacción en el historial de transacciones (User -> Admin)
        cursor.execute("""
            INSERT INTO transactions (sender_code, receiver_code, amount)
            VALUES (?, '99999_STORE_BUY', ?)
        """, (user_code, total_cost_sd))
        
        conn.commit()
        conn.close()
        
        # 7. Notificación al usuario
        add_notification(
            user_code,
            f"🛍️ <b>¡Pedido recibido!</b> Has comprado <b>{item_name}</b> por <b>{format_num(total_cost_sd)} SD</b> "
            f"(Envío: {format_num(delivery_fee_sd)} SD incluido). "
            f"Tu pedido se encuentra pendiente de entrega por el administrador."
        )
        return True, "Compra registrada con éxito. Se encuentra en espera de entrega por el administrador."
    except Exception as e:
        conn.rollback()
        conn.close()
        return False, f"Error al procesar la compra: {str(e)}" 

def deliver_store_purchase(purchase_id, code_delivered=""):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.user_code, p.item_id, p.price_sd, i.name, i.item_type 
        FROM store_purchases p 
        JOIN store_items i ON p.item_id = i.id 
        WHERE p.id = ? AND p.status = 'PENDING'
    """, (purchase_id,))
    purchase = cursor.fetchone()
    
    if purchase:
        user_code, item_id, price_sd, item_name, item_type = purchase
        try:
            # Si el artículo es membresía VIP, activar VIP en el usuario de inmediato
            if item_type == 'MEMBERSHIP':
                cursor.execute("UPDATE users SET is_vip = 1 WHERE wallet_code = ?", (user_code,))
                # ¡Devolver el valor de la membresía en tokens SD como cashback / reembolso de bienvenida, deduciendo del admin 99999!
                cursor.execute("UPDATE users SET balance = balance + ? WHERE wallet_code = ?", (price_sd, user_code))
                cursor.execute("UPDATE users SET balance = balance - ? WHERE wallet_code = '99999'", (price_sd,))
                # Registrar el reembolso en la tabla de transacciones
                cursor.execute("""
                    INSERT INTO transactions (sender_code, receiver_code, amount)
                    VALUES ('99999_STORE_REFUND', ?, ?)
                """, (user_code, price_sd))
                msg_notif = f"👑 <b>¡Membresía VIP Activada!</b> El administrador aprobó tu membresía VIP de Alianza. " \
                            f"Por ser un beneficio VIP de bienvenida, te hemos reembolsado el 100% de su valor: <b>{format_num(price_sd)} SD</b> ($30.00 USD) de inmediato a tu cuenta. " \
                            f"Ahora tus comisiones de retiro se reducen al 1% y tus ganancias de referidos aumentan al 25% de por vida. ¡Disfruta tus privilegios!"
            else:
                msg_notif = f"🎁 <b>¡Tu pedido ha sido entregado!</b> Has recibido tu <b>{item_name}</b>. "                             f"<b>Código/Pin de Activación:</b> <code style='font-size:1.1rem; color:#ffd700;'>{code_delivered}</code>. ¡Gracias por usar la tienda Alianza!"
            
            # Actualizar estado de la compra
            cursor.execute("UPDATE store_purchases SET status = 'DELIVERED', code_delivered = ? WHERE id = ?", (code_delivered, purchase_id))
            conn.commit()
            conn.close()
            
            # Notificar al usuario
            add_notification(user_code, msg_notif)
            return True, "Pedido entregado con éxito."
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, f"Error al procesar la entrega: {str(e)}"
    conn.close()
    return False, "No se encontró el pedido o ya fue procesado."

def reject_store_purchase(purchase_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.user_code, p.price_sd, i.name 
        FROM store_purchases p 
        JOIN store_items i ON p.item_id = i.id 
        WHERE p.id = ? AND p.status = 'PENDING'
    """, (purchase_id,))
    purchase = cursor.fetchone()
    
    if purchase:
        user_code, price_sd, item_name = purchase
        try:
            # Reembolsar los tokens SD al usuario, descontándolos de la cuenta del admin (99999)
            cursor.execute("UPDATE users SET balance = balance + ? WHERE wallet_code = ?", (price_sd, user_code))
            cursor.execute("UPDATE users SET balance = balance - ? WHERE wallet_code = '99999'", (price_sd,))
            
            # Registrar transacción de devolución en transactions (Admin -> User)
            cursor.execute("""
                INSERT INTO transactions (sender_code, receiver_code, amount)
                VALUES ('99999_STORE_REFUND', ?, ?)
            """, (user_code, price_sd))
            
            # Actualizar estado a REJECTED
            cursor.execute("UPDATE store_purchases SET status = 'REJECTED' WHERE id = ?", (purchase_id,))
            conn.commit()
            conn.close()
            
            # Notificar al usuario
            add_notification(
                user_code,
                f"🔴 <b>Pedido Cancelado:</b> Tu compra de <b>{item_name}</b> fue rechazada y reembolsada. "
                f"Se han devuelto <b>{format_num(price_sd)} SD</b> intactos a tu billetera."
            )
            return True
        except Exception as e:
            conn.rollback()
            conn.close()
            return False
    conn.close()
    return False

def get_pending_store_purchases():
    conn = get_db_connection()
    df = pd.read_sql_query("""
        SELECT p.id, p.user_code, p.item_id, p.price_sd, p.timestamp, i.name, i.item_type, u.fullname, u.username
        FROM store_purchases p
        JOIN store_items i ON p.item_id = i.id
        JOIN users u ON p.user_code = u.wallet_code
        WHERE p.status = 'PENDING'
        ORDER BY p.timestamp ASC
    """, conn)
    conn.close()
    return df

def get_user_store_purchases(user_code):
    conn = get_db_connection()
    df = pd.read_sql_query("""
        SELECT p.id, p.price_sd, p.status, p.code_delivered, p.timestamp, i.name, i.item_type
        FROM store_purchases p
        JOIN store_items i ON p.item_id = i.id
        WHERE p.user_code = ?
        ORDER BY p.timestamp DESC
    """, conn, params=(user_code,))
    conn.close()
    return df

def approve_purchase(request_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.user_code, p.amount_sd, p.amount_cop, u.fullname, u.referred_by 
        FROM purchase_requests p 
        JOIN users u ON p.user_code = u.wallet_code 
        WHERE p.id = ?
    """, (request_id,))
    req = cursor.fetchone()
    if req:
        user_code, amount_sd, amount_cop, fullname, referred_by = req
        # Actualizar estado de la solicitud
        cursor.execute("UPDATE purchase_requests SET status = 'APPROVED' WHERE id = ?", (request_id,))
        conn.commit()
        conn.close()
        
        # Enviar los tokens desde la billetera maestra (99999) al comprador
        success, msg = send_points("99999", user_code, amount_sd)
        if success:
            # Enviar notificación oficial de aprobación al comprador
            add_notification(
                user_code, 
                f"🟢 <b>¡Compra aprobada con éxito!</b> El administrador validó tu transferencia de <b>${amount_cop:,.0f} COP</b>. "
                f"Se han acreditado <b>{format_num(amount_sd)} SD</b> directamente a tu billetera."
            )
            
            # Si tiene un referidor válido, calcular el 20% (o 25% si es VIP) y crear registro de comisión pendiente
            if referred_by:
                conn2 = get_db_connection()
                cursor2 = conn2.cursor()
                cursor2.execute("SELECT is_vip FROM users WHERE wallet_code = ?", (referred_by,))
                ref_vip_row = cursor2.fetchone()
                is_ref_vip = ref_vip_row[0] if ref_vip_row else 0
                ref_pct = 0.25 if is_ref_vip == 1 else 0.20
                reward_amount_sd = amount_sd * ref_pct
                conn2 = get_db_connection()
                cursor2 = conn2.cursor()
                cursor2.execute("""
                    INSERT INTO referral_rewards (referrer_code, referred_code, purchase_id, purchase_amount_sd, reward_amount_sd, status)
                    VALUES (?, ?, ?, ?, ?, 'PENDING')
                """, (referred_by, user_code, request_id, amount_sd, reward_amount_sd))
                
                # Obtener nombre del referidor
                cursor2.execute("SELECT fullname FROM users WHERE wallet_code = ?", (referred_by,))
                ref_user = cursor2.fetchone()
                referrer_fullname = ref_user[0] if ref_user else "Referidor"
                conn2.commit()
                conn2.close()
                
                # Enviar notificación al administrador (usuario '99999')
                add_notification(
                    "99999",
                    f"👥 <b>¡Comisión Pendiente de Referidos!</b> El usuario referido <b>{fullname}</b> ({user_code}) "
                    f"compró y fue aprobado por <b>{format_num(amount_sd)} SD</b>. "
                    f"Debes enviar una comisión del 20% (<b>{format_num(reward_amount_sd)} SD</b>) al referidor <b>{referrer_fullname}</b> (Billetera: <b>{referred_by}</b>)."
                )
        return success, msg
    conn.close()
    return False, "No se encontró la solicitud de compra."

def reject_purchase(request_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_code, amount_sd, amount_cop FROM purchase_requests WHERE id = ?", (request_id,))
    req = cursor.fetchone()
    if req:
        user_code, amount_sd, amount_cop = req
        cursor.execute("UPDATE purchase_requests SET status = 'REJECTED' WHERE id = ?", (request_id,))
        conn.commit()
        conn.close()
        
        # Enviar notificación oficial de rechazo
        add_notification(
            user_code, 
            f"🔴 <b>Compra rechazada.</b> El comprobante adjunto por <b>${amount_cop:,.0f} COP</b> fue rechazado "
            f"debido a inconsistencias. Verifica la imagen de Nequi e intenta nuevamente o ponte en contacto con soporte."
        )
        return True
    conn.close()
    return False


def toggle_user_vip_manually(wallet_code, enable):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT fullname FROM users WHERE wallet_code = ?", (wallet_code,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        return False, "No se encontró ningún usuario con ese código de billetera."
    
    fullname = user[0]
    is_vip_val = 1 if enable else 0
    cursor.execute("UPDATE users SET is_vip = ? WHERE wallet_code = ?", (is_vip_val, wallet_code))
    conn.commit()
    conn.close()
    
    if enable:
        add_notification(wallet_code, "👑 <b>¡Membresía VIP Activada!</b> El administrador te ha otorgado el rango VIP permanente. Ahora gozas de comisiones de retiro del 1% y bonos del 25% de por vida.")
        return True, f"✅ ¡Membresía VIP otorgada con éxito al usuario {fullname}!"
    else:
        add_notification(wallet_code, "⚠️ <b>Tu rango VIP ha sido desactivado</b> por el administrador. Tus comisiones de retiro han vuelto al 2% estándar.")
        return True, f"❌ ¡Membresía VIP removida con éxito al usuario {fullname}!"

def approve_purchase_as_vip(request_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.user_code, p.amount_sd, p.amount_cop, u.fullname, u.referred_by 
        FROM purchase_requests p 
        JOIN users u ON p.user_code = u.wallet_code 
        WHERE p.id = ?
    """, (request_id,))
    req = cursor.fetchone()
    if req:
        user_code, amount_sd, amount_cop, fullname, referred_by = req
        # Actualizar estado de la solicitud
        cursor.execute("UPDATE purchase_requests SET status = 'APPROVED' WHERE id = ?", (request_id,))
        # Activar VIP directamente
        cursor.execute("UPDATE users SET is_vip = 1 WHERE wallet_code = ?", (user_code,))
        conn.commit()
        conn.close()
        
        # Enviar los tokens desde la billetera maestra (99999) al comprador (que sirven como su reembolso o saldo comprado)
        success, msg = send_points("99999", user_code, amount_sd)
        if success:
            # Enviar notificación oficial de aprobación de VIP al comprador
            add_notification(
                user_code, 
                f"👑 <b>¡Membresía VIP Activada Directamente!</b> El administrador validó tu pago de <b>${amount_cop:,.0f} COP</b> y te ha activado el rango VIP permanente. "
                f"Se han acreditado <b>{format_num(amount_sd)} SD</b> a tu billetera y gozas de comisiones de retiro reducidas al 1% de por vida. ¡Disfruta tus privilegios!"
            )
            
            # Si tiene un referidor válido, calcular el 25% (ya que el usuario ahora es VIP) y crear registro de comisión pendiente
            if referred_by:
                conn2 = get_db_connection()
                cursor2 = conn2.cursor()
                cursor2.execute("SELECT is_vip FROM users WHERE wallet_code = ?", (referred_by,))
                ref_vip_row = cursor2.fetchone()
                is_ref_vip = ref_vip_row[0] if ref_vip_row else 0
                ref_pct = 0.25 if is_ref_vip == 1 else 0.20
                reward_amount_sd = amount_sd * ref_pct
                
                conn2 = get_db_connection()
                cursor2 = conn2.cursor()
                cursor2.execute("""
                    INSERT INTO referral_rewards (referrer_code, referred_code, purchase_id, purchase_amount_sd, reward_amount_sd, status)
                    VALUES (?, ?, ?, ?, ?, 'PENDING')
                """, (referred_by, user_code, request_id, amount_sd, reward_amount_sd))
                
                # Obtener nombre del referidor
                cursor2.execute("SELECT fullname FROM users WHERE wallet_code = ?", (referred_by,))
                ref_user = cursor2.fetchone()
                referrer_fullname = ref_user[0] if ref_user else "Referidor"
                conn2.commit()
                conn2.close()
                
                # Enviar notificación al administrador (usuario '99999')
                add_notification(
                    "99999",
                    f"👥 <b>¡Comisión de Referidos VIP!</b> El usuario referido <b>{fullname}</b> ({user_code}) "
                    f"activó VIP. "
                    f"Debes enviar una comisión de <b>{format_num(reward_amount_sd)} SD</b> al referidor <b>{referrer_fullname}</b> (Billetera: <b>{referred_by}</b>)."
                )
        return success, msg
    conn.close()
    return False, "No se encontró la solicitud de compra."

# --- LLAMADOS A API Y CACHÉ ---

@st.cache_data(ttl=120)
def fetch_btc_price():
    try:
        response = requests.get("https://api.coinbase.com/v2/prices/BTC-USD/spot", timeout=2)
        if response.status_code == 200:
            data = response.json()
            return float(data['data']['amount'])
    except Exception:
        pass
    return 64320.50

@st.cache_data(ttl=10) # Cache for 10 seconds to keep it super fresh
def fetch_sd_price_from_dexscreener():
    # 1. Intentar con DexScreener
    try:
        url = "https://api.dexscreener.com/latest/dex/tokens/0xC324649213ec1757190bc4b78bcD41Cc1545C264"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            if data and 'pairs' in data and data['pairs'] is not None and len(data['pairs']) > 0:
                pair = data['pairs'][0]
                price_usd = float(pair.get('priceUsd', 0.0))
                if price_usd > 0:
                    return price_usd
    except Exception:
        pass

    # 2. Intentar con GeckoTerminal (Excelente respaldo para pools de BNB que DexScreener no indexa rápido en su API de tokens)
    try:
        url = "https://api.geckoterminal.com/api/v2/networks/bsc/tokens/0xC324649213ec1757190bc4b78bcD41Cc1545C264"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=3)
        if response.status_code == 200:
            data = response.json()
            if data and 'data' in data and 'attributes' in data['data']:
                price_usd = float(data['data']['attributes'].get('price_usd', 0.0))
                if price_usd > 0:
                    return price_usd
    except Exception:
        pass
    return None

@st.cache_data(ttl=30)
def fetch_bnb_price():
    try:
        response = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT", timeout=3)
        if response.status_code == 200:
            return float(response.json().get('price', 580.00))
    except Exception:
        pass
    try:
        response = requests.get("https://api.coinbase.com/v2/prices/BNB-USD/spot", timeout=3)
        if response.status_code == 200:
            return float(response.json()['data']['amount'])
    except Exception:
        pass
    return 580.00

@st.cache_data(ttl=15)
def fetch_native_balance_rpc(wallet_address, rpc_url="https://bsc-dataseed.binance.org/"):
    if not wallet_address or not wallet_address.strip().startswith("0x"):
        return 0.0
    try:
        addr = wallet_address.strip()
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_getBalance",
            "params": [
                addr,
                "latest"
            ],
            "id": 1
        }
        response = requests.post(rpc_url, json=payload, timeout=3)
        if response.status_code == 200:
            result = response.json().get("result")
            if result and result != "0x":
                raw_balance = int(result, 16)
                return raw_balance / 10**18
    except Exception:
        pass
    return 0.0

@st.cache_data(ttl=120)
def fetch_usd_cop_rate():
    try:
        response = requests.get("https://economia.awesomeapi.com.br/json/last/USD-COP", timeout=2)
        if response.status_code == 200:
            data = response.json()
            return float(data['USDCOP']['bid'])
    except Exception:
        pass
    try:
        response = requests.get("https://open.er-api.com/v6/latest/USD", timeout=2)
        if response.status_code == 200:
            data = response.json()
            return float(data['rates']['COP'])
    except Exception:
        pass
    return 4150.00 # Real-world close average fallback


@st.cache_data(ttl=600)
def get_btc_historical_data():
    try:
        response = requests.get("https://min-api.cryptocompare.com/data/v2/histoday?fsym=BTC&tsym=USD&limit=30", timeout=2)
        if response.status_code == 200:
            data = response.json()
            prices = data['Data']['Data']
            df = pd.DataFrame(prices)
            df['Fecha'] = pd.to_datetime(df['time'], unit='s')
            df['Precio (USD)'] = df['close']
            return df[['Fecha', 'Precio (USD)']]
    except Exception:
        pass
    dates = pd.date_range(end=datetime.now(), periods=30)
    np.random.seed(42)
    base = 61200
    prices = [base + i*160 + np.random.normal(0, 700) for i in range(30)]
    return pd.DataFrame({"Fecha": dates, "Precio (USD)": prices})

@st.cache_data(ttl=600)
def get_usd_cop_historical_data():
    try:
        response = requests.get("https://economia.awesomeapi.com.br/json/daily/USD-COP/30", timeout=2)
        if response.status_code == 200:
            data = response.json()
            rates = []
            dates = []
            for item in data:
                rates.append(float(item['bid']))
                timestamp = int(item['timestamp'])
                dates.append(pd.to_datetime(timestamp, unit='s'))
            df = pd.DataFrame({"Fecha": dates, "Tasa (COP)": rates})
            df = df.sort_values(by="Fecha").reset_index(drop=True)
            return df
    except Exception:
        pass
    dates = pd.date_range(end=datetime.now(), periods=30)
    np.random.seed(10)
    rates = [4150 - i*5 + np.random.normal(0, 25) for i in range(30)]
    return pd.DataFrame({"Fecha": dates, "Tasa (COP)": rates})

def get_custom_token_historical_data(current_price):
    dates = pd.date_range(end=datetime.now(), periods=30)
    np.random.seed(100)
    prices = []
    base = current_price * 0.75
    for i in range(29):
        pct_change = np.random.normal(0.008, 0.04)
        base = base * (1 + pct_change)
        prices.append(base)
    prices.append(current_price)
    return pd.DataFrame({"Fecha": dates, "Precio (USD)": prices})

# --- LÓGICA DE NEGOCIO ---

def register_user(username, password, fullname, email, referred_by=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_pw = hash_password(password)
    wallet_code = generate_unique_wallet_code()
    
    if referred_by:
        referred_by = referred_by.strip()
        if len(referred_by) != 5 or not referred_by.isdigit():
            conn.close()
            return False, "El código de referido debe ser de exactamente 5 dígitos numéricos."
        cursor.execute("SELECT fullname FROM users WHERE wallet_code = ?", (referred_by,))
        if not cursor.fetchone():
            conn.close()
            return False, f"El código de referido {referred_by} no corresponde a ningún usuario registrado."
            
    try:
        cursor.execute("""
            INSERT INTO users (username, password, fullname, email, wallet_code, balance, is_admin, referred_by)
            VALUES (?, ?, ?, ?, ?, 0.0, 0, ?)
        """, (username, hashed_pw, fullname, email, wallet_code, referred_by))
        conn.commit()
        conn.close()
        
        # Enviar notificación inicial de bienvenida
        add_notification(
            wallet_code, 
            f"🎉 <b>¡Te damos la bienvenida a Alianza CryptoWallet!</b> Tu cuenta ha sido creada con éxito. "
            f"Tu código de billetera inmutable es <b>{wallet_code}</b>. Explora tus balances e historial."
        )
        
        # Enviar notificación al referidor
        if referred_by:
            add_notification(
                referred_by,
                f"👥 <b>¡Nuevo Referido Registrado!</b> El usuario <b>{fullname}</b> se ha registrado usando tu código de invitación. "
                f"Recibirás una bonificación del 20% en tokens SD de cada compra verificada que realice."
            )
            
        return True, wallet_code
    except sqlite3.IntegrityError:
        conn.close()
        return False, "El nombre de usuario ya está registrado."

def login_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Try salted hash first (New Secure standard)
    hashed_pw_salted = hash_password(password)
    cursor.execute("""
        SELECT id, username, fullname, email, wallet_code, balance, is_admin 
        FROM users WHERE username = ? AND password = ?
    """, (username, hashed_pw_salted))
    user = cursor.fetchone()
    
    if user:
        conn.close()
        return user
        
    # If not found, try legacy unsalted hash (Automatic secure migration fallback)
    hashed_pw_legacy = hash_password_legacy(password)
    cursor.execute("""
        SELECT id, username, fullname, email, wallet_code, balance, is_admin 
        FROM users WHERE username = ? AND password = ?
    """, (username, hashed_pw_legacy))
    user = cursor.fetchone()
    
    if user:
        # Automatically upgrade their password hash to the salted standard upon login!
        cursor.execute("UPDATE users SET password = ? WHERE id = ?", (hashed_pw_salted, user[0]))
        conn.commit()
        conn.close()
        return user
        
    conn.close()
    return None

def change_user_password(username, old_password, new_password):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check old password (supporting both salted and legacy fallbacks)
    hashed_old_salted = hash_password(old_password)
    cursor.execute("SELECT 1 FROM users WHERE username = ? AND password = ?", (username, hashed_old_salted))
    res = cursor.fetchone()
    
    if not res:
        hashed_old_legacy = hash_password_legacy(old_password)
        cursor.execute("SELECT 1 FROM users WHERE username = ? AND password = ?", (username, hashed_old_legacy))
        res = cursor.fetchone()
        if not res:
            conn.close()
            return False, "La contraseña actual es incorrecta."
    
    hashed_new_salted = hash_password(new_password)
    cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_new_salted, username))
    conn.commit()
    conn.close()
    return True, "Contraseña cambiada exitosamente."

def send_points(sender_code, receiver_code, amount):
    if sender_code == receiver_code:
        return False, "No puedes enviarte puntos a ti mismo."
    if amount <= 0:
        return False, "El monto debe ser mayor a cero."
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Verificar remitente (si no es el sistema/admin)
    if sender_code != "99999":
        cursor.execute("SELECT balance FROM users WHERE wallet_code = ?", (sender_code,))
        sender = cursor.fetchone()
        if not sender or sender[0] < amount:
            conn.close()
            return False, "Saldo de tokens insuficiente."
            
    # Verificar destinatario
    cursor.execute("SELECT username, fullname FROM users WHERE wallet_code = ?", (receiver_code,))
    receiver = cursor.fetchone()
    if not receiver:
        conn.close()
        return False, f"El código de billetera {receiver_code} no existe."
    
    receiver_name = receiver[1]
        
    try:
        if sender_code != "99999":
            cursor.execute("UPDATE users SET balance = balance - ?, wallet_code = wallet_code WHERE wallet_code = ?", (amount, sender_code))
        else:
            cursor.execute("UPDATE users SET balance = balance - ?, wallet_code = wallet_code WHERE wallet_code = ?", (amount, sender_code))
            
        cursor.execute("UPDATE users SET balance = balance + ?, wallet_code = wallet_code WHERE wallet_code = ?", (amount, receiver_code))
        
        cursor.execute("""
            INSERT INTO transactions (sender_code, receiver_code, amount)
            VALUES (?, ?, ?)
        """, (sender_code, receiver_code, amount))
        
        conn.commit()
        conn.close()
        
        # Enviar notificación al receptor si la transacción no es automática del admin
        if sender_code != "99999":
            add_notification(
                receiver_code,
                f"📥 <b>¡Has recibido fondos!</b> El código de billetera <b>{sender_code}</b> te ha enviado "
                f"<b>{format_num(amount)} SD</b> de forma directa."
            )
        
        return True, f"¡Acreditación exitosa! Has enviado {format_num(amount)} tokens."
    except Exception as e:
        conn.rollback()
        conn.close()
        return False, f"Error en la transacción: {str(e)}"

def get_user_balance(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance, wallet_code, balance_cop, is_vip FROM users WHERE username = ?", (username,))
    res = cursor.fetchone()
    conn.close()
    return res if res else (0.0, "", 0.0, 0)


def format_num(val):
    if val is None:
        return "0"
    try:
        val_f = float(val)
        if val_f.is_integer() or abs(val_f - round(val_f)) < 1e-9:
            return f"{int(round(val_f)):,}"
        formatted = f"{val_f:,.2f}"
        if '.' in formatted:
            formatted = formatted.rstrip('0').rstrip('.')
        return formatted
    except Exception:
        return str(val)

def format_usd_price(price):
    # Dynamic floating token price formatter (prevents rounding to $0.0000 on low values)
    if price is None:
        return "$0.00"
    try:
        price_f = float(price)
        if price_f <= 0.0:
            return "$0.00"
        if price_f < 0.0001:
            return f"${price_f:,.8f} USD"
        elif price_f < 0.01:
            return f"${price_f:,.6f} USD"
        elif price_f < 0.1:
            return f"${price_f:,.5f} USD"
        elif price_f < 1.0:
            return f"${price_f:,.4f} USD"
        else:
            return f"${price_f:,.2f} USD"
    except Exception:
        return f"${price} USD" 

def update_user_balance_and_cop(user_code, balance_sd, balance_cop):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users 
        SET balance = ?, balance_cop = ? 
        WHERE wallet_code = ?
    """, (balance_sd, balance_cop, user_code))
    conn.commit()
    conn.close()


def get_user_nequi(wallet_code):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nequi_number FROM users WHERE wallet_code = ?", (wallet_code,))
    res = cursor.fetchone()
    conn.close()
    return res[0] if res and res[0] else ""

def update_user_nequi(wallet_code, nequi_number):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET nequi_number = ? WHERE wallet_code = ?", (nequi_number, wallet_code))
    conn.commit()
    conn.close()
    return True

def update_global_nequi(nequi_number):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Actualizar la cuenta madre global en token_settings
    cursor.execute("UPDATE token_settings SET nequi_number = ? WHERE id = 1", (nequi_number,))
    # Sincronizar el nequi_number del propio admin en la tabla de usuarios
    cursor.execute("UPDATE users SET nequi_number = ? WHERE wallet_code = '99999'", (nequi_number,))
    conn.commit()
    conn.close()
    return True


# --- FUNCIONES DE JUEGOS Y CONTROL ---

def get_game_setting(key, default_val="", default_num=0.0):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT value_text, value_numeric FROM game_settings WHERE setting_key = ?", (key,))
    res = cursor.fetchone()
    conn.close()
    if res:
        return res[0], res[1]
    return default_val, default_num

def update_game_setting(key, text_val, num_val):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO game_settings (setting_key, value_text, value_numeric)
        VALUES (?, ?, ?)
    """, (key, text_val, num_val))
    conn.commit()
    conn.close()
    return True

# --- FUNCIONES DE TRIVIA ---
def get_active_trivia():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, question, option_a, option_b, option_c, correct_option, entry_fee, prize_sd 
        FROM trivias WHERE active = 1 ORDER BY id DESC LIMIT 1
    """)
    res = cursor.fetchone()
    conn.close()
    if res:
        return {
            "id": res[0],
            "question": res[1],
            "option_a": res[2],
            "option_b": res[3],
            "option_c": res[4],
            "correct_option": res[5],
            "entry_fee": res[6],
            "prize_sd": res[7]
        }
    return None

def has_user_answered_trivia(user_code, trivia_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM user_trivia_attempts WHERE user_code = ? AND trivia_id = ?", (user_code, trivia_id))
    res = cursor.fetchone()
    conn.close()
    return bool(res)

def play_trivia(user_code, trivia_id, chosen_option):
    trivia = get_active_trivia()
    if not trivia or trivia["id"] != trivia_id:
        return False, "La trivia seleccionada ya no está activa."
        
    if has_user_answered_trivia(user_code, trivia_id):
        return False, "Ya has participado en esta trivia."
        
    # Verificar saldo
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM users WHERE wallet_code = ?", (user_code,))
    user_bal = cursor.fetchone()
    if not user_bal or user_bal[0] < trivia["entry_fee"]:
        conn.close()
        return False, f"Saldo insuficiente. Jugar esta trivia cuesta {trivia['entry_fee']} SD."
        
    is_correct = 1 if chosen_option == trivia["correct_option"] else 0
    
    try:
        # Descontar del usuario y sumarle al admin
        cursor.execute("UPDATE users SET balance = balance - ? WHERE wallet_code = ?", (trivia["entry_fee"], user_code))
        cursor.execute("UPDATE users SET balance = balance + ? WHERE wallet_code = '99999'", (trivia["entry_fee"],))
        
        # Registrar transacción de entrada
        cursor.execute("""
            INSERT INTO transactions (sender_code, receiver_code, amount)
            VALUES (?, '99999_TRIVIA_FEE', ?)
        """, (user_code, trivia["entry_fee"]))
        
        # Registrar intento
        cursor.execute("""
            INSERT INTO user_trivia_attempts (user_code, trivia_id, is_correct)
            VALUES (?, ?, ?)
        """, (user_code, trivia_id, is_correct))
        
        if is_correct:
            # Pagar premio desde el admin
            cursor.execute("UPDATE users SET balance = balance - ? WHERE wallet_code = '99999'", (trivia["prize_sd"],))
            cursor.execute("UPDATE users SET balance = balance + ? WHERE wallet_code = ?", (trivia["prize_sd"], user_code))
            
            # Registrar transacción de premio
            cursor.execute("""
                INSERT INTO transactions (sender_code, receiver_code, amount)
                VALUES ('99999_TRIVIA_REWARD', ?, ?)
            """, (user_code, trivia["prize_sd"]))
            
            add_notification(user_code, f"🧠 <b>¡Trivia Completada!</b> Has respondido correctamente y ganaste <b>{format_num(trivia['prize_sd'])} SD</b>.")
            msg = f"🎉 ¡Excelente! Has respondido correctamente la opción {chosen_option} y has ganado {format_num(trivia['prize_sd'])} SD."
        else:
            add_notification(user_code, f"🧠 <b>¡Trivia Completada!</b> Tu respuesta fue incorrecta. La opción correcta era <b>{trivia['correct_option']}</b>.")
            msg = f"😢 Tu respuesta fue incorrecta. La opción correcta era la {trivia['correct_option']}. ¡Sigue intentando con la próxima!"
            
        conn.commit()
        conn.close()
        return True, msg
    except Exception as e:
        conn.rollback()
        conn.close()
        return False, f"Error al procesar trivia: {str(e)}"

# --- FUNCIONES DE PRONÓSTICOS DEPORTIVOS ---
def get_active_sports_bet():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id, match_name, ticket_cost, prize_sd, status, winner_option,
                   local_team, visitor_team, match_time, ends_at, current_score, match_status
            FROM sports_bets WHERE status = 'ACTIVE' ORDER BY id DESC LIMIT 1
        """)
        res = cursor.fetchone()
    except Exception:
        cursor.execute("""
            SELECT id, match_name, ticket_cost, prize_sd, status, winner_option
            FROM sports_bets WHERE status = 'ACTIVE' ORDER BY id DESC LIMIT 1
        """)
        res = cursor.fetchone()
        if res:
            res = list(res) + ["Colombia", "Brasil", "Hoy 18:00", "Hoy 20:00", "0 - 0", "No iniciado"]
    conn.close()
    if res:
        return {
            "id": res[0],
            "match_name": res[1],
            "ticket_cost": res[2],
            "prize_sd": res[3],
            "status": res[4],
            "winner_option": res[5],
            "local_team": res[6] if len(res) > 6 and res[6] else "",
            "visitor_team": res[7] if len(res) > 7 and res[7] else "",
            "match_time": res[8] if len(res) > 8 and res[8] else "",
            "ends_at": res[9] if len(res) > 9 and res[9] else "",
            "current_score": res[10] if len(res) > 10 and res[10] else "0 - 0",
            "match_status": res[11] if len(res) > 11 and res[11] else "No iniciado"
        }
    return None

def get_user_prediction(user_code, match_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT prediction FROM user_predictions WHERE user_code = ? AND match_id = ?", (user_code, match_id))
    res = cursor.fetchone()
    conn.close()
    return res[0] if res else None

def get_active_sports_bets():
    conn = get_db_connection()
    cursor = conn.cursor()
    active_bets = []
    try:
        cursor.execute("""
            SELECT id, match_name, ticket_cost, prize_sd, status, winner_option,
                   local_team, visitor_team, match_time, ends_at, current_score, match_status
            FROM sports_bets WHERE status = 'ACTIVE' ORDER BY id DESC
        """)
        rows = cursor.fetchall()
        for r in rows:
            active_bets.append({
                "id": r[0],
                "match_name": r[1],
                "ticket_cost": r[2],
                "prize_sd": r[3],
                "status": r[4],
                "winner_option": r[5],
                "local_team": r[6] if len(r) > 6 and r[6] else "",
                "visitor_team": r[7] if len(r) > 7 and r[7] else "",
                "match_time": r[8] if len(r) > 8 and r[8] else "",
                "ends_at": r[9] if len(r) > 9 and r[9] else "",
                "current_score": r[10] if len(r) > 10 and r[10] else "0 - 0",
                "match_status": r[11] if len(r) > 11 and r[11] else "No iniciado"
            })
    except Exception:
        pass
    conn.close()
    return active_bets

def get_sports_bet_by_id(match_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    res = None
    try:
        cursor.execute("""
            SELECT id, match_name, ticket_cost, prize_sd, status, winner_option,
                   local_team, visitor_team, match_time, ends_at, current_score, match_status
            FROM sports_bets WHERE id = ?
        """, (match_id,))
        res = cursor.fetchone()
    except Exception:
        pass
    conn.close()
    if res:
        return {
            "id": res[0],
            "match_name": res[1],
            "ticket_cost": res[2],
            "prize_sd": res[3],
            "status": res[4],
            "winner_option": res[5],
            "local_team": res[6] if len(res) > 6 and res[6] else "",
            "visitor_team": res[7] if len(res) > 7 and res[7] else "",
            "match_time": res[8] if len(res) > 8 and res[8] else "",
            "ends_at": res[9] if len(res) > 9 and res[9] else "",
            "current_score": res[10] if len(res) > 10 and res[10] else "0 - 0",
            "match_status": res[11] if len(res) > 11 and res[11] else "No iniciado"
        }
    return None

def annul_sports_bet(match_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Get match details
        cursor.execute("SELECT match_name, ticket_cost FROM sports_bets WHERE id = ?", (match_id,))
        match_row = cursor.fetchone()
        if not match_row:
            conn.close()
            return False, "No se encontró el partido."
        match_name, ticket_cost = match_row
        
        # Get all predictions for this match
        cursor.execute("SELECT id, user_code FROM user_predictions WHERE match_id = ?", (match_id,))
        predictions = cursor.fetchall()
        
        # Refund each user
        for pred_id, user_code in predictions:
            # Refund user balance
            cursor.execute("UPDATE users SET balance = balance + ? WHERE wallet_code = ?", (ticket_cost, user_code))
            # Deduct from admin balance (99999)
            cursor.execute("UPDATE users SET balance = balance - ? WHERE wallet_code = '99999'", (ticket_cost,))
            
            # Record refund transaction
            cursor.execute("""
                INSERT INTO transactions (sender_code, receiver_code, amount)
                VALUES ('99999_SPORTS_ANNUL_REFUND', ?, ?)
            """, (user_code, ticket_cost))
            
            # Update prediction status to CANCELLED
            cursor.execute("UPDATE user_predictions SET status = 'CANCELLED' WHERE id = ?", (pred_id,))
            
            add_notification(
                user_code,
                f"⚽ <b>Partido Anulado:</b> El partido <b>{match_name}</b> fue anulado por el administrador. "
                f"Se han reembolsado tus <b>{format_num(ticket_cost)} SD</b> a tu billetera de forma inmediata."
            )
            
        # Mark match as CANCELLED
        cursor.execute("UPDATE sports_bets SET status = 'CANCELLED' WHERE id = ?", (match_id,))
        conn.commit()
        conn.close()
        return True, f"¡Partido anulado con éxito! Se reembolsaron los tickets a {len(predictions)} participantes."
    except Exception as e:
        conn.rollback()
        conn.close()
        return False, f"Error al anular el partido: {str(e)}"


def buy_sports_prediction(user_code, match_id, chosen_prediction):
    bet = get_sports_bet_by_id(match_id)
    if not bet or bet["status"] != 'ACTIVE':
        return False, "Este pronóstico ya no está activo."
        
    already_pred = get_user_prediction(user_code, match_id)
    if already_pred:
        return False, f"Ya compraste un ticket de pronóstico para este partido. Elegiste: {already_pred}."
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM users WHERE wallet_code = ?", (user_code,))
    user_bal = cursor.fetchone()
    if not user_bal or user_bal[0] < bet["ticket_cost"]:
        conn.close()
        return False, f"Saldo insuficiente. El ticket de pronóstico cuesta {bet['ticket_cost']} SD."
        
    try:
        # Descontar del usuario y sumarle al admin
        cursor.execute("UPDATE users SET balance = balance - ? WHERE wallet_code = ?", (bet["ticket_cost"], user_code))
        cursor.execute("UPDATE users SET balance = balance + ? WHERE wallet_code = '99999'", (bet["ticket_cost"],))
        
        # Registrar transacción
        cursor.execute("""
            INSERT INTO transactions (sender_code, receiver_code, amount)
            VALUES (?, '99999_SPORTS_TICKET', ?)
        """, (user_code, bet["ticket_cost"]))
        
        # Registrar predicción
        cursor.execute("""
            INSERT INTO user_predictions (user_code, match_id, prediction, status)
            VALUES (?, ?, ?, 'PENDING')
        """, (user_code, match_id, chosen_prediction))
        
        conn.commit()
        conn.close()
        
        add_notification(user_code, f"⚽ <b>¡Pronóstico Registrado!</b> Compraste un ticket para el partido <b>{bet['match_name']}</b>. Elegiste: <b>{chosen_prediction}</b>.")
        return True, f"¡Ticket comprado con éxito! Registraste tu pronóstico '{chosen_prediction}' por {bet['ticket_cost']} SD."
    except Exception as e:
        conn.rollback()
        conn.close()
        return False, f"Error al procesar ticket: {str(e)}"

def resolve_sports_bet(match_id, winning_option):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # 1. Marcar el partido como resuelto
        cursor.execute("UPDATE sports_bets SET status = 'RESOLVED', winner_option = ? WHERE id = ?", (winning_option, match_id))
        
        # 2. Obtener datos del partido
        cursor.execute("SELECT match_name, prize_sd FROM sports_bets WHERE id = ?", (match_id,))
        match_row = cursor.fetchone()
        match_name = match_row[0]
        prize_sd = match_row[1]
        
        # 3. Obtener todas las predicciones para este partido
        cursor.execute("SELECT id, user_code, prediction FROM user_predictions WHERE match_id = ?", (match_id,))
        predictions = cursor.fetchall()
        
        for pred_id, user_code, prediction in predictions:
            if prediction == winning_option:
                # Actualizar predicción a GANADA
                cursor.execute("UPDATE user_predictions SET status = 'WON' WHERE id = ?", (pred_id,))
                
                # Pagar premio al usuario desde el admin
                cursor.execute("UPDATE users SET balance = balance - ? WHERE wallet_code = '99999'", (prize_sd,))
                cursor.execute("UPDATE users SET balance = balance + ? WHERE wallet_code = ?", (prize_sd, user_code))
                
                # Registrar transacción de premio
                cursor.execute("""
                    INSERT INTO transactions (sender_code, receiver_code, amount)
                    VALUES ('99999_SPORTS_REWARD', ?, ?)
                """, (user_code, prize_sd))
                
                add_notification(
                    user_code, 
                    f"⚽ <b>¡Pronóstico Ganado!</b> Tu pronóstico para <b>{match_name}</b> fue acertado. "
                    f"Has ganado el premio de <b>{format_num(prize_sd)} SD</b>."
                )
            else:
                # Actualizar predicción a PERDIDA
                cursor.execute("UPDATE user_predictions SET status = 'LOST' WHERE id = ?", (pred_id,))
                add_notification(
                    user_code, 
                    f"⚽ <b>¡Pronóstico Finalizado!</b> El partido <b>{match_name}</b> finalizó con resultado <b>{winning_option}</b>. "
                    f"Tu pronóstico no acertó. ¡Suerte en el próximo partido!"
                )
                
        conn.commit()
        conn.close()
        return True, "¡Partido resuelto con éxito! Se acreditaron los premios a todos los ganadores."
    except Exception as e:
        conn.rollback()
        conn.close()
        return False, f"Error al resolver partido: {str(e)}"

# --- FUNCIONES DE SUBASTA DE CENTAVOS ---
def get_active_auction():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, item_name, description, current_price, highest_bidder, ends_at, bid_fee_sd, bid_increment, status 
        FROM penny_auctions WHERE status = 'ACTIVE' ORDER BY id DESC LIMIT 1
    """)
    res = cursor.fetchone()
    conn.close()
    if res:
        return {
            "id": res[0],
            "item_name": res[1],
            "description": res[2],
            "current_price": res[3],
            "highest_bidder": res[4],
            "ends_at": res[5],
            "bid_fee_sd": res[6],
            "bid_increment": res[7],
            "status": res[8]
        }
    return None

def place_penny_bid(user_code, auction_id):
    auc = get_active_auction()
    if not auc or auc["id"] != auction_id:
        return False, "La subasta ya no está activa."
        
    # Verificar si el tiempo ya expiró
    ends_at_time = datetime.strptime(auc["ends_at"], "%Y-%m-%d %H:%M:%S")
    now_time = datetime.utcnow()
    if now_time >= ends_at_time:
        # Marcar subasta como finalizada
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE penny_auctions SET status = 'ENDED' WHERE id = ?", (auction_id,))
        conn.commit()
        conn.close()
        return False, "La subasta ha finalizado."
        
    # Verificar saldo
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM users WHERE wallet_code = ?", (user_code,))
    user_bal = cursor.fetchone()
    if not user_bal or user_bal[0] < auc["bid_fee_sd"]:
        conn.close()
        return False, f"Saldo insuficiente. Pujar cuesta {auc['bid_fee_sd']} SD."
        
    try:
        # Cobrar la tarifa de puja (se envía al administrador 99999)
        cursor.execute("UPDATE users SET balance = balance - ? WHERE wallet_code = ?", (auc["bid_fee_sd"], user_code))
        cursor.execute("UPDATE users SET balance = balance + ? WHERE wallet_code = '99999'", (auc["bid_fee_sd"],))
        
        # Registrar transacción
        cursor.execute("""
            INSERT INTO transactions (sender_code, receiver_code, amount)
            VALUES (?, 'SYSTEM_AUCTION_BID_FEE', ?)
        """, (user_code, auc["bid_fee_sd"]))
        
        # Incrementar el precio y cambiar el mejor postor
        new_price = auc["current_price"] + auc["bid_increment"]
        
        # Extender el tiempo en 15 segundos si faltan menos de 60 segundos
        seconds_remaining = (ends_at_time - now_time).total_seconds()
        new_ends_at = ends_at_time
        if seconds_remaining < 60:
            new_ends_at = now_time + timedelta(seconds=20) # Añadir 20 segundos
            
        new_ends_at_str = new_ends_at.strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute("""
            UPDATE penny_auctions 
            SET current_price = ?, highest_bidder = ?, ends_at = ? 
            WHERE id = ?
        """, (new_price, user_code, new_ends_at_str, auction_id))
        
        conn.commit()
        conn.close()
        return True, "¡Puja colocada con éxito!"
    except Exception as e:
        conn.rollback()
        conn.close()
        return False, f"Error al procesar puja: {str(e)}"

def check_and_finalize_auctions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, item_name, highest_bidder, ends_at FROM penny_auctions WHERE status = 'ACTIVE'")
    active_aucs = cursor.fetchall()
    now_time = datetime.utcnow()
    for aid, item_name, bidder, ends_at_str in active_aucs:
        ends_at_time = datetime.strptime(ends_at_str, "%Y-%m-%d %H:%M:%S")
        if now_time >= ends_at_time:
            # Marcar como finalizado
            cursor.execute("UPDATE penny_auctions SET status = 'ENDED' WHERE id = ?", (aid,))
            if bidder and bidder != "99999":
                add_notification(
                    bidder, 
                    f"🔨 <b>¡Ganaste la Subasta!</b> Felicitaciones, ganaste la subasta de <b>{item_name}</b>. "
                    f"Ingresa a la tienda Alianza en la sección de subastas para reclamar tu premio."
                )
    conn.commit()
    conn.close()

# Ejecutar chequeo de subastas automáticamente
check_and_finalize_auctions()

# --- LÓGICA DE MENSAJERÍA Y MÓVILES (EMPRESA DE MENSAJERÍA) ---

def pay_delivery_service(sender_code, driver_code, amount_sd, service_id=""):
    if sender_code == driver_code:
        return False, "No puedes pagarte un envío a ti mismo."
    if amount_sd <= 0:
        return False, "El monto del envío debe ser mayor a cero."
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Verificar saldo en SD del cliente
    cursor.execute("SELECT balance, fullname FROM users WHERE wallet_code = ?", (sender_code,))
    sender = cursor.fetchone()
    if not sender or sender[0] < amount_sd:
        conn.close()
        return False, "Saldo de tokens SIAD (SD) insuficiente para pagar este envío."
    sender_name = sender[1]
    
    # 2. Verificar existencia del conductor (móvil)
    cursor.execute("SELECT fullname FROM users WHERE wallet_code = ?", (driver_code,))
    driver = cursor.fetchone()
    if not driver:
        conn.close()
        return False, f"El código de billetera del móvil {driver_code} no existe o no es válido."
    driver_name = driver[0]
    
    # 3. Calcular montos de subsidio automático
    cashback_sd = amount_sd * 0.50
    bonus_sd = amount_sd * 0.10
    total_admin_subsidy = cashback_sd + bonus_sd
    
    # Verificar si el administrador (billetera maestra 99999) tiene fondos suficientes
    cursor.execute("SELECT balance FROM users WHERE wallet_code = '99999'")
    admin_bal = cursor.fetchone()
    if not admin_bal or admin_bal[0] < total_admin_subsidy:
        conn.close()
        return False, "La billetera del administrador no dispone de fondos de base suficientes para financiar el subsidio en este momento."
        
    try:
        # 4. Descontar del cliente y sumarle al conductor (Pago original)
        cursor.execute("UPDATE users SET balance = balance - ? WHERE wallet_code = ?", (amount_sd, sender_code))
        cursor.execute("UPDATE users SET balance = balance + ? WHERE wallet_code = ?", (amount_sd, driver_code))
        
        # Registrar transacción original
        cursor.execute("""
            INSERT INTO transactions (sender_code, receiver_code, amount)
            VALUES (?, ?, ?)
        """, (sender_code, driver_code, amount_sd))
        
        # 5. Enviar reembolso del 50% al cliente desde el Admin (99999)
        cursor.execute("UPDATE users SET balance = balance - ? WHERE wallet_code = '99999'", (cashback_sd,))
        cursor.execute("UPDATE users SET balance = balance + ? WHERE wallet_code = ?", (cashback_sd, sender_code))
        cursor.execute("""
            INSERT INTO transactions (sender_code, receiver_code, amount)
            VALUES ('99999', ?, ?)
        """, (sender_code, cashback_sd))
        
        # 6. Enviar bono del 10% al móvil desde el Admin (99999)
        cursor.execute("UPDATE users SET balance = balance - ? WHERE wallet_code = '99999'", (bonus_sd,))
        cursor.execute("UPDATE users SET balance = balance + ? WHERE wallet_code = ?", (bonus_sd, driver_code))
        cursor.execute("""
            INSERT INTO transactions (sender_code, receiver_code, amount)
            VALUES ('99999', ?, ?)
        """, (driver_code, bonus_sd))
        
        # 7. Registrar en la tabla de pagos de móviles (Mensajería)
        token_price_usd = get_token_settings()['price_usd']
        usd_cop_rate = fetch_usd_cop_rate()
        amount_cop = amount_sd * token_price_usd * usd_cop_rate
        
        cursor.execute("""
            INSERT INTO movil_payments (user_code, payment_type, amount_sd, amount_cop, target_code)
            VALUES (?, 'SHIPPING_PAYMENT', ?, ?, ?)
        """, (sender_code, amount_sd, amount_cop, driver_code))
        
        conn.commit()
        conn.close()
        
        # 8. Notificaciones
        lbl_service = f" (ID Guía: {service_id})" if service_id else ""
        add_notification(
            sender_code,
            f"📦 <b>¡Pago de Envío Realizado!</b> Pagaste <b>{format_num(amount_sd)} SD</b> "
            f"(${amount_cop:,.0f} COP) al móvil <b>{driver_name} ({driver_code})</b>{lbl_service}. "
            f"🔥 <b>¡Subsidio Alianza!</b> Se te ha devuelto un reembolso del 50% (<b>{format_num(cashback_sd)} SD</b>) a tu billetera de forma automática. <b>¡El envío te costó la mitad!</b>"
        )
        add_notification(
            driver_code,
            f"📦 <b>¡Pago de Envío Recibido!</b> El cliente <b>{sender_name}</b> te pagó <b>{format_num(amount_sd)} SD</b> "
            f"(${amount_cop:,.0f} COP){lbl_service}. "
            f"🚀 <b>¡Bono Alianza!</b> Recibiste un bono del 10% adicional (<b>{format_num(bonus_sd)} SD</b>) del fondo del Administrador. "
            f"Total recibido: <b>{(amount_sd + bonus_sd):,.4f} SD</b>."
        )
        return True, f"¡Pago exitoso! Enviaste {format_num(amount_sd)} SD, se te reembolsó el 50% de inmediato ({format_num(cashback_sd)} SD) y el conductor recibió {amount_sd + bonus_sd:,.4f} SD (10% bono)."
    except Exception as e:
        conn.rollback()
        conn.close()
        return False, f"Error al procesar el pago del envío: {str(e)}"

def pay_weekly_fee(user_code, use_tokens=True, message=""): 
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Obtener datos del usuario
    cursor.execute("SELECT balance, balance_cop, fullname FROM users WHERE wallet_code = ?", (user_code,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        return False, "Usuario no encontrado."
    
    balance_sd, balance_cop, fullname = user
    token = get_token_settings()
    usd_cop_rate = fetch_usd_cop_rate()
    token_price_cop = token['price_usd'] * usd_cop_rate
    
    try:
        if use_tokens:
            # Cuota de 40.000 COP con 20% descuento = 32.000 COP
            fee_cop = 32000.0
            fee_sd = fee_cop / token_price_cop
            
            if balance_sd < fee_sd:
                conn.close()
                return False, f"Saldo en SD insuficiente. Necesitas {format_num(fee_sd)} SD para pagar con descuento del 20%."
                
            # Cobrar en SD (enviar a la cuenta del admin '99999')
            cursor.execute("UPDATE users SET balance = balance - ? WHERE wallet_code = ?", (fee_sd, user_code))
            cursor.execute("UPDATE users SET balance = balance + ? WHERE wallet_code = ?", (fee_sd, '99999'))
            
            # Registrar en transactions
            cursor.execute("""
                INSERT INTO transactions (sender_code, receiver_code, amount)
                VALUES (?, '99999', ?)
            """, (user_code, fee_sd))
            
            # Registrar en movil_payments
            cursor.execute("""
                INSERT INTO movil_payments (user_code, payment_type, amount_sd, amount_cop, target_code, message)
                VALUES (?, 'WEEKLY_FEE_SD', ?, ?, '99999', ?)
            """, (user_code, fee_sd, fee_cop, message or ''))
            
            conn.commit()
            conn.close()
            
            # Notificaciones
            add_notification(
                user_code,
                f"💳 <b>¡Cuota Semanal Pagada!</b> Has pagado tu cuota de móvil por valor de <b>$32,000 COP</b> "
                f"(pagados con <b>{format_num(fee_sd)} SD</b> tras aplicar un 20% de descuento). ¡Gracias por tu pago!"
            )
            add_notification(
                '99999',
                f"🚚 <b>¡Pago de Cuota Recibido!</b> El móvil <b>{fullname} ({user_code})</b> ha pagado su cuota semanal "
                f"usando tokens SD (Recibido: <b>{format_num(fee_sd)} SD</b> equivalente a $32,000 COP)." + (f"<br>💬 <b>Mensaje:</b> {message}" if message else "")
            )
            return True, f"Cuota de móvil pagada con éxito usando {format_num(fee_sd)} SD ($32,000 COP)."
            
        else:
            # Cuota sin descuento = 40.000 COP
            fee_cop = 40000.0
            
            if balance_cop < fee_cop:
                conn.close()
                return False, "Saldo de pesos colombianos (COP) retirable insuficiente para pagar la cuota de $40,000 COP."
                
            # Cobrar en COP del saldo del usuario y sumarlo al del admin
            cursor.execute("UPDATE users SET balance_cop = balance_cop - ? WHERE wallet_code = ?", (fee_cop, user_code))
            cursor.execute("UPDATE users SET balance_cop = balance_cop + ? WHERE wallet_code = ?", (fee_cop, '99999'))
            
            # Registrar en transactions (equivalente en SD para registro histórico)
            cursor.execute("""
                INSERT INTO transactions (sender_code, receiver_code, amount)
                VALUES (?, '99999_COP', ?)
            """, (user_code, fee_cop / token_price_cop))
            
            # Registrar en movil_payments
            cursor.execute("""
                INSERT INTO movil_payments (user_code, payment_type, amount_sd, amount_cop, target_code, message)
                VALUES (?, 'WEEKLY_FEE_COP', ?, ?, '99999', ?)
            """, (user_code, fee_cop / token_price_cop, fee_cop, message or ''))
            
            conn.commit()
            conn.close()
            
            # Notificaciones
            add_notification(
                user_code,
                f"💳 <b>¡Cuota Semanal Pagada!</b> Has pagado tu cuota de móvil de <b>$40,000 COP</b> "
                f"(debitados de tu saldo retirable en pesos). ¡Gracias por tu pago!"
            )
            add_notification(
                '99999',
                f"🚚 <b>¡Pago de Cuota Recibido!</b> El móvil <b>{fullname} ({user_code})</b> ha pagado su cuota semanal "
                f"en pesos colombianos ($40,000 COP)." + (f"<br>💬 <b>Mensaje:</b> {message}" if message else "")
            )
            return True, "Cuota de móvil pagada con éxito usando $40,000 COP de tu saldo retirable."
            
    except Exception as e:
        conn.rollback()
        conn.close()
        return False, f"Error al procesar el pago de la cuota: {str(e)}"

def get_movil_payments_history(user_code):
    conn = get_db_connection()
    df = pd.read_sql_query("""
        SELECT p.id, p.payment_type, p.amount_sd, p.amount_cop, p.target_code, p.timestamp, p.message, 
               u1.fullname as customer_name, u2.fullname as driver_name
        FROM movil_payments p
        LEFT JOIN users u1 ON p.user_code = u1.wallet_code
        LEFT JOIN users u2 ON p.target_code = u2.wallet_code
        WHERE p.user_code = ? OR p.target_code = ?
        ORDER BY p.timestamp DESC
    """, conn, params=(user_code, user_code))
    conn.close()
    return df

def get_all_movil_payments():
    conn = get_db_connection()
    df = pd.read_sql_query("""
        SELECT p.id, p.payment_type, p.amount_sd, p.amount_cop, p.user_code, p.target_code, p.timestamp, p.message, 
               u1.fullname as customer_name, u2.fullname as target_name
        FROM movil_payments p
        LEFT JOIN users u1 ON p.user_code = u1.wallet_code
        LEFT JOIN users u2 ON p.target_code = u2.wallet_code
        ORDER BY p.timestamp DESC
    """, conn)
    conn.close()
    return df


def get_transaction_history(wallet_code):
    conn = get_db_connection()
    df = pd.read_sql_query("""
        SELECT t.id, t.sender_code, t.receiver_code, t.amount, t.timestamp,
               u1.fullname as sender_name, u2.fullname as receiver_name
        FROM transactions t
        LEFT JOIN users u1 ON t.sender_code = u1.wallet_code
        LEFT JOIN users u2 ON t.receiver_code = u2.wallet_code
        WHERE t.sender_code = ? OR t.receiver_code = ?
        ORDER BY t.timestamp ASC
    """, conn, params=(wallet_code, wallet_code))
    conn.close()
    return df

def execute_multi_swap(wallet_code, from_curr, to_curr, amount_from, amount_to, price_from_usd, price_to_usd):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # 1. Deduct From_Currency
        if from_curr == "SD":
            cursor.execute("UPDATE users SET balance = balance - ? WHERE wallet_code = ?", (amount_from, wallet_code))
        elif from_curr == "COP":
            cursor.execute("UPDATE users SET balance_cop = balance_cop - ? WHERE wallet_code = ?", (amount_from, wallet_code))
        elif from_curr == "BNB":
            if "sim_bnb" in st.session_state:
                st.session_state.sim_bnb -= amount_from
        elif from_curr == "USDT":
            if "sim_usdt" in st.session_state:
                st.session_state.sim_usdt -= amount_from
            
        # 2. Add To_Currency
        if to_curr == "SD":
            cursor.execute("UPDATE users SET balance = balance + ? WHERE wallet_code = ?", (amount_to, wallet_code))
        elif to_curr == "COP":
            cursor.execute("UPDATE users SET balance_cop = balance_cop + ? WHERE wallet_code = ?", (amount_to, wallet_code))
        elif to_curr == "BNB":
            if "sim_bnb" in st.session_state:
                st.session_state.sim_bnb += amount_to
        elif to_curr == "USDT":
            if "sim_usdt" in st.session_state:
                st.session_state.sim_usdt += amount_to
            
        # 3. Insert transaction log
        tx_type = f"SWAP_{from_curr}_{to_curr}"
        cursor.execute("""
            INSERT INTO transactions (sender_code, receiver_code, amount)
            VALUES (?, ?, ?)
        """, (wallet_code, tx_type, amount_from))
        
        conn.commit()
        conn.close()
        
        # 4. Add notification
        msg = f"🔄 <b>Swap completado:</b> Cambiaste <b>{format_num(amount_from)} {from_curr}</b> por <b>{format_num(amount_to)} {to_curr}</b> exitosamente."
        add_notification(wallet_code, msg)
        return True, f"¡Intercambio exitoso! Has convertido {format_num(amount_from)} {from_curr} a {format_num(amount_to)} {to_curr}."
    except Exception as e:
        conn.rollback()
        conn.close()
        return False, f"Error al procesar el swap: {str(e)}"

def swap_sd_to_cop(user_code, amount_sd, rate_usd, usd_cop_rate):
    if amount_sd <= 0:
        return False, "La cantidad de SD debe ser mayor a cero."
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM users WHERE wallet_code = ?", (user_code,))
    res = cursor.fetchone()
    if not res or res[0] < amount_sd:
        conn.close()
        return False, "Saldo de tokens SD insuficiente."
    
    # Calcular valor en pesos COP
    usd_value = amount_sd * rate_usd
    cop_value = usd_value * usd_cop_rate
    
    try:
        # Descontar SD, aumentar balance_cop
        cursor.execute("UPDATE users SET balance = balance - ?, balance_cop = balance_cop + ? WHERE wallet_code = ?", (amount_sd, cop_value, user_code))
        
        # Registrar como transacción de swap
        cursor.execute("""
            INSERT INTO transactions (sender_code, receiver_code, amount)
            VALUES (?, 'SWAP_COP', ?)
        """, (user_code, amount_sd))
        
        conn.commit()
        conn.close()
        
        # Enviar notificación
        add_notification(
            user_code,
            f"🔄 <b>Swap completado exitosamente:</b> Has cambiado <b>{format_num(amount_sd)} SD</b> por un valor de <b>${cop_value:,.0f} COP</b>. El saldo se ha acreditado a tu cuenta."
        )
        return True, f"¡Swap exitoso! Has convertido {format_num(amount_sd)} SD a ${cop_value:,.0f} COP."
    except Exception as e:
        conn.rollback()
        conn.close()
        return False, f"Error al procesar el swap: {str(e)}"

def submit_withdrawal_request(user_code, amount_cop, nequi_number):
    if amount_cop < 1000:
        return False, "El monto mínimo de retiro es de $1,000 pesos colombianos (COP)."
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance_cop, is_vip FROM users WHERE wallet_code = ?", (user_code,))
    res = cursor.fetchone()
    if not res or res[0] < amount_cop:
        conn.close()
        return False, "Saldo en pesos (COP) insuficiente para procesar el retiro."
    
    is_vip = res[1] if len(res) > 1 else 0
    fee_pct = 0.01 if is_vip == 1 else 0.02
    fee_cop = amount_cop * fee_pct
    net_cop = amount_cop - fee_cop
    
    try:
        # Descontar saldo de pesos COP de forma inmediata (congelar saldo para retiro)
        cursor.execute("UPDATE users SET balance_cop = balance_cop - ? WHERE wallet_code = ?", (amount_cop, user_code))
        
        # Registrar solicitud de retiro pendiente
        cursor.execute("""
            INSERT INTO withdrawal_requests (user_code, amount_cop, fee_cop, net_cop, nequi_number, status)
            VALUES (?, ?, ?, ?, ?, 'PENDING')
        """, (user_code, amount_cop, fee_cop, net_cop, nequi_number))
        
        conn.commit()
        conn.close()
        
        # Notificar al usuario
        add_notification(
            user_code,
            f"💸 <b>Solicitud de retiro recibida:</b> Has solicitado un retiro por <b>${amount_cop:,.0f} COP</b> a tu cuenta Nequi <b>{nequi_number}</b>. "
            f"Comisión del 2% (${fee_cop:,.0f} COP) deducida. Recibirás neto <b>${net_cop:,.0f} COP</b> una vez que el administrador lo apruebe."
        )
        return True, "Solicitud de retiro enviada con éxito. El administrador la validará pronto."
    except Exception as e:
        conn.rollback()
        conn.close()
        return False, f"Error al procesar el retiro: {str(e)}"

def get_pending_withdrawals():
    conn = get_db_connection()
    df = pd.read_sql_query("""
        SELECT w.id, w.user_code, w.amount_cop, w.fee_cop, w.net_cop, w.nequi_number, w.timestamp, u.fullname, u.username
        FROM withdrawal_requests w
        JOIN users u ON w.user_code = u.wallet_code
        WHERE w.status = 'PENDING'
        ORDER BY w.timestamp ASC
    """, conn)
    conn.close()
    return df

def get_user_withdrawals(user_code):
    conn = get_db_connection()
    df = pd.read_sql_query("""
        SELECT id, amount_cop, fee_cop, net_cop, nequi_number, receipt_image, status, timestamp
        FROM withdrawal_requests
        WHERE user_code = ?
        ORDER BY timestamp DESC
    """, conn, params=(user_code,))
    conn.close()
    return df
def get_platform_fees_summary():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Total fees generated
    cursor.execute("SELECT SUM(fee_cop) FROM withdrawal_requests WHERE status = 'APPROVED'")
    total_fees = cursor.fetchone()[0] or 0.0
    
    # Locked fees (approved within the last 24 hours)
    # Compare against UTC since SQLite uses UTC CURRENT_TIMESTAMP
    cursor.execute("""
        SELECT SUM(fee_cop) FROM withdrawal_requests 
        WHERE status = 'APPROVED' AND approved_at >= datetime('now', '-1 day')
    """)
    locked_fees = cursor.fetchone()[0] or 0.0
    
    # Available fees (approved more than 24 hours ago)
    cursor.execute("""
        SELECT SUM(fee_cop) FROM withdrawal_requests 
        WHERE status = 'APPROVED' AND fee_status = 'UNCLAIMED' AND (approved_at < datetime('now', '-1 day') OR approved_at IS NULL)
    """)
    available_fees = cursor.fetchone()[0] or 0.0
    
    conn.close()
    return total_fees, locked_fees, available_fees

def claim_platform_fees():
    total_fees, locked_fees, available_fees = get_platform_fees_summary()
    if available_fees <= 0:
        return False, "No hay comisiones de plataforma liberadas disponibles para reclamar en este momento."
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Mark as CLAIMED
        cursor.execute("""
            UPDATE withdrawal_requests 
            SET fee_status = 'CLAIMED' 
            WHERE status = 'APPROVED' AND fee_status = 'UNCLAIMED' AND (approved_at < datetime('now', '-1 day') OR approved_at IS NULL)
        """)
        # Add to admin's balance_cop
        cursor.execute("UPDATE users SET balance_cop = balance_cop + ? WHERE username = 'admin'", (available_fees,))
        conn.commit()
        conn.close()
        return True, f"¡Éxito! Se han transferido ${available_fees:,.0f} COP de comisiones liberadas a tu balance en pesos de administrador."
    except Exception as e:
        conn.rollback()
        conn.close()
        return False, f"Error al reclamar comisiones: {str(e)}"

def get_approved_withdrawals_fees():
    conn = get_db_connection()
    df = pd.read_sql_query("""
        SELECT w.id, w.user_code, w.amount_cop, w.fee_cop, w.approved_at, w.fee_status, u.fullname
        FROM withdrawal_requests w
        JOIN users u ON w.user_code = u.wallet_code
        WHERE w.status = 'APPROVED'
        ORDER BY w.approved_at DESC
    """, conn)
    conn.close()
    return df


def approve_withdrawal(request_id, receipt_bytes):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_code, amount_cop, fee_cop, net_cop, nequi_number FROM withdrawal_requests WHERE id = ?", (request_id,))
    res = cursor.fetchone()
    if res:
        user_code, amount_cop, fee_cop, net_cop, nequi_number = res
        try:
            cursor.execute("UPDATE withdrawal_requests SET status = 'APPROVED', receipt_image = ?, approved_at = CURRENT_TIMESTAMP WHERE id = ?", (receipt_bytes, request_id))
            conn.commit()
            conn.close()
            
            # Enviar notificación oficial con el comprobante adjunto
            add_notification(
                user_code,
                f"🟢 <b>¡Retiro aprobado y pagado!</b> El administrador confirmó el envío de <b>${net_cop:,.0f} COP</b> "
                f"a tu cuenta Nequi <b>{nequi_number}</b> (descontando la comisión del 2% de ${fee_cop:,.0f} COP). "
                f"La captura del comprobante oficial ha sido adjuntada con éxito en tu historial."
            )
            return True, "Retiro aprobado con éxito. El comprobante ha sido compartido con el usuario."
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, f"Error al aprobar retiro: {str(e)}"
    conn.close()
    return False, "No se encontró la solicitud de retiro."

def reject_withdrawal(request_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_code, amount_cop FROM withdrawal_requests WHERE id = ?", (request_id,))
    res = cursor.fetchone()
    if res:
        user_code, amount_cop = res
        try:
            cursor.execute("UPDATE withdrawal_requests SET status = 'REJECTED' WHERE id = ?", (request_id,))
            # Devolver saldo de COP al usuario
            cursor.execute("UPDATE users SET balance_cop = balance_cop + ? WHERE wallet_code = ?", (amount_cop, user_code))
            conn.commit()
            conn.close()
            
            # Notificar al usuario
            add_notification(
                user_code,
                f"🔴 <b>Retiro rechazado:</b> Tu solicitud de retiro por <b>${amount_cop:,.0f} COP</b> fue rechazada. "
                f"Los fondos congelados han sido reembolsados en su totalidad a tu saldo retirable (COP)."
            )
            return True
        except Exception as e:
            conn.rollback()
            conn.close()
            return False
    conn.close()
    return False

def get_user_bsc_address(wallet_code):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT bsc_address FROM users WHERE wallet_code = ?", (wallet_code,))
    res = cursor.fetchone()
    conn.close()
    return res[0] if res and res[0] else ""

def update_user_bsc_address(wallet_code, bsc_address):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET bsc_address = ? WHERE wallet_code = ?", (bsc_address, wallet_code))
    conn.commit()
    conn.close()
    return True

@st.cache_data(ttl=15)
def fetch_bep20_balance_rpc(wallet_address, contract_address="0xC324649213ec1757190bc4b78bcD41Cc1545C264", rpc_url="https://bsc-dataseed.binance.org/"):
    if not wallet_address or not wallet_address.strip().startswith("0x"):
        return 0.0
    try:
        addr = wallet_address.strip()
        if addr.startswith("0x"):
            addr = addr[2:]
        if len(addr) != 40:
            return 0.0
        
        # balanceOf selector is 0x70a08231
        data = "0x70a08231" + addr.lower().zfill(64)
        
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_call",
            "params": [
                {
                    "to": contract_address,
                    "data": data
                },
                "latest"
            ],
            "id": 1
        }
        
        response = requests.post(rpc_url, json=payload, timeout=3)
        if response.status_code == 200:
            result = response.json().get("result")
            if result and result != "0x":
                raw_balance = int(result, 16)
                return raw_balance / 10**18
    except Exception:
        pass
    return 0.0


# --- INTERFAZ GRÁFICA ---


# Inyectar Script para Forzar Modo Escritorio completo de 1280px en celulares y tablets para visibilidad total de la app
st.markdown("""
<script>
    // Buscar el viewport tag de Streamlit e intercambiarlo por una vista fija de escritorio (1280px)
    var updateViewport = function() {
        var viewport = document.querySelector("meta[name=viewport]");
        if (viewport) {
            viewport.setAttribute("content", "width=1280, initial-scale=0.35, minimum-scale=0.1, maximum-scale=5.0, user-scalable=yes");
        } else {
            var meta = document.createElement('meta');
            meta.name = "viewport";
            meta.content = "width=1280, initial-scale=0.35, minimum-scale=0.1, maximum-scale=5.0, user-scalable=yes";
            document.getElementsByTagName('head')[0].appendChild(meta);
        }
    };
    
    // Ejecutar inmediatamente y programar un intervalo por si Streamlit restablece el viewport al recargar
    updateViewport();
    setInterval(updateViewport, 1000);
</script>
""", unsafe_allow_html=True)


# Estilo visual moderno premium: Negro Absoluto, Amarillo Dorado y Botones Verdes con Borde Dorado
st.markdown("""
    <style>
    /* Ocultar marca de Streamlit para que parezca una App propia */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    .stDeployButton {display:none !important;}
    
    /* Mantener visible la cabecera para el botón de despliegue del menú pero totalmente transparente */
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
        background: transparent !important;
    }
    /* Fondo principal Negro Puro */
    .main {
        background-color: #000000 !important;
        color: #ffffff !important;
    }
    
    /* Botones Verdes Cripto con Bordes Dorados */
    .stButton>button {
        background: #10b981 !important; /* Verde cripto */
        color: #000000 !important; /* Texto negro para alto contraste */
        border: 2px solid #ffd700 !important; /* Borde dorado */
        border-radius: 6px !important;
        font-weight: 800 !important;
        padding: 0.4rem 1.0rem !important;
        font-size: 0.85rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }
    .stButton>button:hover {
        background: #059669 !important; /* Verde cripto oscuro al hover */
        border-color: #ffffff !important; /* Borde brilla blanco/dorado */
        color: #ffffff !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.4) !important; /* Glow verde cripto */
    }
    
    /* Tarjetas Negras/Grises con Bordes Dorados (Más compactas y visibles) */
    .card {
        background-color: #0d0d11 !important;
        padding: 0.65rem 0.8rem !important; /* Reducido de 1.0rem para máxima visibilidad */
        border-radius: 8px !important; /* Bordes ligeramente más finos */
        border: 1px solid #ffd700 !important; /* Delicado borde dorado */
        margin-bottom: 0.5rem !important; /* Margen reducido */
        box-shadow: 0 3px 10px rgba(255, 215, 0, 0.02) !important;
    }
    
    /* Notificaciones estilizadas */
    .notification-card {
        background-color: #0d0d11 !important;
        padding: 1rem !important;
        border-radius: 6px !important;
        border-left: 4px solid #ffd700 !important;
        border-right: 1px solid #1a1a24 !important;
        border-top: 1px solid #1a1a24 !important;
        border-bottom: 1px solid #1a1a24 !important;
        margin-bottom: 0.8rem !important;
    }
    
    /* Textos en Amarillo Dorado */
    .golden-title {
        color: #ffd700 !important;
        font-weight: 700 !important;
    }
    
    .metric-title {
        color: #ffd700 !important; /* Amarillo dorado */
        font-size: 0.72rem !important; /* Tamaño compacto */
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.07em;
    }
    .metric-value {
        font-size: 1.25rem !important; /* Tamaño compacto */
        font-weight: 800 !important;
        margin: 3px 0 !important;
        color: #ffffff;
    }
    .metric-sub {
        font-size: 0.7rem !important; /* Tamaño compacto */
        color: #a1a1aa !important;
    }
    
    /* Estilización del menú lateral */
    section[data-testid="stSidebar"] {
        background-color: #060608 !important;
        border-right: 2px solid #ffd700 !important; /* Línea divisoria dorada */
    }
    
    /* Evitar la línea amarilla huérfana en el borde de la pantalla cuando el menú se minimiza por completo */
    section[data-testid="stSidebar"][data-collapsed="true"] {
        border-right: none !important;
    }
    
    /* Input fields estilizados */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #0d0d11 !important;
        color: #ffffff !important;
        border: 1px solid #3f3f46 !important;
    }
    .stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus {
        border-color: #ffd700 !important;
    }

    /* Ocultar por completo el círculo de selección de radio nativo de Streamlit */
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] input[type="radio"] {
        display: none !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label > div:not(:has([data-testid="stMarkdownContainer"])) {
        display: none !important;
        width: 0 !important;
        height: 0 !important;
        opacity: 0 !important;
        visibility: hidden !important;
    }
    /* Asegurar que el contenedor del texto del botón esté siempre visible y ocupe el 100% de la tarjeta */
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label > div:has([data-testid="stMarkdownContainer"]) {
        display: flex !important;
        width: 100% !important;
        justify-content: center !important;
        align-items: center !important;
    }
    
    /* CONVERTIR MENÚ DE NAVEGACIÓN EN BOTONES GRANDES (CUADROS/TARJETAS FÍSICAS IDÉNTICAS AL BOTÓN DE CERRAR SESIÓN) */
    [data-testid="stSidebar"] [data-testid="stRadio"] legend, 
    [data-testid="stSidebar"] [data-testid="stRadio"] > label {
        color: #ffd700 !important; /* Título en Amarillo Dorado */
        font-size: 1.15rem !important;
        font-weight: 850 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        margin-bottom: 15px !important;
        display: block !important;
        text-align: center !important;
        border-bottom: 2px solid #ffd70033 !important;
        padding-bottom: 8px !important;
    }

    /* Estilo del Botón de Navegación */
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label,
    [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input[type="radio"]),
    [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"] {
        padding: 22px 14px !important; /* Cuadros mucho más grandes y cómodos, facilísimos de presionar */
        min-height: 80px !important; /* Altura ideal de cuadro táctil premium */
        background: #0d0d11 !important; /* Fondo tipo botón negro oscuro premium de base */
        border: 2px solid #ffd70088 !important; /* Borde dorado sólido como el botón de Cerrar Sesión */
        border-radius: 6px !important; /* Esquinas como el botón de Cerrar Sesión */
        width: 100% !important; /* Cubre todo el ancho del sidebar */
        display: flex !important;
        justify-content: center !important; /* Centrado absoluto del texto */
        align-items: center !important;
        cursor: pointer !important;
        margin: 0 !important;
        box-shadow: 0 5px 12px rgba(0, 0, 0, 0.5) !important; /* Sombra tridimensional real */
        transition: all 0.15s ease-in-out !important;
    }

    /* Separación amplia entre cuadros independientes */
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] > div,
    [data-testid="stSidebar"] [data-testid="stRadio"] div[data-baseweb="radio"] {
        margin-bottom: 18px !important; /* Amplia separación para diseño ultra limpio y fácil de tocar */
    }

    /* Efecto Hover: Brillo dorado completo */
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label:hover,
    [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input[type="radio"]):hover,
    [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"]:hover {
        border-color: #ffd700 !important; /* El borde brilla dorado full */
        background: #161620 !important; /* Brillo sutil de fondo */
        box-shadow: 0 6px 16px rgba(255, 215, 0, 0.15) !important;
        transform: translateY(-2px) !important; /* Elevación física de botón */
    }

    /* EFECTO CLICK ELÁSTICO (AL PRESIONAR SE HUNDE DE FORMA FÍSICA Y REALISTA) */
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label:active,
    [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input[type="radio"]):active,
    [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"]:active {
        transform: scale(0.94) translateY(3px) !important; /* Se hunde de verdad al presionarlo */
        border-color: #ffffff !important; /* El borde destella en blanco al presionar */
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.7) !important;
    }

    /* Texto súper claro, grande e impactante dentro de cada cuadro */
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input[type="radio"]) [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"] [data-testid="stMarkdownContainer"] p {
        font-size: 1.15rem !important; /* Letra extra grande para lectura súper cómoda */
        font-weight: 850 !important; /* Estilo extra grueso de alta visibilidad */
        color: #ffffff !important; /* Texto blanco en reposo */
        text-align: center !important;
        width: 100% !important;
        letter-spacing: 0.04em !important;
        margin: 0 !important;
        text-transform: uppercase !important; /* Todo en mayúsculas estilo botón físico de acción */
    }

    /* CUANDO UN CUADRO ESTÁ ACTIVO/SELECCIONADO: IDÉNTICO AL BOTÓN DE CERRAR SESIÓN (Fondo Verde Cripto + Borde Dorado) */
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label:has(input[type="radio"]:checked),
    [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input[type="radio"]:checked),
    [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"]:has(input[type="radio"]:checked) {
        background: #10b981 !important; /* Verde cripto esmeralda exacto de Cerrar Sesión */
        border: 2px solid #ffd700 !important; /* Borde dorado sólido brillante */
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4) !important; /* Glow verde cripto */
    }

    /* Texto de color negro de alto contraste cuando el botón está activo/seleccionado */
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label:has(input[type="radio"]:checked) [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input[type="radio"]:checked) [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"]:has(input[type="radio"]:checked) [data-testid="stMarkdownContainer"] p {
        color: #000000 !important; /* Texto negro para contraste espectacular sobre verde cripto */
        font-weight: 900 !important;
    }

    /* FORZAR 3 COLUMNAS COMPACTAS DE BALANCES EN DISPOSITIVOS MÓVILES (CELULAR) */
    @media (max-width: 640px) {
        div[data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            align-items: stretch !important;
            gap: 5px !important;
            width: 100% !important;
        }
        div[data-testid="column"] {
            flex: 1 1 0% !important;
            min-width: 0 !important;
        }
        /* Reducir tamaño de tarjetas y amontonamiento en celulares */
        div.card {
            min-height: 100px !important;
            padding: 4px 2px !important;
            margin-bottom: 2px !important;
        }
        /* Ajustar la columna central de dos tarjetas pequeñas apiladas */
        div.card[style*="min-height: 61px"] {
            min-height: 48px !important;
            margin-bottom: 4px !important;
            padding: 2px 2px !important;
        }
        /* Forzar tamaños de texto compactos en móvil */
        .metric-title {
            font-size: 0.48rem !important;
            letter-spacing: 0.01em !important;
            line-height: 0.65rem !important;
        }
        .metric-value {
            font-size: 0.75rem !important;
            margin: 1px 0 !important;
        }
        .metric-sub {
            font-size: 0.42rem !important;
            line-height: 0.55rem !important;
        }
    }


    /* BOTÓN DE FLECHITAS PARA COLAPSAR/EXPANDIR EL MENÚ (SÚPER LLAMATIVO EN DORADO Y GLOW NEÓN) */
    [data-testid="stSidebarCollapseButton"] button, 
    [data-testid="stHeader"] button:has(svg),
    button[aria-label="Collapse sidebar"],
    button[aria-label="Expand sidebar"] {
        background: linear-gradient(135deg, #ffd700 0%, #b8860b 100%) !important; /* Fondo Degradado Amarillo Dorado */
        color: #000000 !important; /* Icono o flechita negra para alto contraste */
        border: 2px solid #ffffff !important; /* Borde blanco brillante */
        border-radius: 50% !important; /* Completamente redondo */
        width: 44px !important;
        height: 44px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.85) !important; /* Brillo dorado neón súper llamativo */
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        z-index: 999999 !important;
        cursor: pointer !important;
    }

    /* Animación de giro y pulsación al pasar el mouse por encima de la flecha */
    [data-testid="stSidebarCollapseButton"] button:hover, 
    [data-testid="stHeader"] button:has(svg):hover,
    button[aria-label="Collapse sidebar"]:hover,
    button[aria-label="Expand sidebar"]:hover {
        transform: scale(1.18) !important; /* Se agranda físicamente */
        background: #10b981 !important; /* Cambia a verde cripto al hover */
        border-color: #ffd700 !important; /* Borde brilla dorado */
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.95) !important; /* Brillo verde cripto súper intenso */
    }

    /* Modificar los vectores SVG del icono dentro del botón para que se vean de color negro puro de alto contraste */
    [data-testid="stSidebarCollapseButton"] button svg, 
    [data-testid="stHeader"] button:has(svg) svg,
    button[aria-label="Collapse sidebar"] svg,
    button[aria-label="Expand sidebar"] svg {
        fill: #000000 !important;
        color: #000000 !important;
        stroke: #000000 !important;
        stroke-width: 2.5px !important;
        width: 22px !important;
        height: 22px !important;
    }

    </style>
""", unsafe_allow_html=True)

# Inicializar sesión
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.fullname = None
    st.session_state.email = None
    st.session_state.wallet_code = None
    st.session_state.is_admin = False


# Cargar configuraciones del token personalizado (Alianza - SD)
token = get_token_settings()

# Cargar cotizaciones globales via API
btc_price = fetch_btc_price()
usd_cop = fetch_usd_cop_rate()

# Cargar precio en tiempo real de DexScreener (Contrato: 0xC324649213ec1757190bc4b78bcD41Cc1545C264)
live_sd_price = fetch_sd_price_from_dexscreener()
if live_sd_price is not None and live_sd_price > 0:
    token_price_usd = live_sd_price
    # Sincronizar automáticamente en la BD para que quede actualizado si el admin no lo cambia manualmente
    try:
        conn_sync = get_db_connection()
        cursor_sync = conn_sync.cursor()
        cursor_sync.execute("UPDATE token_settings SET token_price_usd = ? WHERE id = 1", (live_sd_price,))
        conn_sync.commit()
        conn_sync.close()
    except Exception:
        pass
else:
    token_price_usd = token['price_usd']

token_price_cop = token_price_usd * usd_cop

# Formatear el precio del token de forma dinámica (con precisión inteligente para monedas de bajo coste)
token_price_usd_formatted = format_usd_price(token_price_usd)

# Mostrar precio flotante del token en la parte superior derecha en color verde neón llamativo
st.markdown(f"""
<div style="
    position: fixed;
    top: 12px;
    right: 60px;
    z-index: 999999;
    background: linear-gradient(135deg, #0d0d11 0%, #061f14 100%);
    border: 1.5px solid #10b981;
    border-radius: 30px;
    padding: 5px 15px;
    box-shadow: 0 0 12px rgba(16, 185, 129, 0.35);
    display: flex;
    align-items: center;
    gap: 6px;
    pointer-events: none;
">
    <span style="color: #ffd700; font-weight: 850; font-size: 0.85rem; letter-spacing: 0.05em; font-family: 'Segoe UI', sans-serif;">🪙 {token['symbol']}:</span>
    <span style="color: #10b981; font-weight: 900; font-size: 1.1rem; font-family: 'Segoe UI', sans-serif; text-shadow: 0 0 8px rgba(16,185,129,0.5);">
        {token_price_usd_formatted}
    </span>
</div>
""", unsafe_allow_html=True)

# El administrador ahora controla los precios de la membresía en la tienda directamente desde el panel de control.
# Ya no se fuerza automáticamente de forma dinámica al arrancar, respetando el valor guardado en base de datos.


if not st.session_state.logged_in:
    st.sidebar.title("🔐 Alianza CryptoWallet")
    st.sidebar.markdown("<div style='background-color: #1e293b; padding: 6px 12px; border-radius: 8px; border: 1px solid #334155; margin-bottom: 15px; text-align: center;'><span style='color: #ffd700; font-size: 0.85rem; font-weight: bold;'>🚀 Versión de la App: v64</span></div>", unsafe_allow_html=True)
    menu = st.sidebar.selectbox("Seleccione una opción", ["Iniciar Sesión", "Registrarse"])
    
    if menu == "Iniciar Sesión":
        st.markdown("<h2 class='golden-title'>🔑 Iniciar Sesión</h2>", unsafe_allow_html=True)
        with st.form("login_form"):
            username = st.text_input("Nombre de Usuario", placeholder="Ej. juan123")
            password = st.text_input("Contraseña", type="password", placeholder="******")
            submit = st.form_submit_button("Ingresar")
            
            if submit:
                if username and password:
                    user = login_user(username, password)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user_id = user[0]
                        st.session_state.username = user[1]
                        st.session_state.fullname = user[2]
                        st.session_state.email = user[3]
                        st.session_state.wallet_code = user[4]
                        st.session_state.is_admin = bool(user[6])
                        st.success(f"¡Bienvenido de nuevo, {user[2]}!")
                        st.rerun()
                    else:
                        st.error("Usuario o contraseña incorrectos.")
                else:
                    st.warning("Por favor completa todos los campos.")
                    
    elif menu == "Registrarse":
        st.markdown("<h2 class='golden-title'>📝 Registro de Cuenta</h2>", unsafe_allow_html=True)
        with st.form("register_form"):
            fullname = st.text_input("Nombre Completo", placeholder="Ej. Juan Pérez")
            email = st.text_input("Correo Electrónico", placeholder="Ej. juan@correo.com")
            username = st.text_input("Nombre de Usuario Único", placeholder="Ej. juan123")
            password = st.text_input("Contraseña", type="password", placeholder="Mínimo 6 caracteres")
            confirm_password = st.text_input("Confirmar Contraseña", type="password", placeholder="******")
            referred_by = st.text_input("Código de Referido (Opcional - 5 dígitos)", max_chars=5, placeholder="Ej. 12345")
            submit = st.form_submit_button("Crear Cuenta")
            
            if submit:
                if not (fullname and email and username and password and confirm_password):
                    st.warning("Todos los campos son obligatorios.")
                elif password != confirm_password:
                    st.error("Las contraseñas no coinciden.")
                elif len(password) < 8:
                    st.error("⚠️ Por seguridad criptográfica, la contraseña debe tener al menos 8 caracteres.")
                elif any(weak in password.lower() for weak in ['123456', '12345678', 'admin123', 'password', 'contraseña', 'qwerty', 'alianza123']):
                    st.error("⚠️ ¡Contraseña demasiado débil o expuesta! Tu navegador o sistema la detectará como 'hackeada' o comprometida. Elige una clave más robusta combinando letras, números y símbolos.")
                else:
                    ref_code = referred_by.strip() if referred_by else None
                    success, result = register_user(username, password, fullname, email, ref_code)
                    if success:
                        st.balloons()
                        st.success("¡Registro Exitoso!")
                        st.markdown(f"""
                        <div class="card" style="border-left: 5px solid #ffd700;">
                            <h4 style='color: #ffd700; margin:0;'>🔐 Tu Código de Billetera Único (Inmutable)</h4>
                            <p style='font-size: 1.8rem; font-weight: bold; margin: 10px 0; color: #ffffff;'>{result}</p>\n                            <p style='font-size: 0.85rem; color: #a1a1aa; margin:0;'>
                                ⚠️ Guarda este código de 5 dígitos. Lo necesitarás para recibir transferencias de otros usuarios o del propietario de la app.
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error(result)

else:
    # Sidebar de usuario conectado con toques dorados
    st.sidebar.markdown(f"<h2 class='golden-title'>👋 {st.session_state.fullname}</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("<div style='background-color: #1e293b; padding: 6px 12px; border-radius: 8px; border: 1px solid #334155; margin-bottom: 15px; text-align: center;'><span style='color: #ffd700; font-size: 0.85rem; font-weight: bold;'>🚀 Versión de la App: v64</span></div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"**Billetera ID (Código):** `{st.session_state.wallet_code}`")
    
    # Obtener el número de notificaciones pendientes
    unread_notifs = get_unread_notifications_count(st.session_state.wallet_code)
    notif_label = f"🔔 Notificaciones ({unread_notifs})" if unread_notifs > 0 else "🔔 Notificaciones"
    
    # Balance actualizado
    balance, wallet_code, balance_cop_user, is_vip_user = get_user_balance(st.session_state.username)
    st.session_state.wallet_code = wallet_code
    
    # RESPALDO DE BALANCE EN BASE DE DATOS LOCAL
    balance_db = balance

    # Sincronización automática de saldo con la Blockchain (Binance Smart Chain) si tiene billetera registrada
    user_bsc_wallet = get_user_bsc_address(st.session_state.wallet_code)
    if "sync_blockchain" not in st.session_state:
        st.session_state.sync_blockchain = True
        
    if user_bsc_wallet and st.session_state.sync_blockchain:
        blockchain_balance = fetch_bep20_balance_rpc(user_bsc_wallet, token['contract'])
        # NOTA: Para permitir desincronizar la billetera y mantener el saldo local intacto en SQLite,
        # NO sobrescribimos permanentemente la base de datos al sincronizar. Esto permite al usuario
        # "apagar" la sincronización y recuperar su saldo local original de la base de datos de la app.
        balance = blockchain_balance
    
    # Cálculos de balance
    balance_usd = balance * token_price_usd
    balance_cop_equiv = balance_usd * usd_cop
    
    nav_options = ["🏠 Inicio y Balance", "💸 Enviar SD", "📥 Comprar SD", "🔄 Swap y Retiros", "🛍️ Tienda Alianza", "🚚 Mensajería Alianza", "👥 Mis Referidos", notif_label, "👤 Mi Perfil", "🛡️ Términos y Seguridad"]
    
    # El checkbox de Modo Propietario ahora es exclusivo para la cuenta del propietario de la app (@admin) o wallet_code '99999'
    is_owner_user = (st.session_state.username == 'admin' or st.session_state.wallet_code == '99999' or st.session_state.is_admin)
    if is_owner_user:
        show_admin_panel = st.sidebar.checkbox("🔓 Modo Propietario (Admin)", value=st.session_state.is_admin)
        if show_admin_panel:
            if "👑 Panel del Propietario" not in nav_options:
                nav_options.append("👑 Panel del Propietario")
    elif st.session_state.is_admin:
        if "👑 Panel del Propietario" not in nav_options:
            nav_options.append("👑 Panel del Propietario")
        
    choice = st.sidebar.radio("🌐 Todas las ventanas de la app", nav_options)
    
    if st.sidebar.button("🚪 Cerrar Sesión"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.fullname = None
        st.session_state.email = None
        st.session_state.wallet_code = None
        st.session_state.is_admin = False
        st.rerun()

    # --- INICIO Y BALANCE ---
    if choice == "🏠 Inicio y Balance":
        if is_vip_user == 1:
            col_title, col_vip_badge = st.columns([3, 1])
            with col_title:
                st.markdown(f"<h1 class='golden-title'>💼 Billetera de {st.session_state.fullname}</h1>", unsafe_allow_html=True)
                st.markdown("<span style='color: #ffd700; font-weight: bold; font-size: 1.1rem; display: flex; align-items: center; gap: 8px;'>👑 ¡BIENVENIDO MIEMBRO VIP ALIANZA! Disfrutas de comisiones de retiro reducidas (1%) y ganancias de referidos al 25% de por vida.</span>", unsafe_allow_html=True)
            with col_vip_badge:
                st.image(f"data:image/jpeg;base64,{VIP_BADGE_B64}", width=110)
        else:
            st.markdown(f"<h1 class='golden-title'>💼 Billetera de {st.session_state.fullname}</h1>", unsafe_allow_html=True)
            
        # Fila de Logos Responsivos en la parte superior (SIAD, BINANCE, METAMASK y Dólar/COP)
        st.markdown('<div style="display: flex; align-items: center; justify-content: center; gap: 25px; margin: 20px 0 30px 0; flex-wrap: wrap; padding: 12px 20px; background-color: #08080c; border: 1px solid rgba(255,215,0,0.15); border-radius: 15px; box-shadow: inset 0 0 15px rgba(0,0,0,0.6);"><!-- Binance Coin (BNB) --><div style="text-align: center;"><div style="width: 58px; height: 58px; background: linear-gradient(135deg, #f3ba2f 0%, #a37500 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; font-weight: 900; color: #000000; box-shadow: 0 0 15px rgba(243,186,47,0.45), inset 0 2px 4px rgba(255,255,255,0.4); border: 2px solid rgba(255,255,255,0.15); text-shadow: 0 1px 1px rgba(255,255,255,0.25);">BNB</div><div style="font-size: 0.72rem; color: #a1a1aa; margin-top: 8px; font-weight: 800; letter-spacing: 0.05em; text-transform: uppercase;">Binance</div></div><div style="color: rgba(255,215,0,0.2); font-size: 1.1rem; font-weight: 300; margin-top: -15px;">⚡</div><!-- SIAD (SD) - KING OF COINS (Enlarged, double golden border, intense sunburst glow) --><div style="text-align: center; transform: scale(1.15);"><div style="width: 72px; height: 72px; background: linear-gradient(135deg, #ffe066 0%, #d4af37 50%, #8a6f0d 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.65rem; font-weight: 950; color: #000000; box-shadow: 0 0 30px rgba(255, 215, 0, 0.75), inset 0 3px 5px rgba(255,255,255,0.7); border: 3px solid #ffd700; text-shadow: 0 1px 2px rgba(255,255,255,0.4); font-family: sans-serif;">SD</div><div style="font-size: 0.8rem; color: #ffd700; margin-top: 8px; font-weight: 900; letter-spacing: 0.07em; text-shadow: 0 0 8px rgba(255,215,0,0.3); text-transform: uppercase;">SIAD TOKEN</div></div><div style="color: rgba(255,215,0,0.2); font-size: 1.1rem; font-weight: 300; margin-top: -15px;">⚡</div><!-- MetaMask Fox (MM) --><div style="text-align: center;"><div style="width: 58px; height: 58px; background: linear-gradient(135deg, #e2761f 0%, #803000 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.7rem; font-weight: 900; color: #ffffff; box-shadow: 0 0 15px rgba(226,117,31,0.45), inset 0 2px 4px rgba(255,255,255,0.4); border: 2px solid rgba(255,255,255,0.15); text-shadow: 0 1px 1px rgba(0,0,0,0.35);">🦊</div><div style="font-size: 0.72rem; color: #a1a1aa; margin-top: 8px; font-weight: 800; letter-spacing: 0.05em; text-transform: uppercase;">MetaMask</div></div><div style="color: rgba(255,215,0,0.2); font-size: 1.1rem; font-weight: 300; margin-top: -15px;">⚡</div><!-- Dollar/COP (FIAT) --><div style="text-align: center;"><div style="width: 58px; height: 58px; background: linear-gradient(135deg, #10b981 0%, #045a3a 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.55rem; font-weight: 950; color: #ffffff; box-shadow: 0 0 15px rgba(16,185,129,0.45), inset 0 2px 4px rgba(255,255,255,0.4); border: 2px solid rgba(255,255,255,0.15); text-shadow: 0 1px 2px rgba(0,0,0,0.3);">COP</div><div style="font-size: 0.72rem; color: #a1a1aa; margin-top: 8px; font-weight: 800; letter-spacing: 0.05em; text-transform: uppercase;">Fíat Peso</div></div></div>', unsafe_allow_html=True)
        
        # Alerta visual rápida si tiene notificaciones pendientes
        if unread_notifs > 0:
            st.info(f"📬 Tienes **{unread_notifs} nueva(s) notificación(es)** sin leer. Revísalas en la pestaña del menú lateral.")
            
        # Banner de estado de la Sincronización Blockchain
        if not user_bsc_wallet:
            st.warning("⚠️ **Sincronización Blockchain Inactiva:** No has configurado tu dirección de billetera real (BSC) en tu Perfil. Tu saldo actual es local. Vincula tu billetera MetaMask/Trust Wallet en **👤 Mi Perfil** para operar con tus tokens reales.")
        else:
            if st.session_state.sync_blockchain:
                col_banner, col_btn = st.columns([4, 1])
                with col_banner:
                    st.success(f"🔗 **Blockchain Sincronizada:** Conectado con éxito a Binance Smart Chain. Tu saldo real de tokens BEP-20 es de **{format_num(balance)} {token['symbol']}**.")
                with col_btn:
                    if st.button("❌ Desconectar", key="btn_desync_blockchain", help="Muestra el saldo local de la base de datos de la app"):
                        st.session_state.sync_blockchain = False
                        st.rerun()
            else:
                col_banner, col_btn = st.columns([4, 1])
                with col_banner:
                    st.info(f"💾 **Billetera Desconectada (Modo Local):** Mostrando los saldos locales de la base de datos de la aplicación.")
                with col_btn:
                    if st.button("🔗 Sincronizar", key="btn_sync_blockchain", help="Sincroniza y muestra tu saldo real de tokens BEP-20 de MetaMask"):
                        st.session_state.sync_blockchain = True
                        st.rerun()

        # Muestra del balance personal
        st.subheader("Balance de tu Cuenta")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="card" style="min-height: 130px; display: flex; flex-direction: column; justify-content: center; padding: 0.5rem 0.8rem !important;">
                <div class="metric-title">Balance en {token['symbol']} ({token['name']})</div>
                <div class="metric-value" style="color: #10b981; font-size: 1.4rem !important; margin: 3px 0 !important;">{format_num(balance)} {token['symbol']}</div>
                <div class="metric-sub">Puntos de tu cuenta</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="card" style="margin-bottom: 8px !important; min-height: 61px; display: flex; flex-direction: column; justify-content: center; padding: 0.35rem 0.8rem !important;">
                <div class="metric-title" style="font-size: 0.68rem !important;">Equivalente en Dólares (USD)</div>
                <div class="metric-value" style="color: #ffffff; font-size: 1.1rem !important; margin: 1px 0 !important;">${balance_usd:,.2f} USD</div>
                <div class="metric-sub" style="font-size: 0.62rem !important;">1 {token['symbol']} = {token_price_usd_formatted}</div>
            </div>
            <div class="card" style="margin-bottom: 0px !important; min-height: 61px; display: flex; flex-direction: column; justify-content: center; padding: 0.35rem 0.8rem !important;">
                <div class="metric-title" style="font-size: 0.68rem !important;">Valor Teórico en Pesos</div>
                <div class="metric-value" style="color: #ffffff; font-size: 1.1rem !important; margin: 1px 0 !important;">${balance_cop_equiv:,.0f} COP</div>
                <div class="metric-sub" style="font-size: 0.62rem !important;">Tasa: $1 USD = ${usd_cop:,.2f} COP</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="card" style="border-color: #ffd700; min-height: 130px; display: flex; flex-direction: column; justify-content: center; padding: 0.5rem 0.8rem !important;">
                <div class="metric-title">Saldo Retirable (COP)</div>
                <div class="metric-value" style="color: #ffd700; font-size: 1.4rem !important; margin: 3px 0 !important;">${balance_cop_user:,.0f} COP</div>
                <div class="metric-sub">Saldo líquido cambiado para retiro</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Si es el Administrador, permitirle editar sus saldos directamente según su necesidad
        if st.session_state.username == 'admin' or st.session_state.wallet_code == '99999':
            st.markdown("### 🔧 Panel de Edición de Balances del Administrador")
            with st.expander("🛠️ Ajustar Mis Saldos de Administrador (Edición Directa)", expanded=True):
                st.write("Como administrador, puedes modificar tu saldo de Alianza (SD), tu saldo retirable de pesos (COP) y el Nequi oficial para recibir pagos de usuarios:")
                col_eb1, col_eb2 = st.columns(2)
                with col_eb1:
                    admin_new_sd = st.number_input("Establecer mi saldo de Alianza (SD):", value=float(balance), min_value=0.0, format="%.4f")
                    admin_new_nequi = st.text_input("Número de Cuenta NEQUI Oficial (Cuenta Madre):", value=token['nequi_number'], max_chars=11)
                with col_eb2:
                    admin_new_cop = st.number_input("Establecer mi saldo Retirable (COP):", value=float(balance_cop_user), min_value=0.0, format="%.0f")
                
                if st.button("Guardar Cambios de Saldo y Configuración", key="save_admin_balances_btn"):
                    update_user_balance_and_cop(st.session_state.wallet_code, admin_new_sd, admin_new_cop)
                    if admin_new_nequi and len(admin_new_nequi) >= 10:
                        update_global_nequi(admin_new_nequi)
                    st.success("¡Tus saldos y configuración de Nequi oficial se han actualizado con éxito!")
                    st.rerun()

        # Mercado en Vivo
        st.subheader("📊 Cotización y Mercado en Vivo")
        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1:
            st.markdown(f"""
            <div class="card" style="border-top: 3px solid #ffd700; min-height: 96px; display: flex; flex-direction: column; justify-content: center; padding: 0.5rem 0.8rem !important; margin-bottom: 4px !important;">
                <div class="metric-title">🪙 {token['name']} ({token['symbol']})</div>
                <div class="metric-value" style="font-size: 1.25rem !important; margin: 2px 0 !important;">{token_price_usd_formatted}</div>
                <div class="metric-sub">Valor en COP: ${token_price_cop:,.2f} COP</div>
            </div>
            """, unsafe_allow_html=True)
            # Mostrar contrato
            st.caption("📜 Dirección de Contrato:")
            st.code(token['contract'], language="text")
            
        with col_c2:
            st.markdown(f"""
            <div class="card" style="border-top: 3px solid #10b981; min-height: 96px; display: flex; flex-direction: column; justify-content: center; padding: 0.5rem 0.8rem !important; margin-bottom: 4px !important;">
                <div class="metric-title">₿ Bitcoin (BTC)</div>
                <div class="metric-value" style="font-size: 1.25rem !important; margin: 2px 0 !important;">${btc_price:,.2f} USD</div>
                <div class="metric-sub">Valor en COP: ${(btc_price*usd_cop):,.0f} COP</div>
            </div>
            """, unsafe_allow_html=True)
            st.caption("🌐 Fuente: Coinbase API (Tiempo Real)")
            
        with col_c3:
            st.markdown(f"""
            <div class="card" style="border-top: 3px solid #ffd700; min-height: 96px; display: flex; flex-direction: column; justify-content: center; padding: 0.5rem 0.8rem !important; margin-bottom: 4px !important;">
                <div class="metric-title">💵 Tasa de Cambio (USD/COP)</div>
                <div class="metric-value" style="font-size: 1.25rem !important; margin: 2px 0 !important;">${usd_cop:,.2f} COP</div>
                <div class="metric-sub">Valor de un Dólar en Pesos</div>
            </div>
            """, unsafe_allow_html=True)
            st.caption("🏦 Fuente: AwesomeAPI (Tiempo Real)")

        # Sección de Gráficos Interactivos
        st.subheader("📈 Gráficos de Análisis e Historial")
        
        tab_user, tab_token, tab_btc, tab_cop = st.tabs([
            "💰 Historial de Mi Cuenta", 
            f"🪙 Gráfico {token['symbol']}", 
            "₿ Gráfico Bitcoin (BTC)", 
            "💵 Gráfico Dólar / Peso (COP)"
        ])
        
        with tab_user:
            df_tx = get_transaction_history(st.session_state.wallet_code)
            if len(df_tx) == 0:
                st.info("Aún no tienes movimientos en tu cuenta. Cuando recibas tokens del propietario o envíes puntos, verás tu gráfico de balance acumulado aquí.")
            else:
                # Construir historial de balance
                history_data = []
                current_bal = 0.0
                history_data.append({
                    "Fecha": "Registro Inicial",
                    "Balance (Tokens)": 0.0,
                    "Balance (USD)": 0.0,
                    "Balance (COP)": 0.0
                })
                for idx, row in df_tx.iterrows():
                    amt = row['amount']
                    if row['receiver_code'] == st.session_state.wallet_code:
                        current_bal += amt
                    else:
                        current_bal -= amt
                    
                    history_data.append({
                        "Fecha": row['timestamp'],
                        "Balance (Tokens)": current_bal,
                        "Balance (USD)": current_bal * token_price_usd,
                        "Balance (COP)": current_bal * token_price_usd * usd_cop
                    })
                
                df_hist = pd.DataFrame(history_data)
                sel_currency = st.radio("Moneda para visualizar historial de balance:", ["Tokens", "Dólares (USD)", "Pesos (COP)"], horizontal=True)
                
                y_col = "Balance (Tokens)"
                color_line = "#10b981"
                prefix = ""
                suffix = f" {token['symbol']}"
                
                if sel_currency == "Dólares (USD)":
                    y_col = "Balance (USD)"
                    color_line = "#ffffff"
                    prefix = "$"
                    suffix = " USD"
                elif sel_currency == "Pesos (COP)":
                    y_col = "Balance (COP)"
                    color_line = "#ffd700"
                    prefix = "$"
                    suffix = " COP"
                
                fig = px.line(df_hist, x="Fecha", y=y_col, markers=True, template="plotly_dark")
                fig.update_traces(line_color=color_line, line_width=3)
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    yaxis_title=f"Balance ({sel_currency})",
                    title=f"Evolución de Balance Personal en {sel_currency}"
                )
                st.plotly_chart(fig, use_container_width=True)

        with tab_token:
            # DexScreener Embed iframe interactivo de una, directamente sin textos de información redundantes
            dex_embed_html = """
            <iframe src="https://dexscreener.com/bsc/0xC324649213ec1757190bc4b78bcD41Cc1545C264?embed=1&theme=dark&trades=0" 
                    width="100%" 
                    height="600" 
                    style="border:0; border-radius: 8px;">
            </iframe>
            """
            st.components.v1.html(dex_embed_html, height=620)
            
        with tab_btc:
            st.markdown("#### ₿ Gráfico Interactivo de **Bitcoin (BTC/USD)**")
            btc_embed_html = """
            <div class="tradingview-widget-container" style="height:550px;width:100%;">
              <div id="tradingview_btc" style="height:500px;width:100%;"></div>
              <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
              <script type="text/javascript">
              new TradingView.widget({
                "autosize": true,
                "symbol": "COINBASE:BTCUSD",
                "interval": "D",
                "timezone": "Etc/UTC",
                "theme": "dark",
                "style": "1",
                "locale": "es",
                "toolbar_bg": "#f1f3f6",
                "enable_publishing": false,
                "hide_side_toolbar": false,
                "allow_symbol_change": true,
                "container_id": "tradingview_btc"
              });
              </script>
            </div>
            """
            st.components.v1.html(btc_embed_html, height=570)
            
        with tab_cop:
            st.markdown("#### Historial de la Tasa de Cambio **Dólar a Peso Colombiano (USD/COP)**")
            df_cop = get_usd_cop_historical_data()
            fig_cop = px.line(df_cop, x="Fecha", y="Tasa (COP)", markers=True, template="plotly_dark")
            fig_cop.update_traces(line_color="#ffd700", line_width=3)
            fig_cop.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis_title="COP por USD"
            )
            st.plotly_chart(fig_cop, use_container_width=True)

        # Sección de Historiales de Operación Completo (Multitabs)
        st.subheader("📑 Historial Completo de Operaciones")
        
        tab_txs, tab_buys, tab_withdraws_user, tab_store_user = st.tabs([
            "💸 Envíos y Recibos",
            "📥 Compras de SD (Nequi)",
            "💰 Retiros a Nequi",
            "🛍️ Compras en Tienda"
        ])
        
        with tab_txs:
            df_tx_list = get_transaction_history(st.session_state.wallet_code)
            # Filtrar SYSTEM_STORE de las transacciones directas para no confundir al usuario (ya se ven en Compras en Tienda)
            df_tx_list = df_tx_list[df_tx_list['receiver_code'] != 'SYSTEM_STORE']
            if len(df_tx_list) > 0:
                df_disp = df_tx_list.copy()
                df_disp['Tipo'] = df_disp.apply(lambda r: "🟢 Recibido" if r['receiver_code'] == st.session_state.wallet_code else "🔴 Enviado", axis=1)
                df_disp['De'] = df_disp.apply(lambda r: "Tú (Billetera)" if r['sender_code'] == st.session_state.wallet_code else ("Owner/Sistema" if r['sender_code'] == "99999" else f"{r['sender_name']} ({r['sender_code']})"), axis=1)
                df_disp['Para'] = df_disp.apply(lambda r: "Tú (Billetera)" if r['receiver_code'] == st.session_state.wallet_code else f"{r['receiver_name']} ({r['receiver_code']})", axis=1)
                df_disp['Cantidad'] = df_disp['amount'].apply(lambda x: f"{format_num(x)} {token['symbol']}")
                df_disp['Equivalente USD'] = df_disp['amount'].apply(lambda x: f"${format_num(x * token_price_usd)} USD")
                df_disp['Equivalente COP'] = df_disp['amount'].apply(lambda x: f"${x * token_price_usd * usd_cop:,.0f} COP")
                
                df_disp = df_disp[['timestamp', 'Tipo', 'De', 'Para', 'Cantidad', 'Equivalente USD', 'Equivalente COP']]
                df_disp.columns = ['Fecha', 'Tipo', 'De/Remitente', 'Para/Destinatario', 'Monto Transado', 'Valor (USD)', 'Valor (COP)']
                st.dataframe(df_disp.iloc[::-1], use_container_width=True)
            else:
                st.info("No hay transferencias registradas todavía.")
                
        with tab_buys:
            user_purchases_df = get_user_purchases(st.session_state.wallet_code)
            if len(user_purchases_df) == 0:
                st.info("Aún no tienes solicitudes de compra de SD.")
            else:
                user_purchases_display = user_purchases_df.copy()
                user_purchases_display['Estado'] = user_purchases_display['status'].apply(
                    lambda s: "🟡 Pendiente" if s == 'PENDING' else ("🟢 Aprobada" if s == 'APPROVED' else "🔴 Rechazada")
                )
                user_purchases_display['Valor en Pesos'] = user_purchases_display['amount_cop'].apply(lambda x: f"${x:,.0f} COP")
                user_purchases_display['Tokens SD'] = user_purchases_display['amount_sd'].apply(lambda x: f"{format_num(x)} SD")
                
                for idx, r in user_purchases_display.iterrows():
                    with st.expander(f"📥 Compra #{r['id']} - {r['Fecha']} - {r['Estado']} ({r['Tokens SD']})"):
                        st.markdown(f"""
                        <p><b>Monto transferido:</b> {r['Valor en Pesos']}</p>
                        <p><b>Tokens SD solicitados:</b> {r['Tokens SD']}</p>
                        <p><b>Estado actual:</b> {r['Estado']}</p>
                        """, unsafe_allow_html=True)
                        if r['proof_image']:
                            st.markdown("<b>Tu comprobante enviado por Nequi:</b>", unsafe_allow_html=True)
                            try:
                                st.image(r['proof_image'], caption="Foto del recibo", width=250)
                            except Exception:
                                st.write("No se pudo cargar la imagen.")
                                
        with tab_withdraws_user:
            df_w_hist = get_user_withdrawals(st.session_state.wallet_code)
            if len(df_w_hist) == 0:
                st.info("No tienes solicitudes de retiros todavía.")
            else:
                for idx, row in df_w_hist.iterrows():
                    status_lbl = "🟡 Pendiente" if row['status'] == 'PENDING' else ("🟢 Pagado" if row['status'] == 'APPROVED' else "🔴 Rechazado / Reembolsado")
                    with st.expander(f"💸 Retiro #{row['id']} - {row['timestamp']} - {status_lbl} (${row['amount_cop']:,.0f} COP)"):
                        st.markdown(f"""
                        <p><b>Monto solicitado:</b> ${row['amount_cop']:,.0f} COP</p>
                        <p><b>Comisión cobrada:</b> ${row['fee_cop']:,.0f} COP</p>
                        <p><b>Neto enviado a Nequi ({row['nequi_number']}):</b> <span style="color:#10b981; font-weight:bold;">${row['net_cop']:,.0f} COP</span></p>
                        """, unsafe_allow_html=True)
                        if row['status'] == 'APPROVED' and row['receipt_image']:
                            st.markdown("<b>📸 Comprobante de pago del Administrador:</b>", unsafe_allow_html=True)
                            try:
                                st.image(row['receipt_image'], caption="Soporte de transferencia bancaria", width=250)
                            except Exception:
                                st.write("Soporte de pago no disponible.")
                                
        with tab_store_user:
            df_store_u = get_user_store_purchases(st.session_state.wallet_code)
            if len(df_store_u) == 0:
                st.info("No has realizado compras en la Tienda Alianza todavía.")
            else:
                for idx, row in df_store_u.iterrows():
                    status_lbl = "🟡 Pendiente" if row['status'] == 'PENDING' else ("🟢 Entregado" if row['status'] == 'DELIVERED' else "🔴 Cancelado / Reembolsado")
                    border_c = "#ffd700" if row['status'] == 'DELIVERED' else "#ef4444"
                    with st.expander(f"🛍️ Pedido #{row['id']} - {row['name']} - {row['timestamp']} - {status_lbl}"):
                        st.write(f"<b>Tokens gastados:</b> {row['price_sd']:,.4f} SD", unsafe_allow_html=True)
                        if row['status'] == 'DELIVERED':
                            if row['item_type'] == 'MEMBERSHIP':
                                st.success("👑 Membresía VIP activa y cargada en tu cuenta de por vida.")
                            else:
                                st.markdown(f"""
                                <div style="background-color: #0d0d11; padding: 10px; border-left: 3px solid {border_c}; margin-top:5px;">
                                    <span style="color:#ffd700; font-weight:bold;">Código/Pin de tu producto:</span>
                                    <br><code style="font-size:1.15rem; color:#ffffff;">{row['code_delivered']}</code>
                                </div>
                                """, unsafe_allow_html=True)

    # --- ENVIAR PUNTOS ---
    elif choice == "💸 Enviar SD":
        st.markdown(f"<h1 class='golden-title'>💸 Enviar {token['name']} ({token['symbol']})</h1>", unsafe_allow_html=True)
        st.write(f"Transfiere saldo de **{token['name']} ({token['symbol']})** a otro usuario de forma instantánea usando su código de billetera.")
        
        col_f, col_i = st.columns([2, 1])
        with col_f:
            with st.form("send_form"):
                rec_code = st.text_input("Código de Billetera del Destinatario (5 dígitos)", max_chars=5, placeholder="Ej. 54321")
                amount = st.number_input(f"Cantidad de {token['symbol']} a enviar", min_value=0.0001, format="%.4f")
                submit = st.form_submit_button("Confirmar Envío Directo")
                
                if submit:
                    if len(rec_code) != 5 or not rec_code.isdigit():
                        st.error("El código debe constar exactamente de 5 dígitos numéricos.")
                    elif amount <= 0:
                        st.error("El monto debe ser mayor que cero.")
                    else:
                        success, msg = send_points(st.session_state.wallet_code, rec_code, amount)
                        if success:
                            st.balloons()
                            st.success(msg)
                        else:
                            st.error(msg)
                            
        with col_i:
            st.markdown(f"""
            <div class="card" style="border-left: 5px solid #10b981;">
                <h4 style="margin-top:0; color: #ffd700;">💡 Consejos de Uso</h4>
                <ul style="padding-left: 18px; font-size: 0.9rem; color: #ffffff; line-height: 1.4rem;">
                    <li>El envío de monedas entre billeteras de esta red se efectúa en segundos.</li>\n                    <li>Por seguridad, las transacciones no son reversibles bajo ninguna circunstancia.</li>\n                    <li>Tu balance actual disponible es de <b>{format_num(balance)} {token['symbol']}</b>.</li>\n                </ul>
            </div>
            """, unsafe_allow_html=True)

            # Calculadora / Conversor dinámico para usuarios
            st.markdown(f"""
            <div class="card" style="border-left: 5px solid #ffd700;">
                <h4 style="margin-top:0; color: #ffd700; display:flex; align-items:center; gap:8px;">🧮 Conversor SIAD a Pesos</h4>
                <p style="font-size:0.85rem; color:#a1a1aa; margin-top:2px; line-height:1.2rem;">
                    Calcula cuánto valen tus tokens en Pesos Colombianos antes de transferirlos:
                </p>
            </div>
            """, unsafe_allow_html=True)

            calc_sd_input = st.number_input("Cantidad de tokens SD a cotizar:", min_value=0.0, value=100.0, step=10.0, key="send_calc_sd_input")
            calc_cop_result = calc_sd_input * token_price_cop
            calc_usd_result = calc_sd_input * token_price_usd

            st.markdown(f"""
            <div class="card" style="border-left: 5px solid #10b981; background: linear-gradient(135deg, #0d0d11 0%, #061f14 100%) !important;">
                <p style="font-size:0.85rem; color:#a1a1aa; margin: 3px 0;"><b>Monto a Enviar:</b> {format_num(calc_sd_input)} SD</p>
                <p style="font-size:0.85rem; color:#ffffff; margin: 3px 0;"><b>Equivalente en Dólares:</b> ${format_num(calc_usd_result)} USD</p>
                <p style="font-size:1.15rem; color:#ffd700; font-weight:bold; margin-top:8px; margin-bottom: 0;"><b>Equivalente en Pesos:</b> ${format_num(calc_cop_result)} COP</p>
                <span style="font-size:0.75rem; color:#888899; display:block; margin-top:8px;">Tasa actual: 1 SD = ${token_price_cop:,.2f} COP</span>
            </div>
            """, unsafe_allow_html=True)

    # --- SWAP Y RETIROS ---
    elif choice == "🔄 Swap y Retiros":
        st.markdown("<h1 class='golden-title'>🔄 Cambiar SD y Solicitar Retiro (Nequi)</h1>", unsafe_allow_html=True)
        st.write("Convierte tus tokens SIAD (SD) a pesos colombianos líquidos e inicia solicitudes de retiro seguras directamente a tu cuenta Nequi.")
        
        tab_swap, tab_withdraw, tab_history_with = st.tabs([
            "🔄 Intercambio Multidivisa (Swap)", 
            "💸 Retirar COP a Nequi", 
            "📋 Historial de Retiros"
        ])
        
        with tab_swap:
            st.subheader("🔄 Centro de Intercambio (Swap)")
            st.write("Intercambia tus activos de forma simulada dentro de la base de datos de la app, o realiza intercambios reales on-chain en la blockchain usando PancakeSwap.")
            
            sub_tab_sim, sub_tab_real = st.tabs([
                "🎮 Swap Simulado (Base de Datos)",
                "🥞 Swap Real On-Chain (PancakeSwap)"
            ])
            
            with sub_tab_sim:
                st.subheader("🎮 Intercambio Multidivisa Simulado (Local)")
                st.write("Intercambia de forma instantánea entre **BNB**, **SD (SIAD)**, **USDT** y **Pesos Colombianos (COP)** con tasas y cotizaciones de mercado en tiempo real.")

                # 1. Fetch live prices
                bnb_price_usd = fetch_bnb_price()
                sd_price_usd = token_price_usd
                usdt_price_usd = 1.0
                cop_price_usd = 1.0 / usd_cop if usd_cop > 0 else 1.0 / 4150.0

                # 2. Get user balances
                user_bsc_wallet = get_user_bsc_address(st.session_state.wallet_code)
                
                # Initialize simulated BNB and USDT balances if not set
                if "sim_bnb" not in st.session_state:
                    st.session_state.sim_bnb = 1.2500
                if "sim_usdt" not in st.session_state:
                    st.session_state.sim_usdt = 150.00
                    
                is_web3_active = bool(user_bsc_wallet and user_bsc_wallet.strip().startswith("0x") and st.session_state.get("sync_blockchain", True))
                
                if is_web3_active:
                    user_bsc_wallet = user_bsc_wallet.strip()
                    sd_balance = fetch_bep20_balance_rpc(user_bsc_wallet, token['contract'])
                    bnb_balance = fetch_native_balance_rpc(user_bsc_wallet)
                    usdt_balance = fetch_bep20_balance_rpc(user_bsc_wallet, "0x55d398326f99059ff775485246999027b3197955")
                else:
                    sd_balance = balance # From SQLite DB
                    bnb_balance = st.session_state.sim_bnb
                    usdt_balance = st.session_state.sim_usdt
                    
                cop_balance = balance_cop_user # From SQLite DB

                # Display 4 cards showing balances
                st.write("<b>💳 Tus Saldos Disponibles para Swap:</b>", unsafe_allow_html=True)
                
                # Let's use 4 columns
                bal_col1, bal_col2, bal_col3, bal_col4 = st.columns(4)
                with bal_col1:
                    st.markdown(f"""
                    <div class="card" style="border-top: 3px solid #f3ba2f; min-height: 90px; padding: 0.5rem !important;">
                        <div class="metric-title" style="font-size: 0.7rem !important; color: #f3ba2f;">🪙 BNB Balance</div>
                        <div class="metric-value" style="font-size: 1.15rem !important; color: #ffffff; margin: 2px 0;">{format_num(bnb_balance)} BNB</div>
                        <div class="metric-sub" style="font-size: 0.65rem !important;">~ ${(bnb_balance * bnb_price_usd * usd_cop):,.0f} COP</div>
                    </div>
                    """, unsafe_allow_html=True)
                with bal_col2:
                    st.markdown(f"""
                    <div class="card" style="border-top: 3px solid #10b981; min-height: 90px; padding: 0.5rem !important;">
                        <div class="metric-title" style="font-size: 0.7rem !important; color: #10b981;">🪙 {token['symbol']} Balance</div>
                        <div class="metric-value" style="font-size: 1.15rem !important; color: #ffffff; margin: 2px 0;">{format_num(sd_balance)} SD</div>
                        <div class="metric-sub" style="font-size: 0.65rem !important;">~ ${(sd_balance * sd_price_usd * usd_cop):,.0f} COP</div>
                    </div>
                    """, unsafe_allow_html=True)
                with bal_col3:
                    st.markdown(f"""
                    <div class="card" style="border-top: 3px solid #26a17b; min-height: 90px; padding: 0.5rem !important;">
                        <div class="metric-title" style="font-size: 0.7rem !important; color: #26a17b;">🪙 USDT Balance</div>
                        <div class="metric-value" style="font-size: 1.15rem !important; color: #ffffff; margin: 2px 0;">{format_num(usdt_balance)} USDT</div>
                        <div class="metric-sub" style="font-size: 0.65rem !important;">~ ${(usdt_balance * usdt_price_usd * usd_cop):,.0f} COP</div>
                    </div>
                    """, unsafe_allow_html=True)
                with bal_col4:
                    st.markdown(f"""
                    <div class="card" style="border-top: 3px solid #ffd700; min-height: 90px; padding: 0.5rem !important;">
                        <div class="metric-title" style="font-size: 0.7rem !important; color: #ffd700;">💵 Peso COP Balance</div>
                        <div class="metric-value" style="font-size: 1.15rem !important; color: #ffffff; margin: 2px 0;">${format_num(cop_balance)} COP</div>
                        <div class="metric-sub" style="font-size: 0.65rem !important;">~ ${(cop_balance * cop_price_usd):,.2f} USD</div>
                    </div>
                    """, unsafe_allow_html=True)

                # Inform user if they are in web3 mode or simulated mode
                if is_web3_active:
                    st.success(f"🔗 <b>Conectado a BSC:</b> Los saldos de BNB, SD y USDT se obtienen en vivo de tu dirección <code>{user_bsc_wallet}</code>.")
                    st.warning("⚠️ **Atención sobre el Swap en Vivo:** Tu billetera MetaMask está conectada en **modo lectura**. Por motivos de seguridad del navegador, esta aplicación no puede ordenar a tu extensión MetaMask que firme transacciones reales on-chain para gastar tus criptomonedas. Por lo tanto, los intercambios (Swaps) realizados dentro de la app son **simulados a nivel de base de datos**. Al recargar la página, la app volverá a leer tu balance real de la blockchain y se restaurará a su valor original. Para realizar intercambios reales on-chain que se se ejecuten en la blockchain, por favor usa la pestaña contigua **'PancakeSwap'** que hemos integrado para ti.")
                else:
                    st.warning("⚠️ <b>Saldos Simulados (Local):</b> No has configurado tu billetera BSC en tu Perfil. Estamos usando saldos de prueba de BNB y USDT para que realices tus swaps libremente.")

                st.write("---")

                # Selection of From/To Currencies
                col_sel1, col_sel2 = st.columns(2)
                with col_sel1:
                    from_curr = st.selectbox("💱 Moneda de Origen (Pagas):", ["BNB", "SD", "USDT", "COP"], index=1, key="from_curr_select")
                with col_sel2:
                    to_options = ["BNB", "SD", "USDT", "COP"]
                    if from_curr in to_options:
                        to_options.remove(from_curr)
                    to_curr = st.selectbox("🎯 Moneda de Destino (Recibes):", to_options, index=to_options.index("COP") if "COP" in to_options else 0, key="to_curr_select")

                # Get respective balances
                bal_map = {
                    "BNB": bnb_balance,
                    "SD": sd_balance,
                    "USDT": usdt_balance,
                    "COP": cop_balance
                }
                price_map = {
                    "BNB": bnb_price_usd,
                    "SD": sd_price_usd,
                    "USDT": usdt_price_usd,
                    "COP": cop_price_usd
                }

                max_val = float(bal_map[from_curr])

                col_input1, col_preview = st.columns([2, 1])
                with col_input1:
                    if f"swap_amt_{from_curr}" not in st.session_state:
                        st.session_state[f"swap_amt_{from_curr}"] = 0.0
                    
                    # Percent buttons
                    st.write("<b>💡 Proporción rápida:</b>", unsafe_allow_html=True)
                    col_p1, col_p2, col_p3, col_p4 = st.columns(4)
                    if col_p1.button("25%", key="swap_p_25"):
                        st.session_state[f"swap_amt_{from_curr}"] = max_val * 0.25
                        st.rerun()
                    if col_p2.button("50%", key="swap_p_50"):
                        st.session_state[f"swap_amt_{from_curr}"] = max_val * 0.50
                        st.rerun()
                    if col_p3.button("75%", key="swap_p_75"):
                        st.session_state[f"swap_amt_{from_curr}"] = max_val * 0.75
                        st.rerun()
                    if col_p4.button("100%", key="swap_p_100"):
                        st.session_state[f"swap_amt_{from_curr}"] = max_val
                        st.rerun()

                    # Input fields
                    clamped_swap_amt = float(st.session_state[f"swap_amt_{from_curr}"])
                    if clamped_swap_amt > max_val:
                        clamped_swap_amt = max_val
                    if clamped_swap_amt < 0.0:
                        clamped_swap_amt = 0.0
                    swap_input_val = st.number_input(
                        f"Cantidad de {from_curr} a cambiar (Máx: {format_num(max_val)}):",
                        min_value=0.0000,
                        max_value=max_val,
                        value=clamped_swap_amt,
                        step=0.1 if max_val < 10 else 1.0,
                        format="%.4f" if from_curr != "COP" else "%.0f",
                        key="swap_input_field_new"
                    )
                    st.session_state[f"swap_amt_{from_curr}"] = swap_input_val

                # Calculations
                price_from = price_map[from_curr]
                price_to = price_map[to_curr]

                # Exchange rate
                rate = price_from / price_to
                amount_to_receive = swap_input_val * rate

                with col_preview:
                    st.markdown(f"""
                    <div class="card" style="border-left: 5px solid #10b981; min-height: 150px; display: flex; flex-direction: column; justify-content: center; padding: 0.6rem !important;">
                        <h4 style="margin-top:0; color:#10b981; font-size: 0.95rem; margin-bottom: 8px;">📊 Tipo de Cambio</h4>
                        <p style="font-size:0.82rem; color:#ffffff; margin: 2px 0;"><b>Tasa:</b> 1 {from_curr} = {format_num(rate)} {to_curr}</p>
                        <p style="font-size:0.82rem; color:#a1a1aa; margin: 2px 0;"><b>Valor Origen:</b> ${(swap_input_val * price_from):,.2f} USD</p>
                        <hr style="border-color: #ffd70033; margin: 8px 0;">
                        <p style="font-size:1.1rem; color:#ffd700; font-weight:bold; margin: 0;"><b>Recibirás:</b><br>{format_num(amount_to_receive)} {to_curr}</p>
                    </div>
                    """, unsafe_allow_html=True)

                # Swap Button
                if st.button("🚀 Confirmar Intercambio (Swap)", key="execute_multi_swap_btn"):
                    if swap_input_val <= 0:
                        st.error("⚠️ El monto a cambiar debe ser mayor que cero.")
                    elif swap_input_val > max_val:
                        st.error(f"⚠️ Saldo de {from_curr} insuficiente.")
                    else:
                        with st.spinner("⏳ Cargando... Procesando tu intercambio en tiempo real... Por favor espera..."):
                            import time
                            time.sleep(2.5) # Simular procesamiento visual para dar feedback real
                            success, msg = execute_multi_swap(
                                st.session_state.wallet_code,
                                from_curr,
                                to_curr,
                                swap_input_val,
                                amount_to_receive,
                                price_from,
                                price_to
                            )
                            if success:
                                st.session_state[f"swap_amt_{from_curr}"] = 0.0
                                st.balloons()
                                st.success(msg)
                                st.rerun()
                            else:
                                st.error(msg)
            
            with sub_tab_real:
                st.subheader("🥞 Swap Real On-Chain vía PancakeSwap")
                st.write("Conéctate directamente a la Binance Smart Chain (BSC) para comprar o vender tu token real **SD (SIAD)** utilizando tu extensión de MetaMask o Trust Wallet.")
                
                pancake_url = f"https://pancakeswap.finance/swap?outputCurrency={token['contract']}"
                
                st.markdown(f"""
                <div class="card" style="border-left: 5px solid #f3ba2f; background: linear-gradient(135deg, #0d0d11 0%, #201a00 100%) !important; padding: 15px; margin-bottom: 15px;">
                    <h4 style="color: #f3ba2f; margin-top: 0; display: flex; align-items: center; gap: 8px;">🥞 Pool de Liquidez PancakeSwap</h4>
                    <p style="font-size: 0.9rem; line-height: 1.4rem; color: #ffffff; margin-bottom: 15px;">
                        Para tu seguridad y comodidad, hemos integrado el Widget oficial de PancakeSwap. Si el navegador o tu extensión de billetera bloquea la conexión dentro de un cuadro incrustado debido a políticas de seguridad locales, puedes hacer clic en el botón de abajo para <b>abrir el pool de liquidez real en una nueva pestaña</b> con tu token pre-cargado.
                    </p>
                    <a href="{pancake_url}" target="_blank" style="text-decoration: none;">
                        <div style="background-color: #f3ba2f; color: #000000; font-weight: 800; padding: 10px 18px; border-radius: 6px; text-align: center; font-size: 0.95rem; text-transform: uppercase; letter-spacing: 0.05em; display: inline-block; cursor: pointer; border: 1.5px solid #ffd700; box-shadow: 0 4px 15px rgba(243, 186, 47, 0.25);">
                            🥞 Abrir PancakeSwap en Nueva Pestaña 🚀
                        </div>
                    </a>
                </div>
                """, unsafe_allow_html=True)
                
                # Embedded PancakeSwap Iframe
                pancake_iframe_html = f"""
                <iframe src="https://pancakeswap.finance/swap?outputCurrency={token['contract']}&theme=dark" 
                        width="100%" 
                        height="650" 
                        style="border: 0; border-radius: 12px; box-shadow: 0 5px 25px rgba(0,0,0,0.5);">
                </iframe>
                """
                st.components.v1.html(pancake_iframe_html, height=670)

        with tab_withdraw:
            st.subheader("2. Retirar Pesos Colombianos (COP) a tu Cuenta Nequi")
            st.write("Solicita la transferencia de tu saldo acumulado en pesos a tu cuenta de ahorros Nequi. Se descuenta una tasa del **2% de comisión operacional** por procesamiento de retiro.")
            
            if balance_cop_user <= 0:
                st.info("⚠️ Tu saldo retirable está en $0 COP. Primero realiza una conversión en la pestaña 'Convertir SD a Pesos' para disponer de saldo para retiro.")
            else:
                if balance_cop_user < 1000:
                    st.warning("⚠️ El monto mínimo de retiro es de **$1,000 COP**. Tu saldo retirable actual es menor a este límite.")
                else:
                    col_w1, col_w2 = st.columns([2, 1])
                    with col_w1:
                        user_nequi_saved = get_user_nequi(st.session_state.wallet_code)
                        amount_cop_to_withdraw = st.number_input("Ingresa la cantidad en Pesos (COP) a retirar (Mínimo $1,000 COP):", min_value=1000.0, max_value=float(balance_cop_user), step=5000.0, key="withdraw_amt_input_field")
                        nequi_account_w = st.text_input("Número de Cuenta Nequi (10 dígitos):", value=user_nequi_saved, max_chars=11, placeholder="Ej. 3001234567", key="withdraw_nequi_input_field")
                        
                        st.info("📱 <b>Tip para celular:</b> Toca la pantalla fuera del teclado para actualizar el descuento de la comisión en la tarjeta de la derecha de inmediato.")

                        if st.button("Solicitar Envío de Dinero", key="submit_withdrawal_direct_btn"):
                            if amount_cop_to_withdraw < 1000:
                                st.error("El retiro mínimo es de $1,000 COP.")
                            elif amount_cop_to_withdraw > balance_cop_user:
                                st.error("No posees suficiente saldo en pesos COP retirable.")
                            elif len(nequi_account_w) < 10 or not nequi_account_w.isdigit():
                                st.error("El número de cuenta de Nequi debe constar de dígitos numéricos válidos.")
                            else:
                                success, msg = submit_withdrawal_request(st.session_state.wallet_code, amount_cop_to_withdraw, nequi_account_w)
                                if success:
                                    st.balloons()
                                    st.success(msg)
                                    st.rerun()
                                else:
                                    st.error(msg)
                with col_w2:
                    fee_pct = 0.01 if is_vip_user == 1 else 0.02
                    fee_val = amount_cop_to_withdraw * fee_pct
                    net_val = amount_cop_to_withdraw - fee_val
                    st.markdown(f"""
                    <div class="card" style="border-left: 5px solid #ffd700;">
                        <h4 style="margin-top:0; color:#ffd700;">💸 Liquidación de Transferencia</h4>
                        <p style="font-size:0.85rem; color:#ffffff;"><b>Monto de Retiro:</b> ${format_num(amount_cop_to_withdraw)} COP</p>
                        <p style="font-size:0.85rem; color:#ef4444;"><b>Comisión de Retiro ({"1%" if is_vip_user == 1 else "2%"}):</b> ${format_num(fee_val)} COP</p>
                        <hr style="border-color:#3f3f46; margin: 10px 0;">
                        <p style="font-size:1.1rem; color:#10b981; font-weight:bold;"><b>A Transferir a Nequi:</b> ${format_num(net_val)} COP</p>
                        <span style="font-size:0.75rem; color:#a1a1aa; display:block; margin-top:10px;">
                            🔒 El saldo solicitado de ${format_num(amount_cop_to_withdraw)} COP se congela para retiro y se borrará definitivamente cuando el administrador te envíe la captura de confirmación del pago.
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                    
        with tab_history_with:
            st.subheader("3. Historial de Solicitudes de Retiro")
            df_w_hist = get_user_withdrawals(st.session_state.wallet_code)
            
            if len(df_w_hist) == 0:
                st.info("No hay registros de retiros solicitados todavía.")
            else:
                for idx, row in df_w_hist.iterrows():
                    status_text = "PENDIENTE" if row['status'] == 'PENDING' else ("PAGADO" if row['status'] == 'APPROVED' else "RECHAZADO")
                    status_color = "#ffd700" if row['status'] == 'PENDING' else ("#10b981" if row['status'] == 'APPROVED' else "#ef4444")
                    
                    with st.expander(f"💸 Retiro #{row['id']} - Solicitado: ${row['amount_cop']:,.0f} COP ({status_text})"):
                        col_h_info, col_h_img = st.columns([1, 1])
                        with col_h_info:
                            st.markdown(f"""
                            <div class="card" style="border-left: 3px solid {status_color};">
                                <p><b>ID de Solicitud:</b> #{row['id']}</p>
                                <p><b>Monto de Retiro COP:</b> ${row['amount_cop']:,.0f} COP</p>
                                <p><b>Comisión Operativa (2%):</b> ${row['fee_cop']:,.0f} COP</p>
                                <p><b>Monto Neto Enviado:</b> <span style="color:#10b981; font-weight:bold;">${row['net_cop']:,.0f} COP</span></p>
                                <p><b>Cuenta Nequi:</b> {row['nequi_number']}</p>
                                <p><b>Estado:</b> <span style="color:{status_color}; font-weight:bold;">{status_text}</span></p>
                                <p><b>Fecha de Solicitud:</b> {row['timestamp']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        with col_h_img:
                            if row['status'] == 'APPROVED' and row['receipt_image']:
                                st.subheader("📷 Comprobante de Pago")
                                try:
                                    st.image(row['receipt_image'], caption="Foto del soporte de transferencia Nequi oficial cargada por el admin", use_container_width=True)
                                except Exception:
                                    st.error("No se pudo cargar la imagen del comprobante.")
                            elif row['status'] == 'PENDING':
                                st.info("⏳ Solicitud recibida. El administrador está realizando el pago a tu cuenta Nequi. Una vez realizado, aparecerá tu comprobante aquí.")
                            else:
                                st.error("❌ Retiro rechazado. Los fondos regresaron a tu saldo retirable.")

    # --- COMPRAR SD (PROOF OF PAYMENT & NEQUI) ---
    elif choice == "📥 Comprar SD":
        st.markdown(f"<h1 class='golden-title'>📥 Adquirir Tokens {token['symbol']}</h1>", unsafe_allow_html=True)
        st.write("Sigue los pasos detallados a continuación para recargar saldo de forma directa y oficial.")
        
        col_calc, col_nequi = st.columns([3, 2])
        
        with col_nequi:
            st.markdown(f"""
            <div class="card" style="border-left: 5px solid #ffd700;">
                <h4 style="margin-top:0; color: #ffd700; display: flex; align-items: center; gap: 8px;">📲 Paso 1: Transfiere por NEQUI</h4>\n                <p style="font-size: 0.9rem; color: #e2e8f0; line-height: 1.4rem;">
                    Realiza tu pago desde la app Nequi al número oficial del administrador.
                    <b>Toca el número abajo para seleccionarlo y copiarlo de inmediato:</b>
                </p>
            </div>
            """, unsafe_allow_html=True)
            st.code(token['nequi_number'], language="text")
            
            st.markdown(f"""
            <div class="card" style="border-top: 2px solid #10b981;">
                <h5 style="color: #ffd700; margin-top:0;">📋 Requisitos para el Proceso</h5>\n                <ul style="padding-left: 18px; font-size: 0.85rem; color: #a1a1aa; line-height: 1.3rem;">
                    <li>Conserva una captura de pantalla clara de tu comprobante con hora e ID de transacción.</li>\n                    <li>El sistema autodetectará tu dirección de billetera (ID): <code style="color: #10b981;">{st.session_state.wallet_code}</code>.</li>\n                    <li>Una vez verificado, tu saldo se actualizará automáticamente.</li>\n                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        with col_calc:
            st.subheader("Paso 2: Cotiza tu compra")
            amount_cop_input = st.number_input("Ingresa la cantidad en Pesos Colombianos (COP) que vas a transferir:", min_value=1000, value=20000, step=5000)
            
            sd_to_receive = amount_cop_input / token_price_cop
            
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                st.markdown(f"""
                <div class="card" style="border-color: #ffd700;">
                    <div class="metric-title">Monto a pagar (COP)</div>
                    <div class="metric-value" style="color: #ffd700;">${amount_cop_input:,.0f} COP</div>
                </div>
                """, unsafe_allow_html=True)
            with col_c2:
                st.markdown(f"""
                <div class="card" style="border-color: #10b981;">
                    <div class="metric-title">Tokens a recibir ({token['symbol']})</div>
                    <div class="metric-value" style="color: #10b981;">{sd_to_receive:,.4f} SD</div>
                    <div class="metric-sub">Tasa: 1 SD = ${token_price_cop:,.2f} COP</div>
                </div>
                """, unsafe_allow_html=True)
                
            st.subheader("Paso 3: Sube tu Comprobante de Pago")
            uploaded_file = st.file_uploader("Adjunta la imagen/foto de tu transferencia Nequi:", type=["png", "jpg", "jpeg"])
            
            if st.button("Enviar Solicitud de Compra"):
                if not uploaded_file:
                    st.error("⚠️ Debes adjuntar la imagen del comprobante para que el administrador pueda procesar tu compra.")
                else:
                    try:
                        img_bytes = uploaded_file.read()
                        submit_purchase_request(st.session_state.wallet_code, amount_cop_input, sd_to_receive, img_bytes)
                        st.balloons()
                        st.success("🎉 ¡Tu comprobante ha sido enviado con éxito al administrador! Tu compra de " + f"{sd_to_receive:,.4f} SD" + " está siendo procesada.")
                    except Exception as e:
                        st.error(f"Error procesando la solicitud: {str(e)}")

    # --- PESTAÑA: NOTIFICACIONES ---
    elif "Notificaciones" in choice:
        st.markdown("<h1 class='golden-title'>🔔 Bandeja de Notificaciones</h1>", unsafe_allow_html=True)
        st.write("Mantente al tanto de la aprobación de tus transacciones, recargas de saldo y actualizaciones del sistema.")
        
        # Marcar todas como leídas al entrar
        mark_notifications_as_read(st.session_state.wallet_code)
        
        notifs_df = get_user_notifications(st.session_state.wallet_code)
        
        if len(notifs_df) == 0:
            st.info("No tienes notificaciones registradas en tu historial.")
        else:
            for idx, row in notifs_df.iterrows():
                # Formato y estilo de la tarjeta de notificación
                border_color = "#ffd700"
                if "aprobada" in row['message'] or "recibido" in row['message']:
                    border_color = "#10b981"
                elif "rechazada" in row['message']:
                    border_color = "#ef4444"
                
                # Renderizar HTML limpio para cada notificación
                st.markdown(f"""
                <div class="notification-card" style="border-left-color: {border_color} !important;">
                    <span style="font-size: 0.8rem; color: #888899; float: right;">{row['timestamp']}</span>
                    <p style="margin: 0; font-size: 0.95rem; line-height: 1.4rem; color: #ffffff;">{row['message']}</p>
                </div>
                """, unsafe_allow_html=True)

    # --- TIENDA Alianza (COMPRA DE ARTÍCULOS Y MEMBRESÍA VIP) ---
    elif choice == "🛍️ Tienda Alianza":
        st.markdown(f"<h1 class='golden-title'>🛍️ Tienda Oficial Alianza ({token['symbol']})</h1>", unsafe_allow_html=True)
        st.write("Gasta tus tokens SIAD (SD) acumulados en entretenimiento, alimentos express, recargas de datos, o diviértete con nuestros micro-juegos y sorteos de alta rotación diaria.")
    
        # Consultar si el usuario es VIP
        is_vip_val = is_vip_user == 1
    
        # Tarjeta VIP de estado del usuario
        if is_vip_val:
            st.markdown("""
            <div class="card" style="border-left: 5px solid #10b981; background: linear-gradient(135deg, #0d0d11 0%, #061f14 100%) !important;">
                <h4 style="color: #10b981; margin:0; display:flex; align-items:center; gap:8px;">👑 MIEMBRO VIP DE Alianza</h4>
                <p style="font-size:0.9rem; margin-top:5px; color:#ffffff; line-height:1.4rem;">
                    ¡Felicidades! Tienes activos tus beneficios VIP permanentes:
                    <br>• Comisión de Retiro a Nequi reducida al <b>1%</b> (en lugar de 2%).
                    <br>• Comisión de Referidos aumentada al <b>25%</b> (en lugar de 20%).
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="card" style="border-left: 5px solid #ffd700;">
                <h4 style="color: #ffd700; margin:0;">🌟 ¿Quieres maximizar tus ganancias?</h4>
                <p style="font-size:0.9rem; margin-top:5px; color:#a1a1aa; line-height:1.4rem;">
                    Adquiere la <b>Membresía VIP Alianza</b> en el catálogo de abajo para bajar tus tasas de retiro a la mitad y cobrar comisiones más altas por tus invitados.
                </p>
            </div>
            """, unsafe_allow_html=True)

        # 4 TABS DE LA TIENDA
        tab_pines, tab_recargas, tab_comida, tab_juegos = st.tabs([
            "🎁 Pines y Membresías",
            "📱 Recargas Móviles",
            "🍔 Alimentos y Bebidas",
            "🎮 Juegos y Sorteos"
        ])

        # Tab 1: Pines y Membresías
        with tab_pines:
            st.subheader("🛒 Pines de Entretenimiento y Regalos")
            st.write("Adquiere membresías oficiales y tarjetas de regalo digitales de inmediato.")
            conn = get_db_connection()
            items_pines_df = pd.read_sql_query("SELECT id, name, description, price_sd, item_type FROM store_items WHERE item_type IN ('MEMBERSHIP', 'GIFT_CARD')", conn)
            conn.close()
        
            if len(items_pines_df) == 0:
                st.info("No hay pines ni membresías configuradas.")
            else:
                col_p_cards = st.columns(3)
                for idx_p, row_p in items_pines_df.iterrows():
                    col_idx = idx_p % 3
                    with col_p_cards[col_idx]:
                        border_color = "#ffd700" if row_p['item_type'] == 'MEMBERSHIP' else "#10b981"
                        btn_label = "Adquirir Membresía" if row_p['item_type'] == 'MEMBERSHIP' else "Comprar Pin"
                        is_disabled = row_p['item_type'] == 'MEMBERSHIP' and is_vip_val
                    
                        st.markdown(f"""
                        <div class="card" style="border-color: {border_color}; min-height: 240px; display: flex; flex-direction: column; justify-content: space-between;">
                            <div>
                                <h4 style="color: {border_color}; margin-top:0;">{row_p['name']}</h4>
                                <p style="font-size:0.85rem; color:#e2e8f0; line-height: 1.3rem; min-height: 60px;">{row_p['description']}</p>
                            </div>
                            <div style="margin-top: 15px;">
                                <span style="font-size: 1.3rem; font-weight: 800; color: #ffffff;">{row_p['price_sd']:,.2f} SD</span>
                                <span style="font-size: 0.8rem; color: #a1a1aa; display:block;">Equivale aprox. a ${(row_p['price_sd'] * token_price_cop):,.0f} COP</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                        if is_disabled:
                            st.button("👑 VIP Ya Adquirido", key=f"buy_p_btn_{row_p['id']}", disabled=True)
                        else:
                            if st.button(f"{btn_label} - {row_p['price_sd']} SD", key=f"buy_p_btn_{row_p['id']}"):
                                success, msg = buy_store_item(st.session_state.wallet_code, row_p['id'])
                                if success:
                                    st.balloons()
                                    st.success(msg)
                                    st.rerun()
                                else:
                                    st.error(msg)

        # Tab 2: Recargas Móviles (Punto 1)
        with tab_recargas:
            st.subheader("📱 Paquetes de Datos y Minutos de Celular")
            st.write("Recarga paquetes de telefonía móvil de Claro, Tigo, Movistar, o Wom al instante pagando con tus tokens Alianza.")
            conn = get_db_connection()
            items_recargas_df = pd.read_sql_query("SELECT id, name, description, price_sd FROM store_items WHERE item_type = 'CARRIER_RECHARGE'", conn)
            conn.close()
        
            if len(items_recargas_df) == 0:
                st.info("No hay paquetes de recargas disponibles en este momento.")
            else:
                col_r_cards = st.columns(2)
                for idx_r, row_r in items_recargas_df.iterrows():
                    col_idx = idx_r % 2
                    with col_r_cards[col_idx]:
                        st.markdown(f"""
                        <div class="card" style="border-color: #3b82f6; min-height: 200px; display: flex; flex-direction: column; justify-content: space-between;">
                            <div>
                                <h4 style="color: #3b82f6; margin-top:0;">📱 {row_r['name']}</h4>
                                <p style="font-size:0.85rem; color:#e2e8f0; line-height: 1.3rem;">{row_r['description']}</p>
                            </div>
                            <div style="margin-top: 15px;">
                                <span style="font-size: 1.25rem; font-weight: 800; color: #ffffff;">{row_r['price_sd']:,.2f} SD</span>
                                <span style="font-size: 0.8rem; color: #a1a1aa; display:block;">Equivale aprox. a ${(row_r['price_sd'] * token_price_cop):,.0f} COP</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                        if st.button(f"Comprar Paquete - {row_r['price_sd']} SD", key=f"buy_r_btn_{row_r['id']}"):
                            success, msg = buy_store_item(st.session_state.wallet_code, row_r['id'])
                            if success:
                                st.balloons()
                                st.success(msg)
                                st.rerun()
                            else:
                                st.error(msg)

        # Tab 3: Alimentos y Bebidas (Punto 4 + Categoría Alimentos con envío)
        with tab_comida:
            st.subheader("🍔 Cafetería, Comida Rápida y Bebidas Express")
            st.write("¿Tienes hambre en la calle? Pide combos de alimentos o bebidas. **El costo del envío se suma automáticamente** y puedes modificar estos valores cuando quieras.")
            conn = get_db_connection()
            try:
                items_food_df = pd.read_sql_query("SELECT id, name, description, price_sd, delivery_fee_sd FROM store_items WHERE item_type = 'FOOD'", conn)
            except Exception:
                items_food_df = pd.read_sql_query("SELECT id, name, description, price_sd, 0.0 as delivery_fee_sd FROM store_items WHERE item_type = 'FOOD'", conn)
            conn.close()
        
            if len(items_food_df) == 0:
                st.info("No hay alimentos configurados en el catálogo actualmente.")
            else:
                col_f_cards = st.columns(2)
                for idx_f, row_f in items_food_df.iterrows():
                    col_idx = idx_f % 2
                
                    base_price = row_f['price_sd']
                    delivery_fee = row_f['delivery_fee_sd'] if row_f['delivery_fee_sd'] is not None else 0.0
                    total_food_cost = base_price + delivery_fee
                
                    with col_f_cards[col_idx]:
                        st.markdown(f"""
                        <div class="card" style="border-color: #ef4444; min-height: 240px; display: flex; flex-direction: column; justify-content: space-between;">
                            <div>
                                <h4 style="color: #ef4444; margin-top:0;">🍔 {row_f['name']}</h4>
                                <p style="font-size:0.85rem; color:#e2e8f0; line-height: 1.3rem;">{row_f['description']}</p>
                                <span style="font-size:0.8rem; color:#a1a1aa; display:block; margin-top:5px;">
                                    💵 <b>Precio base:</b> {format_num(base_price)} SD | 🚚 <b>Costo Envío:</b> {format_num(delivery_fee)} SD
                                </span>
                            </div>
                            <div style="margin-top: 15px; border-top: 1px dashed rgba(255,255,255,0.1); padding-top:10px;">
                                <span style="font-size: 1.35rem; font-weight: 900; color: #ffd700;">{format_num(total_food_cost)} SD Total</span>
                                <span style="font-size: 0.8rem; color: #a1a1aa; display:block;">Equivale aprox. a ${(total_food_cost * token_price_cop):,.0f} COP</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                        if st.button(f"Pedir Alimento (Total: {format_num(total_food_cost)} SD)", key=f"buy_f_btn_{row_f['id']}"):
                            success, msg = buy_store_item(st.session_state.wallet_code, row_f['id'])
                            if success:
                                st.balloons()
                                st.success(msg)
                                st.rerun()
                            else:
                                st.error(msg)

        # Tab 4: Juegos y Sorteos (Lucky Spin, PPT, Trivia, Pronósticos, Subastas, Raspa y Gana, Consejo Cripto)
        with tab_juegos:
            st.subheader("🎮 Centro de Micro-Juegos y Sorteos de Alta Rotación")
            st.write("Gasta tus fracciones de tokens para ganar grandes premios acumulados. ¡Toda la diversión en un solo lugar!")
            
            # Tarjeta de Saldo Local de Juego Disponible
            st.markdown(f"""
            <div style="background-color: #0d0d11; border: 1.5px solid #10b981; border-radius: 12px; padding: 12px 20px; display: flex; align-items: center; justify-content: space-between; margin-bottom: 15px; box-shadow: 0 4px 15px rgba(16, 185, 129, 0.15);">
                <div>
                    <span style="color:#10b981; font-weight:bold; font-size:1.0rem;">💳 Saldo de Juego Disponible (Base de Datos):</span>
                    <span style="color:#a1a1aa; font-size:0.8rem; display:block; margin-top:2px;">Este saldo se descuenta y se abona localmente sin pagar comisiones de gas.</span>
                </div>
                <div style="text-align:right;">
                    <span style="color:#10b981; font-weight:900; font-size:1.4rem;">{format_num(balance_db)} {token['symbol']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            

        
            # Sub-tabs para organizar los 7 juegos
            tab_sub_spin, tab_sub_ppt, tab_sub_trivia, tab_sub_bets, tab_sub_auc, tab_sub_scratch, tab_sub_tip = st.tabs([
                "🎡 Lucky Spin",
                "🥊 Piedra/Papel/Tijera",
                "🧠 Trivia Alianza",
                "⚽ Pronósticos",
                "🔨 Subastas",
                "🎟️ Raspa y Gana",
                "🔮 Consejo Cripto"
            ])
        
            # ----------------- JUEGO 1: LUCKY SPIN (RULETA) -----------------
            with tab_sub_spin:
                st.markdown("#### 🎡 La Ruleta de la Fortuna Alianza (Lucky Spin)")
            
                _, spin_cost = get_game_setting('ruleta_cost', default_num=1.0)
                prizes_str, _ = get_game_setting('ruleta_prizes', default_val='0.1,0.5,1.0,2.0,5.0,0.0')
                probs_str, _ = get_game_setting('ruleta_prob', default_val='20,30,25,15,5,5')
            
                spin_prizes = [float(p) for p in prizes_str.split(',') if p]
                spin_probs = [int(p) for p in probs_str.split(',') if p]
            
                col_spin_l, col_spin_r = st.columns([1, 1])
                with col_spin_l:
                    st.markdown(clean_html(f"""
                    <div class="card" style="border-left: 4px solid #ffd700;">
                        <h5 style="color:#ffd700; margin-top:0;">⚡ Multiplica tus Monedas</h5>
                        <p style="font-size:0.9rem; color:#ffffff;">Girar la ruleta tiene un costo de <b>{format_num(spin_cost)} SD</b>. Los premios configurados por el administrador hoy son:</p>
                        <ul style="font-size:0.85rem; color:#a1a1aa; padding-left:20px;">
                            <li>🚀 Gran Premio: <b>{format_num(max(spin_prizes))} SD</b></li>
                            <li>💎 Otros Premios: {', '.join([f"{format_num(p)} SD" for p in sorted(list(set(spin_prizes))) if p > 0])}</li>
                            <li>💀 Casilla perder: 0 SD</li>
                        </ul>
                    </div>
                    """), unsafe_allow_html=True)
                with col_spin_r:
                    if st.button("🎡 Girar Ruleta Ahora", key="play_spin_btn"):
                        # Verificar saldo
                        if balance_db < spin_cost:
                            st.error(f"⚠️ Saldo insuficiente para girar la ruleta. Cuesta {format_num(spin_cost)} SD.")
                        else:
                            with st.spinner("⏳ ¡Girando la ruleta con física 3D en la blockchain...!"):
                                import time
                                time.sleep(2.0) # Simulación de animación
                            
                                # Realizar tiro probabilístico
                                import random
                                choices = list(range(len(spin_prizes)))
                                chosen_idx = random.choices(choices, weights=spin_probs, k=1)[0]
                                won_prize = spin_prizes[chosen_idx]
                            
                                conn_g = get_db_connection()
                                cursor_g = conn_g.cursor()
                                try:
                                    # Cobrar tarifa: del usuario al admin (99999)
                                    cursor_g.execute("UPDATE users SET balance = balance - ? WHERE wallet_code = ?", (spin_cost, st.session_state.wallet_code))
                                    cursor_g.execute("UPDATE users SET balance = balance + ? WHERE wallet_code = '99999'", (spin_cost,))
                                    # Registrar transacción
                                    cursor_g.execute("""
                                        INSERT INTO transactions (sender_code, receiver_code, amount)
                                        VALUES (?, '99999_LUCKY_SPIN_FEE', ?)
                                    """, (st.session_state.wallet_code, spin_cost))
                                    
                                    if won_prize > 0:
                                        # Pagar premio: del admin (99999) al usuario
                                        cursor_g.execute("UPDATE users SET balance = balance - ? WHERE wallet_code = '99999'", (won_prize,))
                                        cursor_g.execute("UPDATE users SET balance = balance + ? WHERE wallet_code = ?", (won_prize, st.session_state.wallet_code))
                                        cursor_g.execute("""
                                            INSERT INTO transactions (sender_code, receiver_code, amount)
                                            VALUES ('99999_LUCKY_SPIN_REWARD', ?, ?)
                                        """, (st.session_state.wallet_code, won_prize))
                                    
                                    conn_g.commit()
                                    conn_g.close()
                                
                                    if won_prize > spin_cost:
                                        st.balloons()
                                        st.success(f"🎉 ¡SÚPER GANANCIA! La ruleta se detuvo en: ¡{format_num(won_prize)} SD! Te has acreditado el premio.")
                                    elif won_prize > 0:
                                        st.success(f"👍 ¡Felicidades! Ganaste {format_num(won_prize)} SD en la ruleta.")
                                    else:
                                        st.warning("😢 Esta vez no tuviste suerte y cayó en 0 SD. ¡Intenta de nuevo, la suerte cambia en un segundo!")
                                    
                                    # Letrero visible por exactamente 4 segundos
                                    time.sleep(4.0)
                                    st.rerun()
                                except Exception as e:
                                    conn_g.rollback()
                                    conn_g.close()
                                    st.error(f"Error al procesar el tiro: {str(e)}")

            # ----------------- JUEGO 2: PIEDRA, PAPEL O TIJERA contra BOT -----------------
            with tab_sub_ppt:
                st.markdown("#### 🥊 Duelo Rápido: Piedra, Papel o Tijera")
                _, ppt_mult = get_game_setting('ppt_multiplier', default_num=1.90)
            
                st.write(f"Desafía al Bot Alianza. Si ganas el duelo, te llevas tu apuesta multiplicada por **{format_num(ppt_mult)}x**. Si hay empate, se te devuelve tu apuesta.")
            
                col_ppt_l, col_ppt_r = st.columns([1, 1])
                with col_ppt_l:
                    chosen_move = st.radio("🥊 Selecciona tu movimiento de ataque:", ["🪨 Piedra", "📄 Papel", "✂️ Tijera"], horizontal=True, key="user_ppt_move_field")
                    default_bet_val = min(1.0, max(0.1, float(balance_db)))
                    bet_amount = st.number_input("💵 Cantidad de Tokens SD a apostar en el duelo:", min_value=0.1, max_value=max(float(balance_db), 0.1), value=default_bet_val, format="%.2f", key="user_ppt_bet_field")
                with col_ppt_r:
                    if st.button("🥊 Confirmar e Iniciar Duelo", key="play_ppt_btn"):
                        if balance_db < bet_amount:
                            st.error("⚠️ Saldo insuficiente para realizar esta apuesta.")
                        else:
                            with st.spinner("🥊 ¡Lanzando jugadas al aire... El bot está calculando su defensa!"):
                                import time
                                time.sleep(1.5)
                            
                                bot_choices = ["🪨 Piedra", "📄 Papel", "✂️ Tijera"]
                                import random
                                bot_move = random.choice(bot_choices)
                            
                                # Lógica del ganador
                                result = "" # 'WIN', 'LOSE', 'DRAW'
                                if chosen_move == bot_move:
                                    result = "DRAW"
                                elif (chosen_move == "🪨 Piedra" and bot_move == "✂️ Tijera") or                                  (chosen_move == "📄 Papel" and bot_move == "🪨 Piedra") or                                  (chosen_move == "✂️ Tijera" and bot_move == "📄 Papel"):
                                    result = "WIN"
                                else:
                                    result = "LOSE"
                                
                                conn_p = get_db_connection()
                                cursor_p = conn_p.cursor()
                                try:
                                    # 1. Cobrar la apuesta inicial: de usuario al admin (99999)
                                    cursor_p.execute("UPDATE users SET balance = balance - ? WHERE wallet_code = ?", (bet_amount, st.session_state.wallet_code))
                                    cursor_p.execute("UPDATE users SET balance = balance + ? WHERE wallet_code = '99999'", (bet_amount,))
                                    cursor_p.execute("""
                                        INSERT INTO transactions (sender_code, receiver_code, amount)
                                        VALUES (?, '99999_PPT_BET', ?)
                                    """, (st.session_state.wallet_code, bet_amount))

                                    if result == "WIN":
                                        won_amt = bet_amount * ppt_mult
                                        # Pagar recompensa completa: del admin (99999) al usuario
                                        cursor_p.execute("UPDATE users SET balance = balance - ? WHERE wallet_code = '99999'", (won_amt,))
                                        cursor_p.execute("UPDATE users SET balance = balance + ? WHERE wallet_code = ?", (won_amt, st.session_state.wallet_code))
                                        
                                        cursor_p.execute("""
                                            INSERT INTO transactions (sender_code, receiver_code, amount)
                                            VALUES ('99999_PPT_REWARD', ?, ?)
                                        """, (st.session_state.wallet_code, won_amt))
                                    
                                        st.balloons()
                                        st.success(f"🏆 <b>¡GANASTE EL DUELO!</b> Tu oponente lanzó <b>{bot_move}</b>. Has vencido con <b>{chosen_move}</b> y te has ganado <b>{format_num(won_amt)} SD</b>.")
                                    elif result == "DRAW":
                                        # Devolver la apuesta completa: de admin (99999) al usuario
                                        cursor_p.execute("UPDATE users SET balance = balance - ? WHERE wallet_code = '99999'", (bet_amount,))
                                        cursor_p.execute("UPDATE users SET balance = balance + ? WHERE wallet_code = ?", (bet_amount, st.session_state.wallet_code))
                                        
                                        cursor_p.execute("""
                                            INSERT INTO transactions (sender_code, receiver_code, amount)
                                            VALUES ('99999_PPT_DRAW_REFUND', ?, ?)
                                        """, (st.session_state.wallet_code, bet_amount))
                                        
                                        st.info(f"🤝 <b>¡HUBO UN EMPATE!</b> Tu oponente también lanzó <b>{bot_move}</b>. Se te reembolsan tus <b>{format_num(bet_amount)} SD</b> intactos.")
                                    else: # LOSE
                                        cursor_p.execute("""
                                            INSERT INTO transactions (sender_code, receiver_code, amount)
                                            VALUES (?, '99999_PPT_LOSE', ?)
                                        """, (st.session_state.wallet_code, bet_amount))
                                    
                                        st.error(f"💀 <b>¡HAS SIDO DERROTADO!</b> Tu oponente lanzó <b>{bot_move}</b> y venció a tu <b>{chosen_move}</b>. Perdiste <b>{format_num(bet_amount)} SD</b>.")
                                    
                                    conn_p.commit()
                                    conn_p.close()
                                    # Esperar exactamente 4 segundos para mostrar letrero de resultado
                                    time.sleep(4.0)
                                    st.rerun()
                                except Exception as e:
                                    conn_p.rollback()
                                    conn_p.close()
                                    st.error(f"Error procesando duelo: {str(e)}")

            # ----------------- JUEGO 3: TRIVIA ALIANZA (Punto 5) -----------------
            with tab_sub_trivia:
                st.markdown("#### 🧠 El Desafío de Trivia Alianza")
                trivia = get_active_trivia()
            
                if not trivia:
                    st.info("No hay trivias activas publicadas por el administrador en este momento. Vuelve más tarde.")
                else:
                    st.markdown(clean_html(f"""
                    <div class="card" style="border-left: 4px solid #3b82f6;">
                        <h4 style="color:#3b82f6; margin-top:0;">📝 Trivia ID #{trivia['id']}</h4>
                        <p style="font-size:1.1rem; color:#ffffff; font-weight:bold; margin-bottom:15px;">{trivia['question']}</p>
                        <p style="font-size:0.85rem; color:#a1a1aa; margin:0;">
                            🎟️ <b>Costo de Entrada:</b> {format_num(trivia['entry_fee'])} SD | 🎁 <b>Premio de Acierto:</b> {format_num(trivia['prize_sd'])} SD
                        </p>
                    </div>
                    """), unsafe_allow_html=True)
                
                    if has_user_answered_trivia(st.session_state.wallet_code, trivia['id']):
                        st.warning("⚠️ <b>Participación Completada:</b> Ya has respondido a esta pregunta de trivia. Espera a que el administrador publique una nueva pregunta.")
                    else:
                        ans_options = {
                            f"A) {trivia['option_a']}": "A",
                            f"B) {trivia['option_b']}": "B",
                            f"C) {trivia['option_c']}": "C"
                        }
                        user_ans_label = st.radio("🧠 Selecciona tu respuesta correcta:", list(ans_options.keys()), key=f"trivia_ans_radio_{trivia['id']}")
                        user_ans_letter = ans_options[user_ans_label]
                    
                        if st.button("🧠 Registrar Mi Respuesta", key=f"submit_trivia_btn_{trivia['id']}"):
                            success_t, msg_t = play_trivia(st.session_state.wallet_code, trivia['id'], user_ans_letter)
                            if success_t:
                                if "incorrecta" in msg_t or "😢" in msg_t:
                                    st.error(msg_t)
                                else:
                                    st.balloons()
                                    st.success(msg_t)
                                # Letrero visible por exactamente 4 segundos
                                import time
                                time.sleep(4.0)
                                st.rerun()
                            else:
                                st.error(msg_t)

            # ----------------- JUEGO 4: PRONÓSTICOS DEPORTIVOS -----------------
            with tab_sub_bets:
                st.markdown("#### ⚽ Pronósticos Deportivos Alianza (La Polla)")
                active_bets = get_active_sports_bets()
            
                if not active_bets:
                    st.info("No hay partidos activos para pronósticos en este momento. ¡Pronto el administrador publicará un gran partido!")
                else:
                    st.write("<b>🏟️ Elige un partido activo para ver en vivo o realizar tu pronóstico:</b>", unsafe_allow_html=True)
                    match_options = {f"⚽ {b['local_team']} vs {b['visitor_team']} (Premio: {format_num(b['prize_sd'])} SD)": b for b in active_bets}
                    selected_match_disp = st.selectbox("Selecciona el partido:", list(match_options.keys()), key="user_active_match_selectbox")
                    bet = match_options[selected_match_disp]
                    
                    st.markdown(clean_html(f"""
                    <div class="card" style="border-left: 4px solid #ef4444; background: linear-gradient(135deg, #0d0d11 0%, #200404 100%) !important; padding: 20px;">
                        <h4 style="color:#ef4444; margin-top:0; text-align:center; font-weight:800; text-transform:uppercase; letter-spacing:0.05em;">⚽ PRONÓSTICOS DEPORTIVOS (LA POLLA ALIANZA)</h4>
                        
                        <!-- Panel de Marcador Estilo Marcador de TV -->
                        <div style="display:flex; align-items:center; justify-content:space-between; margin: 20px 0; background-color:#08080c; border:1px solid #ffffff15; border-radius:12px; padding:15px 25px; box-shadow:inset 0 0 15px rgba(0,0,0,0.6); flex-wrap:wrap; gap:10px;">
                            <div style="text-align:center; flex:1; min-width:120px;">
                                <div style="font-size:1.4rem; font-weight:900; color:#ffffff;">{bet['local_team'] if bet['local_team'] else bet['match_name'].split(' vs ')[0] if ' vs ' in bet['match_name'] else bet['match_name']}</div>
                                <div style="font-size:0.75rem; color:#888899; margin-top:3px; font-weight:bold; letter-spacing:0.05em;">LOCAL</div>
                            </div>
                            <div style="text-align:center; padding: 0 20px; border-left:1px solid #ffffff15; border-right:1px solid #ffffff15; min-width:120px; margin:0 auto;">
                                <div style="font-size:2.2rem; font-weight:950; color:#ffd700; letter-spacing:0.1em; text-shadow:0 0 10px rgba(255,215,0,0.3);">{bet['current_score']}</div>
                                <div style="font-size:0.85rem; font-weight:bold; color:#10b981; text-transform:uppercase; margin-top:5px; background-color:#10b98115; padding:2px 8px; border-radius:15px; display:inline-block;">⏱️ {bet['match_status']}</div>
                            </div>
                            <div style="text-align:center; flex:1; min-width:120px;">
                                <div style="font-size:1.4rem; font-weight:900; color:#ffffff;">{bet['visitor_team'] if bet['visitor_team'] else bet['match_name'].split(' vs ')[1] if ' vs ' in bet['match_name'] else 'Visitante'}</div>
                                <div style="font-size:0.75rem; color:#888899; margin-top:3px; font-weight:bold; letter-spacing:0.05em;">VISITANTE</div>
                            </div>
                        </div>
                        
                        <!-- Detalles de Tiempos y Fechas -->
                        <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; font-size:0.85rem; color:#a1a1aa; margin-bottom:15px; border-top:1px solid #ffffff15; padding-top:15px;">
                            <div>⏰ <b>Hora de Inicio:</b> <span style="color:#ffffff;">{bet['match_time']}</span></div>
                            <div style="text-align:right;">🏁 <b>Finalización Estimada:</b> <span style="color:#ffffff;">{bet['ends_at']}</span></div>
                        </div>
                        
                        <p style="font-size:0.85rem; color:#a1a1aa; margin:0; text-align:center; border-top:1px solid #ffffff15; padding-top:12px;">
                            🎟️ <b>Costo del Ticket:</b> {format_num(bet['ticket_cost'])} SD | 🏆 <b>Premio de Acierto:</b> {format_num(bet['prize_sd'])} SD
                        </p>
                    </div>
                    """), unsafe_allow_html=True)
                
                    user_pred_saved = get_user_prediction(st.session_state.wallet_code, bet['id'])
                    if user_pred_saved:
                        st.success(f"🎫 **Ticket Adquirido:** Ya registraste tu pronóstico de este partido: <b>{user_pred_saved}</b>. Una vez finalizado el partido en la vida real, el administrador elegirá el resultado ganador y recibirás tu premio si acertaste.")
                    else:
                        st.write("<b>🗳️ Selecciona una opción para apostar y comprar tu ticket directamente:</b>", unsafe_allow_html=True)
                        col_p1, col_p2, col_p3 = st.columns(3)
                        with col_p1:
                            if st.button("🏠 Gana Local", key=f"bet_local_{bet['id']}", use_container_width=True):
                                success_b, msg_b = buy_sports_prediction(st.session_state.wallet_code, bet['id'], "LOCAL")
                                if success_b:
                                    st.balloons()
                                    st.success(msg_b)
                                    import time
                                    time.sleep(4.0)
                                    st.rerun()
                                else:
                                    st.error(msg_b)
                        with col_p2:
                            if st.button("🤝 Empate", key=f"bet_draw_{bet['id']}", use_container_width=True):
                                success_b, msg_b = buy_sports_prediction(st.session_state.wallet_code, bet['id'], "EMPATE")
                                if success_b:
                                    st.balloons()
                                    st.success(msg_b)
                                    import time
                                    time.sleep(4.0)
                                    st.rerun()
                                else:
                                    st.error(msg_b)
                        with col_p3:
                            if st.button("🚀 Gana Visitante", key=f"bet_visitor_{bet['id']}", use_container_width=True):
                                success_b, msg_b = buy_sports_prediction(st.session_state.wallet_code, bet['id'], "VISITANTE")
                                if success_b:
                                    st.balloons()
                                    st.success(msg_b)
                                    import time
                                    time.sleep(4.0)
                                    st.rerun()
                                else:
                                    st.error(msg_b)

            # ----------------- JUEGO 5: SUBASTA DE CENTAVOS -----------------
            with tab_sub_auc:
                st.markdown("#### 🔨 Subasta de Centavos Express (Penny Auctions)")
                auc = get_active_auction()
            
                if not auc:
                    st.info("No hay subastas de productos activas en este momento.")
                else:
                    ends_time = datetime.strptime(auc["ends_at"], "%Y-%m-%d %H:%M:%S")
                    now_time = datetime.utcnow()
                    seconds_rem = max(int((ends_time - now_time).total_seconds()), 0)
                
                    # Formatear el mejor postor
                    highest_bidder_disp = auc["highest_bidder"]
                    if highest_bidder_disp == "99999":
                        highest_bidder_disp = "Propietario (Admin)"
                    elif highest_bidder_disp == st.session_state.wallet_code:
                        highest_bidder_disp = "👑 ¡Tú eres el mejor postor!"
                    else:
                        highest_bidder_disp = f"Usuario {highest_bidder_disp}"
                
                    st.markdown(clean_html(f"""
                    <div class="card" style="border-left: 4px solid #ffd700;">
                        <h4 style="color:#ffd700; margin-top:0;">🔨 Subasta Activa: {auc['item_name']}</h4>
                        <p style="font-size:0.88rem; color:#e2e8f0; margin-top:2px;">{auc['description']}</p>
                        <hr style="border-color:#ffd7001a; margin: 10px 0;">
                        <p style="font-size:1.2rem; color:#10b981; font-weight:bold; margin:3px 0;"><b>Precio actual de compra:</b> {format_num(auc['current_price'])} SD</p>
                        <p style="font-size:0.9rem; color:#ffffff; margin:3px 0;"><b>Líder de la Subasta:</b> {highest_bidder_disp}</p>
                        <p style="font-size:0.85rem; color:#a1a1aa; margin:3px 0;"><b>Costo por Puja:</b> {format_num(auc['bid_fee_sd'])} SD | <b>Aumento del precio:</b> +{format_num(auc['bid_increment'])} SD</p>
                    </div>
                    """), unsafe_allow_html=True)
                
                    if seconds_rem <= 0:
                        st.warning("⏱️ **Subasta Cerrada:** Se ha agotado el tiempo de puja de este artículo.")
                        if auc["highest_bidder"] == st.session_state.wallet_code:
                            st.success("🎉 ¡Ganaste la subasta! Puedes reclamar el PIN de tu premio de inmediato presionando el botón de abajo.")
                            if st.button("🎁 Reclamar Premio Ganado", key=f"claim_auc_btn_{auc['id']}"):
                                conn_c = get_db_connection()
                                cursor_c = conn_c.cursor()
                                try:
                                    # Marcar como reclamado
                                    cursor_c.execute("UPDATE penny_auctions SET status = 'CLAIMED' WHERE id = ?", (auc["id"],))
                                    conn_c.commit()
                                    conn_c.close()
                                
                                    # Entregar de forma ficticia
                                    add_notification(st.session_state.wallet_code, f"🎁 <b>¡Premio de Subasta Entregado!</b> Has reclamado con éxito tu artículo: <b>{auc['item_name']}</b>. El administrador te enviará tu código PIN a tus notificaciones pronto.")
                                    st.balloons()
                                    st.success("¡Premio reclamado! Revisa tu buzón de notificaciones en los próximos minutos.")
                                    st.rerun()
                                except Exception as e:
                                    conn_c.rollback()
                                    conn_c.close()
                                    st.error(str(e))
                        else:
                            st.info(f"El ganador definitivo de este artículo es el usuario <b>{auc['highest_bidder']}</b>.")
                    else:
                        # Mostrar cronómetro
                        hours_r, remainder_r = divmod(seconds_rem, 3600)
                        mins_r, secs_r = divmod(remainder_r, 60)
                        time_str = f"⏳ <b>Tiempo Restante:</b> {hours_r:02d}h {mins_r:02d}m {secs_r:02d}s"
                        st.markdown(f"<div style='font-size:1.15rem; color:#ff4d4d; font-weight:bold; margin-bottom:12px;'>{time_str}</div>", unsafe_allow_html=True)
                    
                        if st.button(f"🔨 Pujar (+{format_num(auc['bid_increment'])} SD)", key=f"place_bid_btn_{auc['id']}"):
                            success_p_b, msg_p_b = place_penny_bid(st.session_state.wallet_code, auc["id"])
                            if success_p_b:
                                st.success(msg_p_b)
                                import time
                                time.sleep(4.0)
                                st.rerun()
                            else:
                                st.error(msg_p_b)
                    
                    # Mostrar tabla de participantes y pujas recientes
                    st.markdown("---")
                    st.write("<b>📋 Participantes y Ofertas Recientes en esta Subasta:</b>", unsafe_allow_html=True)
                    try:
                        conn_bids = get_db_connection()
                        bids_df = pd.read_sql_query("""
                            SELECT t.timestamp as 'Fecha/Hora', u.fullname as 'Participante', u.wallet_code as 'ID Billetera', t.amount as 'Puja (SD)'
                            FROM transactions t
                            LEFT JOIN users u ON t.sender_code = u.wallet_code
                            WHERE t.receiver_code = '99999_AUCTION_BID_FEE' OR t.receiver_code = 'SYSTEM_AUCTION_BID_FEE'
                            ORDER BY t.timestamp DESC LIMIT 15
                        """, conn_bids)
                        conn_bids.close()
                        
                        if len(bids_df) == 0:
                            st.info("No hay pujas registradas todavía. ¡Sé el primero en pujar por este artículo!")
                        else:
                            st.dataframe(bids_df, use_container_width=True)
                    except Exception as e_bids:
                        st.write("Cargando tabla de pujas...")

            # ----------------- JUEGO 6: RASPA Y GANA DIGITAL (Scratch Cards) -----------------
            with tab_sub_scratch:
                st.markdown("#### 🎟️ Tarjeta Raspa y Gana Digital (Scratch Cards)")
                _, scratch_cost = get_game_setting('scratch_cost', default_num=0.5)
                s_prizes_str, _ = get_game_setting('scratch_prizes', default_val='0.0,0.2,0.5,1.0,3.0,10.0')
                s_probs_str, _ = get_game_setting('scratch_prob', default_val='50,25,15,7,2,1')
            
                s_prizes = [float(p) for p in s_prizes_str.split(',') if p]
                s_probs = [int(p) for p in s_probs_str.split(',') if p]
            
                st.write(f"Adquiere una tarjeta virtual raspa y gana por solo **{format_num(scratch_cost)} SD**. Revela 3 casillas iguales para ganar hasta **{format_num(max(s_prizes))} SD**.")
            
                if "scratch_game_res" not in st.session_state:
                    st.session_state.scratch_game_res = None

                col_sc_l, col_sc_r = st.columns([1, 1])
                with col_sc_l:
                    if st.session_state.scratch_game_res:
                        res_data = st.session_state.scratch_game_res
                        border_clr = "#10b981" if res_data["won_amt"] > 0 else "#ef4444"
                        st.markdown(clean_html(f"""
                        <div class="card" style="border: 2px solid {border_clr}; text-align:center; background: linear-gradient(135deg, #0d0d11 0%, #15151e 100%) !important;">
                            <div style="font-size: 1.5rem; color:#ffd700; font-weight:800;">ALIANZA SCRATCH</div>
                            <p style="font-size:0.82rem; color:#a1a1aa; margin:5px 0;">¡Tarjeta raspada!</p>
                            <div style="background-color:#050507; border: 2px solid {border_clr}; padding:15px; margin-top:10px; font-size:2.2rem; letter-spacing:0.15em; font-weight:bold; border-radius:6px; color:#ffffff;">{res_data["emojis"]}</div>
                        </div>
                        """), unsafe_allow_html=True)
                    else:
                        st.markdown(clean_html(f"""
                        <div class="card" style="border-top: 3px solid #10b981; text-align:center;">
                            <div style="font-size: 1.5rem; color:#10b981; font-weight:800;">ALIANZA SCRATCH</div>
                            <p style="font-size:0.82rem; color:#a1a1aa; margin:5px 0;">¿Tendrás las tres coronas ganadoras de la suerte?</p>
                            <div style="background-color:#0d0d11; border: 2px dashed #ffd70044; padding:15px; margin-top:10px; font-size:2.0rem; letter-spacing:0.3em; font-weight:bold; border-radius:6px; color:#5f5f6e;">❓ ❓ ❓</div>
                        </div>
                        """), unsafe_allow_html=True)
                with col_sc_r:
                    if st.button("🎟️ Comprar y Raspar Tarjeta", key="play_scratch_btn"):
                        if balance_db < scratch_cost:
                            st.error(f"⚠️ Saldo insuficiente para comprar la tarjeta. Cuesta {format_num(scratch_cost)} SD.")
                        else:
                            with st.spinner("⏳ Comprando tarjeta y revelando casillas protectoras..."):
                                import time
                                time.sleep(2.0)
                            
                                import random
                                s_choices = list(range(len(s_prizes)))
                                s_chosen_idx = random.choices(s_choices, weights=s_probs, k=1)[0]
                                won_amt_s = s_prizes[s_chosen_idx]
                            
                                # Generar combinación visual de emojis
                                winning_emojis = ["👑", "⭐", "💎", "🍎", "🔥", "🍀"]
                                if won_amt_s > 0:
                                    matching_emoji = random.choice(winning_emojis)
                                    display_emojis = f"{matching_emoji} {matching_emoji} {matching_emoji}"
                                else:
                                    shuffled = list(winning_emojis)
                                    random.shuffle(shuffled)
                                    display_emojis = f"{shuffled[0]} {shuffled[1]} {shuffled[2]}"
                                
                                conn_sc = get_db_connection()
                                cursor_sc = conn_sc.cursor()
                                try:
                                    # Cobrar el raspadito: de usuario a admin (99999)
                                    cursor_sc.execute("UPDATE users SET balance = balance - ? WHERE wallet_code = ?", (scratch_cost, st.session_state.wallet_code))
                                    cursor_sc.execute("UPDATE users SET balance = balance + ? WHERE wallet_code = '99999'", (scratch_cost,))
                                    
                                    cursor_sc.execute("""
                                        INSERT INTO transactions (sender_code, receiver_code, amount)
                                        VALUES (?, '99999_SCRATCH_FEE', ?)
                                    """, (st.session_state.wallet_code, scratch_cost))
                                
                                    if won_amt_s > 0:
                                        # Pagar premio: del admin (99999) al usuario
                                        cursor_sc.execute("UPDATE users SET balance = balance - ? WHERE wallet_code = '99999'", (won_amt_s,))
                                        cursor_sc.execute("UPDATE users SET balance = balance + ? WHERE wallet_code = ?", (won_amt_s, st.session_state.wallet_code))
                                        
                                        cursor_sc.execute("""
                                            INSERT INTO transactions (sender_code, receiver_code, amount)
                                            VALUES ('99999_SCRATCH_REWARD', ?, ?)
                                        """, (st.session_state.wallet_code, won_amt_s))
                                    
                                    conn_sc.commit()
                                    conn_sc.close()
                                
                                    st.session_state.scratch_game_res = {
                                        "emojis": display_emojis,
                                        "won_amt": won_amt_s
                                    }
                                    
                                    if won_amt_s > scratch_cost:
                                        st.balloons()
                                        st.success(f"🎉 ¡Felicidades! Tres figuras idénticas coinciden. Has ganado un premio de <b>{format_num(won_amt_s)} SD</b>.")
                                    elif won_amt_s > 0:
                                        st.success(f"👍 ¡Buen intento! Obtuviste un premio menor de consolación de <b>{format_num(won_amt_s)} SD</b>.")
                                    else:
                                        st.warning("😢 No coincidieron las figuras. ¡Compra otra tarjeta y cambia tu suerte en el próximo raspadito!")
                                    
                                    # Esperar exactamente 4 segundos para que se vea el letrero
                                    time.sleep(4.0)
                                    st.rerun()
                                except Exception as e:
                                    conn_sc.rollback()
                                    conn_sc.close()
                                    st.error(f"Error procesando raspa y gana: {str(e)}")

            # ----------------- JUEGO 7: ALERTA DIARIA O CONSEJO CRIPTO -----------------
            with tab_sub_tip:
                st.markdown("#### 🔮 Alerta Diaria o Consejo Millonario Cripto")
                _, tip_cost = get_game_setting('crypto_tip_cost', default_num=0.2)
                tip_text, _ = get_game_setting('crypto_tip', default_val='🔑 Consejo del día no configurado todavía.')
            
                # Verificar si el usuario ya lo desbloqueó hoy
                conn_u = get_db_connection()
                cursor_u = conn_u.cursor()
                cursor_u.execute("SELECT id FROM user_unlocked_tips WHERE user_code = ? AND DATE(unlocked_at) = DATE('now')", (st.session_state.wallet_code,))
                is_unlocked = bool(cursor_u.fetchone())
                conn_u.close()
            
                if is_unlocked:
                    st.markdown(clean_html(f"""
                    <div class="card" style="border: 2px solid #ffd700; background: linear-gradient(135deg, #0d0d11 0%, #201a00 100%) !important; padding: 22px; text-align:center;">
                        <h3 style="color:#ffd700; margin-top:0; font-family:serif;">🔮 CONSEJO MILLONARIO DESBLOQUEADO</h3>
                        <p style="font-size:1.15rem; color:#ffffff; font-style:italic; line-height:1.6rem; font-family:serif; max-width:80%; margin: 15px auto;">
                            "{tip_text}"
                        </p>
                        <span style="font-size:0.75rem; color:#10b981; font-weight:bold; letter-spacing:0.1em;">🔓 ACCESO COMPLETO DIARIO</span>
                    </div>
                    """), unsafe_allow_html=True)
                else:
                    st.markdown(clean_html(f"""
                    <div class="card" style="border: 1px dashed rgba(255,215,0,0.3); padding: 30px; text-align:center; background-color:#050507; filter: blur(0.3px);">
                        <div style="font-size: 3.0rem; margin-bottom:12px; filter: grayscale(1);">🔒🔮🔒</div>
                        <h4 style="color:#a1a1aa; margin-top:0;">Consejo Millonario Oculto</h4>
                        <p style="font-size:0.9rem; color:#888899; max-width:60%; margin: 10px auto; line-height:1.3rem;">
                            El administrador ha publicado un consejo financiero exclusivo para hoy. Desbloquéalo para acelerar tus ganancias de Alianza.
                        </p>
                        <span style="font-size:1.1rem; color:#ffd700; font-weight:800; display:block; margin: 15px 0;">Costo de Desbloqueo: {format_num(tip_cost)} SD</span>
                    </div>
                    """), unsafe_allow_html=True)
                
                    if st.button(f"🔓 Desbloquear Consejo con {format_num(tip_cost)} SD", key="unlock_tip_btn"):
                        if balance_db < tip_cost:
                            st.error(f"⚠️ Saldo insuficiente para desbloquear el consejo. Cuesta {format_num(tip_cost)} SD.")
                        else:
                            conn_un = get_db_connection()
                            cursor_un = conn_un.cursor()
                            try:
                                # Cobrar coste
                                cursor_un.execute("UPDATE users SET balance = balance - ? WHERE wallet_code = ?", (tip_cost, st.session_state.wallet_code))
                                cursor_un.execute("UPDATE users SET balance = balance + ? WHERE wallet_code = '99999'", (tip_cost,))
                            
                                cursor_un.execute("""
                                    INSERT INTO transactions (sender_code, receiver_code, amount)
                                    VALUES (?, 'SYSTEM_TIP_UNLOCK', ?)
                                """, (st.session_state.wallet_code, tip_cost))
                            
                                # Registrar desbloqueo
                                cursor_un.execute("INSERT INTO user_unlocked_tips (user_code, tip_id) VALUES (?, 'daily_tip')", (st.session_state.wallet_code,))
                            
                                conn_un.commit()
                                conn_un.close()
                            
                                st.balloons()
                                st.success("¡Consejo desbloqueado con éxito!")
                                st.rerun()
                            except Exception as e:
                                conn_un.rollback()
                                conn_un.close()
                                st.error(str(e))

    # --- SECCIÓN: COURIER Y CONDUCTORES (MENSAJERÍA Alianza) ---
    elif choice == "🚚 Mensajería Alianza":
        st.markdown("<h1 class='golden-title'>🚚 Servicios de Mensajería y Móviles</h1>", unsafe_allow_html=True)
        st.write("Gestiona los pagos de envíos de encomiendas de forma directa y cancela tus cuotas semanales de móviles con descuentos especiales en tokens SD.")
        
        tab_pay_ship, tab_pay_fee, tab_ship_history = st.tabs([
            "📦 Pagar Servicio de Envío",
            "💳 Pagar Cuota Semanal (Móviles)",
            "📋 Mi Historial de Mensajería"
        ])
        
        with tab_pay_ship:
            st.subheader("Pagar Envío Directamente al Conductor")
            st.write("Ingresa el código único del móvil para transferirle de forma segura el valor del envío en tokens SIAD (SD).")
            
            col_ship_f, col_ship_info = st.columns([2, 1])
            with col_ship_f:
                driver_code_input = st.text_input("Código de Billetera del Conductor / Móvil (5 dígitos):", max_chars=5, placeholder="Ej. 12345", key="msg_driver_input_field")
                
                if "msg_amt_input" not in st.session_state:
                    st.session_state.msg_amt_input = 5.0
                
                st.write("<b>💡 Tarifas rápidas o desliza la barra de abajo para cotización en vivo:</b>", unsafe_allow_html=True)
                col_sh_b1, col_sh_b2, col_sh_b3, col_sh_b4 = st.columns(4)
                if col_sh_b1.button("5 SD", key="sh_btn_5"):
                    st.session_state.msg_amt_input = 5.0
                    st.rerun()
                if col_sh_b2.button("10 SD", key="sh_btn_10"):
                    st.session_state.msg_amt_input = 10.0
                    st.rerun()
                if col_sh_b3.button("15 SD", key="sh_btn_15"):
                    st.session_state.msg_amt_input = 15.0
                    st.rerun()
                if col_sh_b4.button("20 SD", key="sh_btn_20"):
                    st.session_state.msg_amt_input = 20.0
                    st.rerun()

                # Deslizador interactivo instantáneo para celular
                amount_sd_input_slider = st.slider("🎚️ Desliza para ajustar la tarifa del envío:", min_value=0.0, max_value=200.0, value=float(st.session_state.msg_amt_input), step=1.0, key="msg_amt_slider_key")
                st.session_state.msg_amt_input = amount_sd_input_slider

                amount_sd_input = st.number_input("O escribe el monto exacto en Tokens SD:", min_value=0.0000, value=float(st.session_state.msg_amt_input), step=1.0, format="%.4f", key="msg_amt_input_field")
                st.session_state.msg_amt_input = amount_sd_input
                service_id_input = st.text_input("ID de Envío / Número de Guía (Opcional):", placeholder="Ej. GUIA-9831", key="msg_guia_input_field")
                
                st.info("📱 <b>Tip para celular:</b> Toca la pantalla fuera del teclado para actualizar la cotización de subsidio de la derecha de inmediato.")

                if st.button("Confirmar y Pagar Envío", key="pay_delivery_direct_btn"):
                    if len(driver_code_input) != 5 or not driver_code_input.isdigit():
                        st.error("⚠️ El código del móvil debe tener exactamente 5 dígitos numéricos.")
                    elif amount_sd_input <= 0:
                        st.error("⚠️ El monto del pago en SD debe ser mayor a cero.")
                    else:
                        success, msg = pay_delivery_service(st.session_state.wallet_code, driver_code_input, amount_sd_input, service_id_input)
                        if success:
                            st.balloons()
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)
            with col_ship_info:
                # Mostrar cotización del envío dinámicamente
                equiv_cop_calc = amount_sd_input * token_price_cop
                cashback_sd_preview = amount_sd_input * 0.5
                cashback_cop_preview = equiv_cop_calc * 0.5
                net_sd_preview = amount_sd_input * 0.5
                net_cop_preview = equiv_cop_calc * 0.5
                driver_receives_sd = amount_sd_input * 1.1
                driver_receives_cop = equiv_cop_calc * 1.1
                
                st.markdown(f"""
                <div class="card" style="border-left: 5px solid #10b981; background: linear-gradient(135deg, #000000 0%, #061f14 100%) !important;">
                    <h4 style="margin-top:0; color:#10b981; display:flex; align-items:center; gap:8px;">🔥 ¡Subsidio Alianza Activo!</h4>
                    <p style="font-size:0.85rem; color:#a1a1aa; margin-top:2px; line-height:1.2rem;">
                        Al pagar tu envío usando tus tokens <b>Alianza (SD)</b>, el Administrador financia automáticamente el <b>50%</b> de tu envío y te lo devuelve al instante.
                    </p>
                    <hr style="border-color:#232d42; margin: 10px 0;">
                    <p style="font-size:0.85rem; color:#ffffff; margin:3px 0;"><b>Tarifa de Envío:</b> {format_num(amount_sd_input)} SD (${format_num(equiv_cop_calc)} COP)</p>
                    <p style="font-size:0.85rem; color:#10b981; margin:3px 0;"><b>Cashback al Instante (50%):</b> +{format_num(cashback_sd_preview)} SD (+${format_num(cashback_cop_preview)} COP)</p>
                    <p style="font-size:1.1rem; color:#ffd700; font-weight:bold; margin:8px 0;"><b>Tu Costo Neto Real:</b> {format_num(net_sd_preview)} SD (${format_num(net_cop_preview)} COP)</p>
                    <hr style="border-color:#232d42; margin: 10px 0;">
                    <p style="font-size:0.85rem; color:#ffffff; margin:3px 0;"><b>El Conductor recibe (110%):</b></p>
                    <p style="font-size:1.0rem; color:#10b981; font-weight:bold; margin:3px 0;">{format_num(driver_receives_sd)} SD (${format_num(driver_receives_cop)} COP)</p>
                    <span style="font-size:0.75rem; color:#a1a1aa; line-height:1.1rem; display:block; margin-top:10px;">
                        ℹ️ El 50% de tu reembolso y el 10% de bono del conductor son financiados automáticamente de forma directa desde la billetera de fondos base del administrador.
                    </span>
                </div>
                """, unsafe_allow_html=True)
                
        with tab_pay_fee:
            st.subheader("Pago de Cuota Semanal para Móviles")
            st.write("Si conduces un móvil afiliado a la red de mensajería, debes pagar tu cuota semanal obligatoria de **$40,000 COP**.")
            st.markdown("""
            <div class="card" style="border-left: 5px solid #ffd700; background: linear-gradient(135deg, #0d0d11 0%, #201a00 100%) !important;">
                <h4 style="color:#ffd700; margin:0;">🔥 ¡Paga con Tokens SD y Obtén un 20% de Descuento!</h4>
                <p style="font-size:0.9rem; margin-top:5px; color:#ffffff; line-height:1.4rem;">
                    Si decides pagar tu cuota semanal usando tus tokens <b>Alianza (SD)</b>, el valor se reduce automáticamente a <b>$32,000 COP</b>.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Input de mensaje de reporte del usuario
            fee_message = st.text_input("💬 Mensaje o reporte de pago opcional (Ej: Pago movil Jorge):", placeholder="Ej: Pago movil Jorge", key="weekly_fee_msg_text_field")
            
            fee_cop_with_discount = 32000.0
            fee_cop_normal = 40000.0
            
            fee_sd_with_discount = fee_cop_with_discount / token_price_cop
            
            col_fee_1, col_fee_2 = st.columns(2)
            
            with col_fee_1:
                st.markdown(f"""
                <div class="card" style="border-color: #10b981; min-height: 280px; display:flex; flex-direction:column; justify-content:space-between;">
                    <div>
                        <h4 style="color:#10b981; margin-top:0;">🪙 Opción A: Pago con Tokens SD</h4>
                        <p style="font-size:0.85rem; color:#a1a1aa;">Paga con tus monedas ganadas o compradas y aprovecha el descuento de tarifa.</p>
                        <hr style="border-color:#232d42; margin:10px 0;">
                        <span style="font-size:0.9rem; color:#ffffff;"><b>Valor cuota:</b> $32,000 COP (20% OFF)</span><br>
                        <span style="font-size:1.35rem; font-weight:800; color:#ffd700; display:block; margin-top:5px;">{format_num(fee_sd_with_discount)} SD</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Pagar Cuota con SD", key="pay_fee_sd_btn"):
                    success, msg = pay_weekly_fee(st.session_state.wallet_code, use_tokens=True, message=fee_message)
                    if success:
                        st.balloons()
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
                        
            with col_fee_2:
                st.markdown(f"""
                <div class="card" style="border-color: #ffd700; min-height: 280px; display:flex; flex-direction:column; justify-content:space-between;">
                    <div>
                        <h4 style="color:#ffd700; margin-top:0;">💵 Opción B: Pago con Saldo Pesos (COP)</h4>
                        <p style="font-size:0.85rem; color:#a1a1aa;">Debita directamente de tu saldo retirable en pesos disponible en la app.</p>
                        <hr style="border-color:#232d42; margin:10px 0;">
                        <span style="font-size:0.9rem; color:#ffffff;"><b>Valor cuota:</b> $40,000 COP (Sin descuento)</span><br>
                        <span style="font-size:1.35rem; font-weight:800; color:#ffffff; display:block; margin-top:5px;">${fee_cop_normal:,.0f} COP</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Pagar Cuota con Saldo COP", key="pay_fee_cop_btn"):
                    success, msg = pay_weekly_fee(st.session_state.wallet_code, use_tokens=False, message=fee_message)
                    if success:
                        st.balloons()
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
                        
        with tab_ship_history:
            st.subheader("Historial de Operaciones de Mensajería")
            st.write("Consulta el registro de pagos de envíos realizados, recibidos y pagos de cuotas semanales de móviles.")
            
            df_m_hist = get_movil_payments_history(st.session_state.wallet_code)
            
            if len(df_m_hist) == 0:
                st.info("Aún no tienes registros de mensajería registrados.")
            else:
                df_m_display = df_m_hist.copy()
                
                df_m_display['Tipo de Pago'] = df_m_display['payment_type'].apply(
                    lambda t: "📦 Pago de Envío" if t == 'SHIPPING_PAYMENT' 
                    else ("💳 Cuota Semanal (SD)" if t == 'WEEKLY_FEE_SD' else "💳 Cuota Semanal (COP)")
                )
                
                df_m_display['Rol'] = df_m_display.apply(
                    lambda r: "Remitente/Cliente" if r['target_code'] == '99999' or r['target_code'] != st.session_state.wallet_code else "Receptor/Conductor", axis=1
                )
                
                df_m_display['De'] = df_m_display.apply(
                    lambda r: "Tú" if r['customer_name'] == st.session_state.fullname else f"{r['customer_name']}", axis=1
                )
                df_m_display['Para/Destino'] = df_m_display.apply(
                    lambda r: "Maestra / Admin" if r['target_code'] == '99999' else (f"{r['driver_name']}" if r['target_code'] == st.session_state.wallet_code else f"{r['driver_name']} ({r['target_code']})"), axis=1
                )
                
                df_m_display['Tokens SD'] = df_m_display['amount_sd'].apply(lambda x: f"{format_num(x)} SD")
                df_m_display['Pesos Colombianos'] = df_m_display['amount_cop'].apply(lambda x: f"${x:,.0f} COP")
                df_m_display['Mensaje'] = df_m_display['message'].apply(lambda x: str(x) if x else "Ninguno")
                
                df_m_display = df_m_display[['timestamp', 'Tipo de Pago', 'Rol', 'De', 'Para/Destino', 'Tokens SD', 'Pesos Colombianos', 'Mensaje']]
                df_m_display.columns = ['Fecha/Hora', 'Tipo de Operación', 'Tu Rol', 'Emisor/Cliente', 'Receptor/Destinatario', 'Tokens SD', 'Pesos Colombianos', 'Mensaje/Detalle']
                st.dataframe(df_m_display, use_container_width=True)



    # --- SECCIÓN: MIS REFERIDOS (ÁRBOL GENEALÓGICO) ---
    elif choice == "👥 Mis Referidos":
        st.markdown("<h1 class='golden-title'>👥 Mi Red de Referidos</h1>", unsafe_allow_html=True)
        st.write("Gestiona tu red de invitados de Alianza, visualiza tu árbol genealógico completo y monitorea tus ganancias generadas.")
        
        # Tarjeta de invitación principal
        st.markdown(f"""
        <div class="card" style="border-left: 5px solid #ffd700; background: linear-gradient(135deg, #0d0d11 0%, #201a00 100%) !important; padding: 20px; margin-bottom: 20px;">
            <h3 style="color: #ffd700; margin-top: 0; display: flex; align-items: center; gap: 8px;">🔗 ¡Invita Amigos y Gana de por Vida!</h3>
            <p style="font-size: 0.95rem; line-height: 1.4rem; color: #ffffff; margin-bottom: 15px;">
                Comparte tu código de referido único. Cuando tus invitados se registren con tu código y compren tokens SIAD (SD), recibirás comisiones directas:
                <br>• <b>20% de Comisión</b> de cada compra si eres un miembro regular.
                <br>• <b>👑 25% de Comisión</b> de cada compra de por vida si eres un miembro <b>VIP</b>.
            </p>
            <p style="font-size: 0.85rem; color: #a1a1aa; margin-bottom: 5px;">Tu código de referido único:</p>
            <div style="background-color: #000000; padding: 12px; border-radius: 8px; border: 1px solid #ffd70044; display: flex; justify-content: space-between; align-items: center;">
                <code style="font-size: 1.6rem; color: #10b981; font-weight: bold; letter-spacing: 0.1em;">{st.session_state.wallet_code}</code>
                <span style="color: #ffd700; font-size: 0.85rem; font-weight: bold;">🔑 Código Activo</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Métricas de referidos
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Total referidos directos
        cursor.execute("SELECT COUNT(*) FROM users WHERE referred_by = ?", (st.session_state.wallet_code,))
        direct_count = cursor.fetchone()[0] or 0
        
        # Total ganancias de comisiones de referidos (APPROVED)
        cursor.execute("SELECT SUM(reward_amount_sd) FROM referral_rewards WHERE referrer_code = ? AND status = 'APPROVED'", (st.session_state.wallet_code,))
        total_commissions_approved = cursor.fetchone()[0] or 0.0
        
        # Total ganancias de comisiones de referidos (PENDING)
        cursor.execute("SELECT SUM(reward_amount_sd) FROM referral_rewards WHERE referrer_code = ? AND status = 'PENDING'", (st.session_state.wallet_code,))
        total_commissions_pending = cursor.fetchone()[0] or 0.0
        
        conn.close()
        
        col_ref1, col_ref2, col_ref3 = st.columns(3)
        with col_ref1:
            st.markdown(f"""
            <div class="card" style="border-left: 4px solid #10b981; min-height: 110px; display: flex; flex-direction: column; justify-content: center;">
                <div class="metric-title">Referidos Directos</div>
                <div class="metric-value" style="color: #10b981;">{direct_count} Usuarios</div>
                <div class="metric-sub">Invitados de Nivel 1</div>
            </div>
            """, unsafe_allow_html=True)
        with col_ref2:
            st.markdown(f"""
            <div class="card" style="border-left: 4px solid #ffd700; min-height: 110px; display: flex; flex-direction: column; justify-content: center;">
                <div class="metric-title">Ganancias Cobradas</div>
                <div class="metric-value" style="color: #ffd700;">{format_num(total_commissions_approved)} SD</div>
                <div class="metric-sub">Comisiones ya liberadas</div>
            </div>
            """, unsafe_allow_html=True)
        with col_ref3:
            st.markdown(f"""
            <div class="card" style="border-left: 4px solid #ef4444; min-height: 110px; display: flex; flex-direction: column; justify-content: center;">
                <div class="metric-title">Comisiones Pendientes</div>
                <div class="metric-value" style="color: #ef4444;">{format_num(total_commissions_pending)} SD</div>
                <div class="metric-sub">En espera de aprobación del admin</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.subheader("🌲 Árbol Genealógico de Mi Red")
        st.write("Explora de forma visual la estructura de tu red (Soporta múltiples niveles de invitados en profundidad):")
        
        # Función recursiva para obtener árbol (Soporta múltiples niveles de invitados)
        def get_referral_tree(parent_code, level=1):
            conn_tree = get_db_connection()
            cursor_tree = conn_tree.cursor()
            cursor_tree.execute("""
                SELECT wallet_code, fullname, username 
                FROM users 
                WHERE referred_by = ?
                ORDER BY fullname ASC
            """, (parent_code,))
            referred_users = cursor_tree.fetchall()
            
            tree_nodes = []
            for wallet_code, fullname, username in referred_users:
                # Obtener ganancias generadas por este referido para su referidor directo (parent_code)
                cursor_tree.execute("""
                    SELECT SUM(reward_amount_sd) 
                    FROM referral_rewards 
                    WHERE referrer_code = ? AND referred_code = ? AND status = 'APPROVED'
                """, (parent_code, wallet_code))
                earned = cursor_tree.fetchone()[0] or 0.0
                
                children = get_referral_tree(wallet_code, level + 1)
                
                tree_nodes.append({
                    "wallet_code": wallet_code,
                    "fullname": fullname,
                    "username": username,
                    "earned": earned,
                    "level": level,
                    "children": children
                })
            conn_tree.close()
            return tree_nodes
            
        # Función recursiva para renderizar HTML con un diseño estructurado de crucigrama / árbol de conexiones
        def render_referral_tree_html(nodes, indent=0):
            if not nodes:
                return ""
            
            html = ""
            for idx, node in enumerate(nodes):
                is_last = (idx == len(nodes) - 1)
                connector = "└── " if is_last else "├── "
                
                # Diseño de fila compacta crucigrama (sin sangrías al inicio de línea para evitar modo código en Streamlit)
                html += f"""<div style="font-family: 'Segoe UI', Arial, sans-serif; color: #ffffff; font-size: 0.95rem; margin: 4px 0; padding-left: {25 * indent}px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px dotted #ffd7001a; padding-bottom: 6px;">
<div style="display: flex; align-items: center; gap: 8px;">
<span style="color: #ffd700; font-weight: bold; font-family: monospace;">{connector}</span>
<span style="color: #10b981; font-weight: bold; font-size: 1.0rem;">👤 {node['fullname']}</span>
<span style="color: #a1a1aa; font-size: 0.8rem;">(@{node['username']})</span>
<span style="background-color: #0f172a; color: #10b981; font-size: 0.75rem; padding: 2px 6px; border-radius: 4px; border: 1px solid #10b98133; font-family: monospace;">ID: {node['wallet_code']}</span>
</div>
<div style="text-align: right;">
<span style="color: #ffd700; font-weight: 850; font-size: 1.05rem;">+{format_num(node['earned'])} SD</span>
</div>
</div>"""
                if node['children']:
                    html += render_referral_tree_html(node['children'], indent + 1)
            return html
            
        # Cargar y mostrar árbol genealógico
        my_tree = get_referral_tree(st.session_state.wallet_code)
        if len(my_tree) == 0:
            st.write("") # Si no tiene referidos, aparece completamente en blanco (sin mensajes molestos)
        else:
            tree_html = f"""<div style="border: 2px solid #ffd70033; padding: 18px; border-radius: 12px; background-color: #07070a; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(255, 215, 0, 0.02);">
<div class="card" style="border-left: 4px solid #ffd700; background-color: #111116; margin-bottom: 15px; padding: 12px 15px; display: flex; justify-content: space-between; align-items: center;">
<div>
<span style="font-weight: bold; color: #ffd700; font-size: 1.1rem;">👑 Tú ({st.session_state.fullname})</span>
<span style="color: #a1a1aa; font-size: 0.85rem; margin-left: 8px;">@{st.session_state.username}</span>
<span style="color: #888899; font-size: 0.75rem; display: block; margin-top: 2px;">Cima de tu Red | Código: <code>{st.session_state.wallet_code}</code></span>
</div>
<div style="text-align: right;">
<span style="color: #10b981; font-weight: 800; font-size: 1.2rem;">+{format_num(total_commissions_approved)} SD</span>
<span style="color: #888899; font-size: 0.75rem; display: block;">Ganancias Cobradas</span>
</div>
</div>"""
            tree_html += render_referral_tree_html(my_tree)
            tree_html += "</div>"
            
            st.markdown(tree_html, unsafe_allow_html=True)



    # --- PERFIL ---
    elif choice == "👤 Mi Perfil":
        st.markdown("<h1 class='golden-title'>👤 Mi Perfil y Cuenta</h1>", unsafe_allow_html=True)
        
        tab_perf_config, tab_perf_history = st.tabs(["👤 Configuración de Cuenta", "📋 Historial Completo de Movimientos"])
        
        with tab_perf_history:
            st.markdown("### 📋 Historial Completo de Movimientos")
            st.write("Consulta el registro detallado de todas tus actividades de red, transacciones de la tienda, recargas y participación en juegos de Alianza.")
            
            try:
                df_all_tx = get_transaction_history(st.session_state.wallet_code)
                if len(df_all_tx) == 0:
                    st.info("No hay movimientos registrados en tu cuenta todavía.")
                else:
                    decoded_txs = []
                    for idx_tx, row_tx in df_all_tx.iterrows():
                        s_code = row_tx['sender_code']
                        r_code = row_tx['receiver_code']
                        amt = float(row_tx['amount'])
                        tstamp = row_tx['timestamp']
                        
                        concept = "Transacción General"
                        tx_type = "Otros"
                        amount_str = f"{format_num(amt)} SD"
                        
                        # Determinar tipo e intermediario
                        if s_code == st.session_state.wallet_code:
                            tx_type = "🔴 Gasto / Envío"
                            if r_code == '99999_LUCKY_SPIN_FEE':
                                concept = "Giro de Ruleta (Lucky Spin)"
                            elif r_code == '99999_PPT_BET':
                                concept = "Apuesta en Piedra, Papel o Tijera contra el Bot"
                            elif r_code == '99999_PPT_LOSE':
                                concept = "Apuesta Perdida en Piedra, Papel o Tijera"
                            elif r_code == '99999_TRIVIA_FEE':
                                concept = "Entrada a Trivia Alianza"
                            elif r_code == '99999_SPORTS_TICKET':
                                concept = "Compra de Ticket de Pronóstico (La Polla)"
                            elif r_code == '99999_AUCTION_BID_FEE':
                                concept = "Puja en Subasta de Centavos"
                            elif r_code == '99999_SCRATCH_FEE':
                                concept = "Compra de Tarjeta Raspa y Gana"
                            elif r_code == '99999_TIP_UNLOCK':
                                concept = "Desbloqueo de Consejo Millonario Cripto"
                            elif r_code == 'SYSTEM_STORE' or r_code == '99999_STORE_BUY':
                                concept = "Compra en Tienda Alianza"
                            elif r_code == '99999':
                                concept = "Envío directo de tokens al Administrador (Cuenta Madre)"
                            elif r_code == 'SWAP_COP':
                                concept = "Swap / Liquidación de Tokens SD a Pesos (COP)"
                                amount_str = f"-{format_num(amt)} SD"
                            elif r_code == '99999_COP':
                                concept = "Pago de Cuota Semanal en Pesos (COP)"
                            else:
                                concept = f"Envío de tokens directo al usuario {r_code}"
                        elif r_code == st.session_state.wallet_code:
                            tx_type = "🟢 Ingreso / Premio"
                            if s_code == '99999_LUCKY_SPIN_REWARD':
                                concept = "Premio de Ruleta de la Fortuna (Lucky Spin)"
                            elif s_code == '99999_PPT_REWARD':
                                concept = "Premio de Piedra, Papel o Tijera"
                            elif s_code == '99999_PPT_DRAW_REFUND':
                                concept = "Reembolso por Empate en Piedra, Papel o Tijera"
                            elif s_code == '99999_TRIVIA_REWARD':
                                concept = "Premio por Acierto en Trivia Alianza"
                            elif s_code == '99999_SPORTS_REWARD':
                                concept = "Premio Ganado en Pronósticos Deportivos (La Polla)"
                            elif s_code == '99999_SPORTS_ANNUL_REFUND':
                                concept = "Reembolso por Partido Anulado (La Polla)"
                            elif s_code == '99999_SCRATCH_REWARD':
                                concept = "Premio de Tarjeta Raspa y Gana"
                            elif s_code == 'SYSTEM_STORE_REFUND' or s_code == '99999_STORE_REFUND':
                                concept = "Reembolso o Bono de la Tienda Alianza"
                            elif s_code == '99999':
                                concept = "Acreditación directa enviada por el Administrador"
                            else:
                                concept = f"Recepción directa de tokens del usuario {s_code}"
                                
                        decoded_txs.append({
                            "Fecha/Hora": tstamp,
                            "Movimiento": tx_type,
                            "Descripción": concept,
                            "Monto (SD)": amount_str
                        })
                        
                    df_decoded = pd.DataFrame(decoded_txs)
                    st.dataframe(df_decoded.iloc[::-1], use_container_width=True)
            except Exception as e_tx:
                st.info("Cargando historial de movimientos...")

        with tab_perf_config:
            col_prof, col_pwd = st.columns(2)
            with col_prof:
                # Si el usuario es VIP, mostrar insignia llamativa
                if is_vip_user == 1:
                    st.markdown("""
                    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 15px; background: linear-gradient(135deg, #201a00 0%, #0d0d11 100%) !important; padding: 15px; border-radius: 12px; border: 1px solid #ffd700;">
                        <div style="flex-shrink: 0;">
                    """, unsafe_allow_html=True)
                    st.image(f"data:image/jpeg;base64,{VIP_BADGE_B64}", width=70)
                    st.markdown("""
                        </div>
                        <div>
                            <h3 style="margin: 0; color: #ffd700; font-weight: 800; font-size: 1.25rem;">👑 MIEMBRO VIP ALIANZA</h3>
                            <p style="margin: 4px 0 0 0; color: #ffffff; font-size: 0.85rem; line-height: 1.2rem;">Comisiones de retiro del 1% y ganancias de referidos del 25% de por vida.</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="card">
                    <h3 style="margin-top:0; color: #ffd700;">📋 Información de Cuenta</h3>
                    <hr style="border-color: #ffd700; margin: 15px 0;">
                    <p><b>Nombre Completo:</b> {st.session_state.fullname}</p>
                    <p><b>Usuario:</b> {st.session_state.username}</p>
                    <p><b>Correo Electrónico:</b> {st.session_state.email}</p>
                    <p><b>Billetera ID (Inmutable):</b> <code style="font-size: 1.15rem; color:#10b981;">{st.session_state.wallet_code}</code></p>
                    <hr style="border-color: #232d42; margin: 15px 0;">
                    <p style="font-size:0.9rem; color:#ffd700;"><b>¿Necesitas más tokens?</b></p>
                    <p style="font-size:0.85rem; color:#a1a1aa; margin-bottom:15px;">Puedes adquirir tokens directamente haciendo una transferencia e ingresando tu comprobante de pago.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Formulario dinámico para guardar y actualizar el Nequi del propio usuario o del administrador (cuenta madre)
                user_nequi_val = get_user_nequi(st.session_state.wallet_code)
                is_admin_user = (st.session_state.username == 'admin' or st.session_state.wallet_code == '99999')
                with st.form("edit_nequi_form"):
                    if is_admin_user:
                        st.write("<b>📱 Nequi Oficial de Recaudación (Cuenta Madre)</b>", unsafe_allow_html=True)
                        new_user_nequi = st.text_input("Ingresa el número de Nequi oficial para recibir pagos de usuarios:", value=token['nequi_number'], max_chars=11, placeholder="Ej. 3001234567")
                    else:
                        st.write("<b>📱 Mi Cuenta de Nequi</b>", unsafe_allow_html=True)
                        new_user_nequi = st.text_input("Ingresa tu número de celular Nequi para recibir retiros:", value=user_nequi_val, max_chars=11, placeholder="Ej. 3001234567")
                    
                    submit_nequi = st.form_submit_button("Guardar Nequi")
                    
                    if submit_nequi:
                        if new_user_nequi and (len(new_user_nequi) < 10 or not new_user_nequi.isdigit()):
                            st.error("⚠️ Por favor ingresa un número de Nequi válido de 10 dígitos.")
                        else:
                            if is_admin_user:
                                update_global_nequi(new_user_nequi)
                                st.success("✅ ¡El Nequi de recaudación oficial (Cuenta Madre) ha sido actualizado!")
                            else:
                                update_user_nequi(st.session_state.wallet_code, new_user_nequi)
                                st.success("✅ ¡Tu cuenta de Nequi ha sido actualizada!")
                            st.rerun()

                # Formulario para guardar y actualizar la Billetera BSC (Real Token)
                user_bsc_wallet_val = get_user_bsc_address(st.session_state.wallet_code)
                with st.form("edit_bsc_wallet_form"):
                    st.write("<b>🪙 Dirección de Billetera Real (Binance Smart Chain - BSC)</b>", unsafe_allow_html=True)
                    new_bsc_wallet = st.text_input("Ingresa tu dirección de MetaMask / Trust Wallet (0x...):", value=user_bsc_wallet_val, placeholder="Ej. 0x1234567890123456789012345678901234567890")
                    submit_bsc = st.form_submit_button("Sincronizar Billetera BSC")
                    
                    if submit_bsc:
                        if new_bsc_wallet and (not new_bsc_wallet.strip().startswith("0x") or len(new_bsc_wallet.strip()) != 42):
                            st.error("⚠️ Por favor ingresa una dirección de billetera BSC (0x...) válida de 42 caracteres.")
                        else:
                            update_user_bsc_address(st.session_state.wallet_code, new_bsc_wallet.strip())
                            st.success("✅ ¡Tu dirección de billetera BSC ha sido sincronizada! Tu saldo de tokens reales ahora se actualizará en tiempo real.")
                            st.rerun()
                
                if st.button("Ir a Comprar SD"):
                    st.info("Utiliza la barra lateral e ingresa al menú '📥 Comprar SD'")
                
            with col_pwd:
                st.subheader("🔒 Cambiar Contraseña")
                with st.form("pwd_form"):
                    o_pwd = st.text_input("Contraseña Actual", type="password")
                    n_pwd = st.text_input("Nueva Contraseña", type="password")
                    c_pwd = st.text_input("Confirmar Nueva Contraseña", type="password")
                    sub_p = st.form_submit_button("Actualizar Contraseña")
                    
                    if sub_p:
                        if not (o_pwd and n_pwd and c_pwd):
                            st.warning("Todos los campos son obligatorios.")
                        elif n_pwd != c_pwd:
                            st.error("Las nuevas contraseñas no coinciden.")
                        elif len(n_pwd) < 6:
                            st.error("La nueva contraseña debe tener al menos 6 caracteres.")
                        else:
                            succ, msg = change_user_password(st.session_state.username, o_pwd, n_pwd)
                            if succ:
                                st.success(msg)
                            else:
                                st.error(msg)

    # --- PESTAÑA: TÉRMINOS Y SEGURIDAD ---
    elif choice == "🛡️ Términos y Seguridad":
        st.markdown("<h1 class='golden-title'>🛡️ Términos, Condiciones y Seguridad</h1>", unsafe_allow_html=True)
        st.write("Revisa las políticas, normativas e instructivos de seguridad operacional para interactuar con la red oficial Alianza.")
        
        col_terms, col_sec = st.columns(2)
        
        with col_terms:
            st.markdown(f"""
            <div class="card" style="border-left: 4px solid #ffd700;">
                <h3 style="margin-top:0; color: #ffd700;">📝 Términos y Condiciones</h3>\n                <hr style="border-color: #ffd700; margin: 10px 0;">\n                <ol style="padding-left: 18px; font-size: 0.9rem; color: #e2e8f0; line-height: 1.5rem;">
                    <li><b>Naturaleza del Token:</b> La moneda digital SIAD (SD) opera de forma descentralizada y segura en nuestra plataforma privada. La posesión de SD representa la total conformidad con el reglamento general.</li>\n                    <li><b>Irreversibilidad de Transacciones:</b> Debido a la estructura criptográfica e inmutabilidad de la base de datos de Alianza, <b>todas las transacciones, transferencias y envíos son definitivos</b>. No existe la posibilidad de reverso, anulación o cancelación.</li>\n                    <li><b>Responsabilidad de Envío:</b> Es responsabilidad exclusiva y total del usuario remitente verificar el código único de billetera de 5 dígitos del destinatario antes de presionar el botón de envío.</li>\n                    <li><b>Veracidad de los Pagos:</b> El envío de capturas o comprobantes de pago alterados, falsos o de transacciones ya procesadas resultará en la suspensión inmediata y permanente de la cuenta del usuario sin derecho a reclamos.</li>\n                </ol>
            </div>
            """, unsafe_allow_html=True)
            
        with col_sec:
            st.markdown(f"""
            <div class="card" style="border-left: 4px solid #10b981;">
                <h3 style="margin-top:0; color: #10b981;">🔒 Estándar y Políticas de Seguridad</h3>\n                <hr style="border-color: #10b981; margin: 10px 0;">\n                <ul style="padding-left: 18px; font-size: 0.9rem; color: #e2e8f0; line-height: 1.5rem; list-style-type: square;">
                    <li><b>Criptografía de Contraseñas:</b> Su contraseña está protegida por un sistema de Hashing <b>SHA-256 de nivel bancario</b>. Nadie, ni siquiera los administradores de la plataforma, tiene acceso a ver o recuperar su clave en texto plano.</li>\n                    <li><b>Código ID Inmutable:</b> Tu identificador único de billetera de 5 dígitos se genera de manera criptográfica al momento del registro. Este código es <b>permanente, inmutable y de por vida</b>. No se puede modificar bajo ningún motivo técnico.</li>\n                    <li><b>Cierre de Sesión Seguro:</b> Recuerda que tu sesión permanece abierta mientras uses tu navegador. Si accedes a la billetera desde computadores compartidos o públicos, asegúrate de utilizar el botón <b>Cerrar Sesión</b> de la barra lateral para evitar accesos no autorizados.</li>\n                    <li><b>Soporte Oficial:</b> Los administradores nunca te pedirán tu contraseña de acceso para verificar saldos o realizar aprobaciones de comprobantes de pago.</li>\n                </ul>
            </div>
            """, unsafe_allow_html=True)

    # --- PANEL DEL PROPIETARIO ---
    elif choice == "👑 Panel del Propietario":
        st.markdown("<h1 class='golden-title'>👑 Consola del Propietario de la App</h1>", unsafe_allow_html=True)
        
        # Consola de edición expresa ultra-llamativa
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1f1a01 0%, #08080c 100%) !important; border: 3px solid #ffd700; border-radius: 15px; padding: 22px 25px; margin-top: 15px; margin-bottom: 25px; text-align: center; box-shadow: 0 0 25px rgba(255, 215, 0, 0.45); border-image: linear-gradient(to right, #ffd700, #b8860b) 1;">
            <h2 style="color:#ffd700; margin:0 0 10px 0; font-weight:950; letter-spacing:0.07em; font-size:1.6rem; text-shadow:0 0 12px rgba(255,215,0,0.4); text-transform:uppercase;">🛠️ CONSOLA DE CONFIGURACIÓN Y EDICIÓN ECONÓMICA</h2>
            <p style="font-size:0.95rem; color:#ffffff; line-height:1.5rem; margin-bottom:15px;">Como propietario, dispones del control de precios, tarifas de envío y costos de la Tienda Alianza y los minijuegos en tiempo real. Activa el botón de abajo para expandir los editores instantáneos.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Botón checkbox llamativo
        show_express_editors = st.checkbox("⚙️ MOSTRAR EDITORES EXPRESOS DE LA TIENDA Y JUEGOS EN VIVO", value=False, key="show_express_editors_chk_field")
        
        # --- NUEVA SECCIÓN DE ACCESO EXPRESO A CONFIGURACIÓN DE JUEGOS ---
        if show_express_editors:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #091c12 0%, #0d0d11 100%) !important; border: 2.5px solid #ffd700; border-radius: 12px; padding: 18px; margin-top: 15px; margin-bottom: 15px; text-align: center; box-shadow: 0 4px 15px rgba(255, 215, 0, 0.25);">
                <h3 style="color:#ffd700; margin-top:0; font-weight:900; letter-spacing:0.05em; font-size:1.2rem;">🎮 CONSOLA DE CONFIGURACIÓN RÁPIDA DE LOS JUEGOS</h3>
                <p style="font-size:0.85rem; color:#a1a1aa; margin-bottom:0px;">Modifica costos de tickets, precios de entradas, premios y multiplicadores de ganancia de todos los juegos al instante.</p>
            </div>
            """, unsafe_allow_html=True)
        
            with st.expander("🎮 ABRIR PANEL DE CONFIGURACIÓN RÁPIDA DE LOS JUEGOS (EDITAR VALORES)", expanded=False):
                st.subheader("⚙️ Configuración y Edición de Valores de Juegos")
                st.write("Modifica el valor de los tickets de entrada, precios y premios en tokens SIAD (SD) de todos los juegos interactivos de la aplicación.")
                
                # Form for express games config
                r_cost_text_e, r_cost_e = get_game_setting('ruleta_cost', default_num=1.0)
                r_prizes_e, _ = get_game_setting('ruleta_prizes', default_val='0.1,0.5,1.0,2.0,5.0,0.0')
                r_prob_e, _ = get_game_setting('ruleta_prob', default_val='20,30,25,15,5,5')
                
                _, p_mult_e = get_game_setting('ppt_multiplier', default_num=1.90)
                
                _, s_cost_e = get_game_setting('scratch_cost', default_num=0.5)
                s_prizes_e, _ = get_game_setting('scratch_prizes', default_val='0.0,0.2,0.5,1.0,3.0,10.0')
                s_prob_e, _ = get_game_setting('scratch_prob', default_val='50,25,15,7,2,1')
                
                _, tip_cost_e = get_game_setting('crypto_tip_cost', default_num=0.2)
                tip_text_e, _ = get_game_setting('crypto_tip', default_val='')
                
                curr_trivia_e = get_active_trivia()
            active_bets_e = get_active_sports_bets()
            curr_bet_e = None
            if active_bets_e:
                m_opts_exp = {f"⚽ {b['local_team']} vs {b['visitor_team']} (ID: #{b['id']})": b for b in active_bets_e}
                selected_m_exp = st.selectbox("⚽ Selecciona el partido activo a configurar de forma rápida en la consola:", list(m_opts_exp.keys()), key="exp_active_match_selectbox_field")
                curr_bet_e = m_opts_exp[selected_m_exp]
            
            with st.form("admin_games_express_config_form_v2"):
                col_exp_g1, col_exp_g2 = st.columns(2)
                with col_exp_g1:
                    st.write("<b>🎡 La Ruleta (Lucky Spin):</b>", unsafe_allow_html=True)
                    new_exp_r_cost = st.number_input("Costo de Giro de Ruleta (SD):", value=float(r_cost_e), min_value=0.0, format="%.2f", key="exp_r_cost_main")
                    new_exp_r_prizes = st.text_input("Premios (6 valores separados por comas):", value=r_prizes_e, key="exp_r_prizes_main")
                    new_exp_r_prob = st.text_input("Probabilidades (deben sumar 100):", value=r_prob_e, key="exp_r_prob_main")
                    
                    st.write("<b>🥊 Piedra, Papel o Tijera (PPT):</b>", unsafe_allow_html=True)
                    new_exp_p_mult = st.number_input("Multiplicador de Ganancia de PPT (Ej: 1.90):", value=float(p_mult_e), min_value=1.0, max_value=3.0, format="%.2f", key="exp_p_mult_main")
                    
                    st.write("<b>🧠 Trivia Alianza Activa:</b>", unsafe_allow_html=True)
                    new_exp_t_fee = st.number_input("Costo de Entrada a la Trivia (SD):", value=float(curr_trivia_e["entry_fee"]) if curr_trivia_e else 0.50, min_value=0.0, format="%.2f", key="exp_t_fee_main")
                    new_exp_t_prize = st.number_input("Premio de la Trivia (SD):", value=float(curr_trivia_e["prize_sd"]) if curr_trivia_e else 1.50, min_value=0.0001, format="%.2f", key="exp_t_prize_main")
                    
                with col_exp_g2:
                    st.write("<b>🎟️ Raspa y Gana (Scratch Cards):</b>", unsafe_allow_html=True)
                    new_exp_s_cost = st.number_input("Costo de Tarjeta (SD):", value=float(s_cost_e), min_value=0.0, format="%.2f", key="exp_s_cost_main")
                    new_exp_s_prizes = st.text_input("Premios (6 valores separados por comas):", value=s_prizes_e, key="exp_s_prizes_main")
                    new_exp_s_prob = st.text_input("Probabilidades (deben sumar 100):", value=s_prob_e, key="exp_s_prob_main")
                    
                    st.write("<b>⚽ Pronósticos Deportivos (La Polla):</b>", unsafe_allow_html=True)
                    if curr_bet_e:
                        new_exp_m_cost = st.number_input("Costo del Ticket de Pronóstico (SD):", value=float(curr_bet_e["ticket_cost"]), min_value=0.0, format="%.2f", key="exp_m_cost_main")
                        new_exp_m_prize = st.number_input("Premio por Acierto (SD):", value=float(curr_bet_e["prize_sd"]), min_value=0.0001, format="%.2f", key="exp_m_prize_main")
                        new_exp_local_team = st.text_input("Equipo Local:", value=curr_bet_e["local_team"], key="exp_m_local_team")
                        new_exp_visitor_team = st.text_input("Equipo Visitante:", value=curr_bet_e["visitor_team"], key="exp_m_visitor_team")
                        new_exp_match_time = st.text_input("Hora de Inicio:", value=curr_bet_e["match_time"], key="exp_m_match_time")
                        new_exp_ends_at = st.text_input("Hora de Finalización:", value=curr_bet_e["ends_at"], key="exp_m_ends_at")
                        new_exp_current_score = st.text_input("Marcador Actual:", value=curr_bet_e["current_score"], key="exp_m_current_score")
                        new_exp_match_status = st.text_input("Estado / Minuto del Partido:", value=curr_bet_e["match_status"], key="exp_m_match_status")
                    else:
                        st.info("ℹ️ No hay ningún partido activo para configurar rápidamente en este momento.")
                    
                    st.write("<b>🔮 Consejo Cripto:</b>", unsafe_allow_html=True)
                    new_exp_tip_cost = st.number_input("Costo para desbloquear Consejo (SD):", value=float(tip_cost_e), min_value=0.0, format="%.2f", key="exp_tip_cost_main")
                
                submit_exp_games_config = st.form_submit_button("💾 Guardar Ajustes de Todos los Juegos")
                
                if submit_exp_games_config:
                    r_probs_chk = [int(x) for x in new_exp_r_prob.split(',') if x]
                    s_probs_chk = [int(x) for x in new_exp_s_prob.split(',') if x]
                    
                    if sum(r_probs_chk) != 100 or sum(s_probs_chk) != 100:
                        st.error("⚠️ Las probabilidades de la Ruleta y del Raspa y Gana deben sumar exactamente 100.")
                    elif len(new_exp_r_prizes.split(',')) != 6 or len(new_exp_s_prizes.split(',')) != 6:
                        st.error("⚠️ Debes ingresar exactamente 6 valores de premios para la Ruleta y para el Raspa y Gana.")
                    else:
                        update_game_setting('ruleta_cost', '', new_exp_r_cost)
                        update_game_setting('ruleta_prizes', new_exp_r_prizes, 0.0)
                        update_game_setting('ruleta_prob', new_exp_r_prob, 0.0)
                        update_game_setting('ppt_multiplier', '', new_exp_p_mult)
                        update_game_setting('scratch_cost', '', new_exp_s_cost)
                        update_game_setting('scratch_prizes', new_exp_s_prizes, 0.0)
                        update_game_setting('scratch_prob', new_exp_s_prob, 0.0)
                        update_game_setting('crypto_tip_cost', '', new_exp_tip_cost)
                        
                        if curr_trivia_e:
                            conn_t_up_exp = get_db_connection()
                            cursor_t_up_exp = conn_t_up_exp.cursor()
                            cursor_t_up_exp.execute("UPDATE trivias SET entry_fee = ?, prize_sd = ? WHERE id = ?", (new_exp_t_fee, new_exp_t_prize, curr_trivia_e["id"]))
                            conn_t_up_exp.commit()
                            conn_t_up_exp.close()
                            
                        if curr_bet_e:
                            conn_m_up_exp = get_db_connection()
                            cursor_m_up_exp = conn_m_up_exp.cursor()
                            cursor_m_up_exp.execute("""
                                UPDATE sports_bets 
                                SET ticket_cost = ?, prize_sd = ?, local_team = ?, visitor_team = ?, 
                                    match_name = ?, match_time = ?, ends_at = ?, current_score = ?, match_status = ? 
                                WHERE id = ?
                            """, (new_exp_m_cost, new_exp_m_prize, new_exp_local_team, new_exp_visitor_team, 
                                  f"{new_exp_local_team} vs {new_exp_visitor_team}", new_exp_match_time, new_exp_ends_at, 
                                  new_exp_current_score, new_exp_match_status, curr_bet_e["id"]))
                            conn_m_up_exp.commit()
                            conn_m_up_exp.close()
                            
                        st.success("✅ ¡Ajustes de todos los juegos guardados con éxito!")
                        st.rerun()
            
            # --- NUEVA SECCIÓN DE ACCESO EXPRESO A EDICIÓN DE TIENDA ---
            st.markdown("""
            <div style="background: linear-gradient(135deg, #1e1b00 0%, #0d0d11 100%) !important; border: 2.5px solid #ffd700; border-radius: 12px; padding: 18px; margin-bottom: 15px; text-align: center; box-shadow: 0 4px 15px rgba(255, 215, 0, 0.25);">
                <h3 style="color:#ffd700; margin-top:0; font-weight:900; letter-spacing:0.05em; font-size:1.2rem;">🛍️ CONSOLA DE EDICIÓN EXPRESA DE LA TIENDA</h3>
                <p style="font-size:0.85rem; color:#a1a1aa; margin-bottom:0px;">Modifica costos de envío, valores de productos, combos de alimentos y pines digitales al instante de forma rápida.</p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("🛍️ ABRIR PANEL DE EDICIÓN RÁPIDA DE LA TIENDA ALIANZA (EDITAR VALORES)", expanded=False):
                st.subheader("🛒 Catálogo General de Precios de la Tienda")
                st.write("Modifica el nombre, descripción, costo de tokens (SD) y tarifas de envío al instante. Los cambios se guardarán automáticamente en la base de datos.")
                
                try:
                    conn_items_exp = get_db_connection()
                    try:
                        store_items_list_exp = pd.read_sql_query("SELECT id, name, description, price_sd, item_type, delivery_fee_sd FROM store_items", conn_items_exp)
                    except Exception:
                        store_items_list_exp = pd.read_sql_query("SELECT id, name, description, price_sd, item_type, 0.0 as delivery_fee_sd FROM store_items", conn_items_exp)
                    conn_items_exp.close()
                    
                    for idx_i_e, item_row_e in store_items_list_exp.iterrows():
                        i_id_e = item_row_e['id']
                        i_name_e = item_row_e['name']
                        i_type_e = item_row_e['item_type']
                        i_price_e = float(item_row_e['price_sd'])
                        i_desc_e = item_row_e['description']
                        i_deliv_e = float(item_row_e['delivery_fee_sd']) if item_row_e['delivery_fee_sd'] is not None else 0.0
                        
                        type_label_e = "🏆 Membresía VIP Alianza" if i_type_e == 'MEMBERSHIP' else ("🍔 Alimentos y Bebidas" if i_type_e == 'FOOD' else "🎁 Tarjeta de Regalo / Pin / Recarga")
                        with st.container():
                            st.write(f"<b>Editar Artículo: {i_name_e} ({type_label_e})</b>", unsafe_allow_html=True)
                            with st.form(f"edit_express_store_item_form_{i_id_e}"):
                                edit_name_e = st.text_input("Nombre del Artículo", value=i_name_e)
                                edit_desc_e = st.text_area("Descripción", value=i_desc_e, height=80)
                                edit_price_e = st.number_input("Costo del Artículo (SD)", value=i_price_e, min_value=0.0001, format="%.4f")
                                edit_deliv_e = st.number_input("Tarifa de Envío / Domicilio (SD)", value=i_deliv_e, min_value=0.0, format="%.4f") if i_type_e == 'FOOD' else 0.0
                                submit_item_edit_e = st.form_submit_button(f"💾 Guardar Cambios para '{i_name_e}'")
                                
                                if submit_item_edit_e:
                                    if not edit_name_e.strip() or not edit_desc_e.strip():
                                        st.error("⚠️ El nombre y la descripción no pueden estar vacíos.")
                                    else:
                                        update_store_item_price(i_id_e, edit_price_e, edit_name_e, edit_desc_e, edit_deliv_e)
                                        st.success(f"✅ ¡Se han guardado los cambios para '{edit_name_e}' con éxito!")
                                        st.rerun()
                            st.markdown("<hr style='border-color: #ffd7001a;'>", unsafe_allow_html=True)
                except Exception as e_exp:
                    st.write("Cargando catálogo...")
            
        pending_claims_count = len(get_pending_purchases())
        pending_rewards_count = len(get_pending_referral_rewards())
        pending_withdraws_count = len(get_pending_withdrawals())
        pending_store_count = len(get_pending_store_purchases())
        
        tab_mint, tab_claims, tab_withdraws, tab_store, tab_referrals, tab_fees, tab_messenger, tab_broadcast, tab_settings = st.tabs([
            "💸 Emisión de Monedas", 
            f"📥 Comprobantes por Confirmar ({pending_claims_count})", 
            f"💰 Solicitudes de Retiro ({pending_withdraws_count})",
            f"🛍️ Pedidos de Tienda ({pending_store_count})",
            f"👥 Comisiones de Referidos ({pending_rewards_count})",
            "📊 Comisiones de Plataforma",
            "🚚 Control de Mensajería",
            "📢 Enviar Comunicado",
            "⚙️ Configuración del Token y Nequi"
        ])
        
        with tab_mint:
            st.subheader("👥 Control de Usuarios Registrados y Emisión")
            
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users WHERE is_admin = 0")
            total_users_registered = cursor.fetchone()[0] or 0
            
            # Tabla de directorio completa de todos los usuarios
            users_all_df = pd.read_sql_query("""
                SELECT fullname as 'Nombre Completo', 
                       username as 'Nombre de Usuario', 
                       wallet_code as 'Código de Billetera (ID)', 
                       balance as 'Balance (SD)', 
                       balance_cop as 'Saldo Retirable (COP)',
                       CASE WHEN is_vip = 1 THEN '👑 VIP' ELSE '👤 Regular' END as 'Rango'
                FROM users 
                WHERE is_admin = 0
                ORDER BY fullname ASC
            """, conn)
            conn.close()
            
            # Tarjeta de métrica destacada superior
            st.markdown(f"""
            <div class="card" style="border-left: 5px solid #ffd700; padding: 15px; margin-bottom: 20px; display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <h3 style="margin: 0; color: #ffd700; font-size: 1.15rem; font-weight: bold; text-transform: uppercase; letter-spacing: 0.05em;">👥 Total de Usuarios Registrados</h3>
                    <p style="margin: 5px 0 0 0; font-size: 0.85rem; color: #a1a1aa;">Usuarios activos registrados en la base de datos de Alianza.</p>
                </div>
                <div>
                    <span style="font-size: 2.2rem; font-weight: 900; color: #ffffff; text-shadow: 0 0 10px rgba(255, 215, 0, 0.35);">{total_users_registered}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Mostrar tabla detallada de usuarios
            st.write("<b>📋 Directorio de Cuentas y Códigos de Billetera:</b>", unsafe_allow_html=True)
            if len(users_all_df) == 0:
                st.info("No hay usuarios registrados todavía.")
            else:
                st.dataframe(users_all_df, use_container_width=True)
                
            st.markdown("---")
            st.subheader("💸 Cargar Monedas Directamente")
            st.write("Acredita saldo directamente ingresando el código de billetera.")
            
            with st.form("mint_form"):
                t_code = st.text_input("Ingresa el código de 5 dígitos del destinatario", max_chars=5, placeholder="Ej. 12345")
                m_amount = st.number_input(f"Monto de {token['symbol']} a emitir y transferir", min_value=0.0001, step=100.0, format="%.4f")
                submit_m = st.form_submit_button("Acreditar Billetera")
                
                if submit_m:
                    if len(t_code) != 5 or not t_code.isdigit():
                        st.error("El código debe ser de exactamente 5 dígitos numéricos.")
                    else:
                        succ, msg = send_points("99999", t_code, m_amount)
                        if succ:
                            # Enviar notificación directa por asignación manual
                            add_notification(
                                t_code,
                                f"👑 <b>¡Acreditación Oficial!</b> El propietario de la app ha cargado directamente "
                                f"<b>{format_num(m_amount)} SD</b> en tu cuenta."
                            )
                            st.success(f"¡Asignación Exitosa! Se enviaron {format_num(m_amount)} {token['symbol']} al código {t_code}.")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error(msg)
            
            st.markdown("---")
            st.subheader("👑 Gestión y Activación Manual de Membresía VIP")
            st.write("Como propietario, puedes otorgar o remover directamente el estado VIP de cualquier usuario:")
            with st.form("manual_vip_form"):
                vip_wallet_code = st.text_input("Código de Billetera del Usuario (5 dígitos):", max_chars=5, placeholder="Ej. 12345")
                action_vip = st.selectbox("Acción a ejecutar:", ["Activar Membresía VIP (1% Comisión)", "Desactivar Membresía VIP (2% Comisión)"])
                submit_vip_btn = st.form_submit_button("Ejecutar Acción VIP")
                
                if submit_vip_btn:
                    if len(vip_wallet_code) != 5 or not vip_wallet_code.isdigit():
                        st.error("⚠️ El código de billetera debe constar exactamente de 5 dígitos numéricos.")
                    else:
                        is_enable = "Activar" in action_vip
                        success_v, msg_v = toggle_user_vip_manually(vip_wallet_code, is_enable)
                        if success_v:
                            st.success(msg_v)
                            st.balloons()
                            st.rerun()
                        else:
                            st.error(msg_v)
                                
        with tab_claims:
            st.subheader("📥 Verificación Manual de Comprobantes de Nequi")
            st.write("Revisa los recibos enviados por los usuarios. Verifica en tu Nequi personal antes de aprobar la acreditación.")
            
            claims_df = get_pending_purchases()
            
            if len(claims_df) == 0:
                st.info("🎉 ¡Al día! No hay comprobantes de pago pendientes de verificación.")
            else:
                for idx, row in claims_df.iterrows():
                    with st.expander(f"📥 Solicitud #{row['id']} - Usuario: {row['fullname']} ({row['user_code']})"):
                        col_req_info, col_req_image = st.columns([1, 1])
                        
                        with col_req_info:
                            st.markdown(f"""
                            <div class="card" style="border-left: 3px solid #ffd700;">
                                <p><b>Usuario:</b> {row['fullname']} (@{row['username']})</p>\n                                <p><b>Código de Billetera:</b> <code style="color:#10b981;">{row['user_code']}</code></p>\n                                <p><b>Cantidad de Dinero Transferido:</b> <span style="color:#ffd700; font-weight:bold;">${row['amount_cop']:,.0f} COP</span></p>\n                                <p><b>Tokens SD a Acreditar:</b> <span style="color:#10b981; font-weight:bold;">{row['amount_sd']:,.4f} SD</span></p>\n                                <p><b>Fecha de Solicitud:</b> {row['timestamp']}</p>\n                            </div>
                            """, unsafe_allow_html=True)
                            
                            col_app, col_app_vip, col_rej = st.columns(3)
                            with col_app:
                                if st.button("Confirmar Compra (Tokens SD)", key=f"app_{row['id']}"):
                                    success, msg = approve_purchase(row['id'])
                                    if success:
                                        st.success("¡Transacción aprobada y tokens acreditados!")
                                        st.rerun()
                                    else:
                                        st.error(msg)
                            with col_app_vip:
                                if st.button("👑 Confirmar como VIP", key=f"app_vip_{row['id']}"):
                                    success, msg = approve_purchase_as_vip(row['id'])
                                    if success:
                                        st.success("¡Membresía VIP aprobada y activada con éxito!")
                                        st.rerun()
                                    else:
                                        st.error(msg)
                            with col_rej:
                                if st.button("Rechazar Solicitud", key=f"rej_{row['id']}"):
                                    if reject_purchase(row['id']):
                                        st.warning("Solicitud de pago rechazada.")
                                        st.rerun()
                                        
                        with col_req_image:
                            st.subheader("📷 Comprobante Recibido")
                            try:
                                # Mostrar la imagen BLOB guardada en la base de datos
                                st.image(row['proof_image'], caption="Foto del recibo de Nequi subida por el usuario", use_container_width=True)
                            except Exception as e:
                                st.error(f"No se pudo cargar la imagen del comprobante: {str(e)}")
                                
        with tab_withdraws:
            st.subheader("💰 Validación y Pago Manual de Retiros a Nequi")
            st.write("Revisa las solicitudes de retiro en pesos (COP). Transfiere el **Monto Neto** al número de Nequi indicado, toma una captura e impleméntala como comprobante para validar y dar de baja el retiro de forma definitiva.")
            
            with_df = get_pending_withdrawals()
            
            if len(with_df) == 0:
                st.info("🎉 ¡Al día! No hay solicitudes de retiro pendientes de pago.")
            else:
                for idx, row in with_df.iterrows():
                    with st.expander(f"💸 Retiro #{row['id']} - Usuario: {row['fullname']} ({row['user_code']})"):
                        col_w_info, col_w_pay = st.columns([1, 1])
                        
                        with col_w_info:
                            st.markdown(f"""
                            <div class="card" style="border-left: 3px solid #ffd700;">
                                <p><b>Usuario Solicitante:</b> {row['fullname']} (@{row['username']})</p>
                                <p><b>Código de Billetera:</b> <code style="color:#10b981;">{row['user_code']}</code></p>
                                <p><b>Cuenta Nequi a Transferir:</b> <span style="color:#ffd700; font-weight:bold; font-size:1.2rem;">{row['nequi_number']}</span></p>
                                <p><b>Monto de Retiro Total:</b> ${row['amount_cop']:,.0f} COP</p>
                                <p><b>Comisión Operativa (2%):</b> ${row['fee_cop']:,.0f} COP</p>
                                <p><b>Monto Neto a Enviar:</b> <span style="color:#10b981; font-weight:bold; font-size:1.3rem;">${row['net_cop']:,.0f} COP</span></p>
                                <p><b>Fecha de Solicitud:</b> {row['timestamp']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                        with col_w_pay:
                            st.subheader("Subir Soporte Nequi y Confirmar Pago")
                            with st.form(f"admin_confirm_withdrawal_{row['id']}"):
                                with_receipt = st.file_uploader("Adjunta captura de pantalla de transferencia de Nequi realizada:", type=["jpg", "jpeg", "png"], key=f"w_receipt_{row['id']}")
                                
                                col_btn_app, col_btn_rej = st.columns(2)
                                with col_btn_app:
                                    submit_app = st.form_submit_button("Confirmar y Enviar Retiro")
                                    if submit_app:
                                        if not with_receipt:
                                            st.error("⚠️ Debes subir la captura de la transferencia de Nequi antes de confirmar.")
                                        else:
                                            try:
                                                receipt_bytes = with_receipt.read()
                                                success, msg = approve_withdrawal(row['id'], receipt_bytes)
                                                if success:
                                                    st.success("¡Pago de retiro confirmado y comunicado con éxito!")
                                                    st.balloons()
                                                    st.rerun()
                                                else:
                                                    st.error(msg)
                                            except Exception as e:
                                                st.error(f"Error procesando la aprobación: {str(e)}")
                                with col_btn_rej:
                                    submit_rej = st.form_submit_button("Rechazar y Reembolsar COP")
                                    if submit_rej:
                                        if reject_withdrawal(row['id']):
                                            st.warning("Retiro rechazado. Los fondos han sido reembolsados al usuario de inmediato.")
                                            st.rerun()
                                
        with tab_store:
            st.subheader("🛍️ Gestión de Pedidos de la Tienda Alianza")
            st.write("Procesa las compras de los usuarios de la tienda. Puedes entregar el código de activación (PIN) o aprobar la activación VIP.")
            
            store_claims_df = get_pending_store_purchases()
            
            if len(store_claims_df) == 0:
                st.info("🎉 ¡Al día! No hay pedidos de tienda pendientes de entrega.")
            else:
                for idx, row in store_claims_df.iterrows():
                    with st.expander(f"🛍️ Pedido #{row['id']} - {row['name']} - Usuario: {row['fullname']} ({row['user_code']})"):
                        st.markdown(f"""
                        <div class="card" style="border-left: 3px solid #10b981;">
                            <p><b>Artículo comprado:</b> <span style="color:#10b981; font-weight:bold;">{row['name']}</span> ({row['item_type']})</p>
                            <p><b>Usuario:</b> {row['fullname']} (@{row['username']})</p>
                            <p><b>Código de Billetera:</b> <code>{row['user_code']}</code></p>
                            <p><b>Tokens SD Descontados:</b> <span style="color:#ffd700; font-weight:bold;">{row['price_sd']:,.4f} SD</span></p>
                            <p><b>Fecha de Compra:</b> {row['timestamp']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if row['item_type'] == 'MEMBERSHIP':
                            st.write("💡 Este artículo es una Membresía VIP. Al aprobarlo, se le activarán las comisiones reducidas (1%) y bonos (25%) automáticamente.")
                            col_app_s, col_rej_s = st.columns(2)
                            with col_app_s:
                                if st.button("Aprobar y Activar VIP", key=f"app_store_{row['id']}"):
                                    success, msg = deliver_store_purchase(row['id'], "VIP_ACTIVATED")
                                    if success:
                                        st.success(msg)
                                        st.rerun()
                                    else:
                                        st.error(msg)
                            with col_rej_s:
                                if st.button("Rechazar y Reembolsar SD", key=f"rej_store_vip_{row['id']}"):
                                    if reject_store_purchase(row['id']):
                                        st.warning("Compra rechazada y tokens reembolsados.")
                                        st.rerun()
                        else:
                            with st.form(f"deliver_pin_form_{row['id']}"):
                                pin_code = st.text_input("Ingresa el PIN / Código de Activación / Mensaje:", placeholder="Ej. NF-8492-9482-PK19")
                                col_app_s, col_rej_s = st.columns(2)
                                with col_app_s:
                                    submit_deliv = st.form_submit_button("Entregar y Notificar Código")
                                    if submit_deliv:
                                        if not pin_code:
                                            st.error("⚠️ Debes proporcionar el Pin/Código para entregarlo al usuario.")
                                        else:
                                            success, msg = deliver_store_purchase(row['id'], pin_code)
                                            if success:
                                                st.success(msg)
                                                st.rerun()
                                            else:
                                                st.error(msg)
                                with col_rej_s:
                                    submit_rej_store = st.form_submit_button("Rechazar y Reembolsar SD")
                                    if submit_rej_store:
                                        if reject_store_purchase(row['id']):
                                            st.warning("Compra rechazada y tokens reembolsados.")
                                            st.rerun()

        with tab_referrals:
            st.subheader("👥 Gestión de Comisiones por Referidos")
            st.write("Cada vez que un usuario que fue invitado realiza una compra y es aprobada, se calcula un 20% de comisión para su referidor. Valida y autoriza el pago aquí.")
            
            ref_rewards_df = get_pending_referral_rewards()
            
            if len(ref_rewards_df) == 0:
                st.info("🎉 ¡Al día! No hay comisiones de referidos pendientes de pago.")
            else:
                for idx, row in ref_rewards_df.iterrows():
                    with st.expander(f"👥 Comisión #{row['id']} - Referidor: {row['referrer_name']} ({row['referrer_code']})"):
                        st.markdown(f"""
                        <div class="card" style="border-left: 3px solid #10b981;">
                            <p><b>Referidor (Beneficiario):</b> {row['referrer_name']} (Billetera: <code style="color:#10b981;">{row['referrer_code']}</code>)</p>
                            <p><b>Referido (Comprador):</b> {row['referred_name']} (Billetera: <code>{row['referred_code']}</code>)</p>
                            <p><b>Monto de Compra:</b> <span style="color:#ffffff; font-weight:bold;">{row['purchase_amount_sd']:,.4f} SD</span></p>
                            <p><b>Comisión Pendiente (20%):</b> <span style="color:#ffd700; font-weight:bold; font-size:1.15rem;">{row['reward_amount_sd']:,.4f} SD</span></p>
                            <p><b>Fecha de Registro:</b> {row['timestamp']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        col_pay, col_dec = st.columns(2)
                        with col_pay:
                            if st.button("Aprobar y Enviar Comisión", key=f"pay_ref_{row['id']}"):
                                success, msg = approve_referral_reward(row['id'])
                                if success:
                                    st.success(f"¡Comisión de {row['reward_amount_sd']:,.4f} SD pagada exitosamente!")
                                    st.rerun()
                                else:
                                    st.error(msg)
                        with col_dec:
                            if st.button("Rechazar Comisión", key=f"rej_ref_{row['id']}"):
                                if reject_referral_reward(row['id']):
                                    st.warning("Comisión de referidos cancelada.")
                                    st.rerun()

        with tab_fees:
            st.subheader("📊 Comisiones de la Plataforma (2% por Retiros)")
            st.write("La plataforma recauda un **2% de comisión** en pesos colombianos (COP) por cada retiro aprobado. Por políticas de seguridad, estas comisiones quedan **bloqueadas por 24 horas** a partir de la aprobación del retiro y posteriormente quedan libres para ser reclamadas por el propietario.")
            
            # Obtener resumen de comisiones
            total_fees, locked_fees, available_fees = get_platform_fees_summary()
            
            col_f1, col_f2, col_f3 = st.columns(3)
            with col_f1:
                st.markdown(f"""
                <div class="card" style="border-left: 5px solid #3b82f6;">
                    <div class="metric-title">Comisiones Totales Históricas</div>
                    <div class="metric-value" style="color: #3b82f6;">${total_fees:,.0f} COP</div>
                    <div class="metric-sub">Comisiones recaudadas en total</div>
                </div>
                """, unsafe_allow_html=True)
            with col_f2:
                st.markdown(f"""
                <div class="card" style="border-left: 5px solid #ef4444;">
                    <div class="metric-title">🔒 Comisiones Bloqueadas (24 Horas)</div>
                    <div class="metric-value" style="color: #ef4444;">${locked_fees:,.0f} COP</div>
                    <div class="metric-sub">Bajo resguardo de seguridad</div>
                </div>
                """, unsafe_allow_html=True)
            with col_f3:
                st.markdown(f"""
                <div class="card" style="border-left: 5px solid #10b981;">
                    <div class="metric-title">🔓 Comisiones Liberadas / Retirables</div>
                    <div class="metric-value" style="color: #10b981;">${available_fees:,.0f} COP</div>
                    <div class="metric-sub">Listas para ser transferidas a tu balance</div>
                </div>
                """, unsafe_allow_html=True)
                
            # Botón para reclamar
            if available_fees > 0:
                if st.button("Reclamar y Acreditar Comisiones Liberadas"):
                    success, msg = claim_platform_fees()
                    if success:
                        st.balloons()
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
            else:
                st.info("ℹ️ No hay comisiones liberadas pendientes por reclamar en este momento. Las comisiones bloqueadas se liberarán automáticamente después de 24 horas de la aprobación de su respectivo retiro.")
                
            # Tabla de registros de comisiones
            st.subheader("📋 Historial de Comisiones por Retiro")
            df_fees_list = get_approved_withdrawals_fees()
            
            if len(df_fees_list) == 0:
                st.info("No hay registros de comisiones recaudadas todavía.")
            else:
                def calculate_remaining_time(approved_at_str):
                    if not approved_at_str:
                        return "🔓 Liberado"
                    try:
                        approved_time = datetime.strptime(approved_at_str, "%Y-%m-%d %H:%M:%S")
                        release_time = approved_time + timedelta(hours=24)
                        now = datetime.utcnow()
                        if now < release_time:
                            remaining = release_time - now
                            hours, remainder = divmod(remaining.seconds, 3600)
                            minutes, _ = divmod(remainder, 60)
                            return f"🔒 Bloqueado ({hours}h {minutes}m restantes)"
                        else:
                            return "🔓 Liberado"
                    except Exception:
                        return "🔓 Liberado"
                
                df_fees_list['Tiempo de Bloqueo'] = df_fees_list['approved_at'].apply(calculate_remaining_time)
                df_fees_list['Monto del Retiro'] = df_fees_list['amount_cop'].apply(lambda x: f"${x:,.0f} COP")
                df_fees_list['Comisión Recaudada (2%)'] = df_fees_list['fee_cop'].apply(lambda x: f"${x:,.0f} COP")
                df_fees_list['Estado del Saldo'] = df_fees_list.apply(
                    lambda r: "Claimed (Reclamado)" if r['fee_status'] == 'CLAIMED' else r['Tiempo de Bloqueo'], axis=1
                )
                
                df_fees_display = df_fees_list[['approved_at', 'fullname', 'user_code', 'Monto del Retiro', 'Comisión Recaudada (2%)', 'Estado del Saldo']]
                df_fees_display.columns = ['Fecha Aprobación', 'Usuario', 'Código Billetera', 'Monto del Retiro', 'Comisión Recaudada', 'Estado / Bloqueo']
                st.dataframe(df_fees_display, use_container_width=True)

        with tab_messenger:
            st.subheader("🚚 Control de Operaciones de Mensajería y Móviles")
            st.write("Monitorea todos los pagos de envíos entre clientes y conductores, así como el recaudo de cuotas semanales.")
            
            df_all_m = get_all_movil_payments()
            
            if len(df_all_m) == 0:
                st.info("No hay transacciones de mensajería registradas en el sistema.")
            else:
                df_all_m_display = df_all_m.copy()
                df_all_m_display['Tipo de Pago'] = df_all_m_display['payment_type'].apply(
                    lambda t: "📦 Pago de Envío" if t == 'SHIPPING_PAYMENT' 
                    else ("💳 Cuota Semanal (SD)" if t == 'WEEKLY_FEE_SD' else "💳 Cuota Semanal (COP)")
                )
                df_all_m_display['Cliente'] = df_all_m_display.apply(lambda r: f"{r['customer_name']} ({r['user_code']})", axis=1)
                df_all_m_display['Destino'] = df_all_m_display.apply(
                    lambda r: "Admin / Maestra" if r['target_code'] == '99999' else f"{r['target_name']} ({r['target_code']})", axis=1
                )
                df_all_m_display['Monto (SD)'] = df_all_m_display['amount_sd'].apply(lambda x: f"{format_num(x)} SD")
                df_all_m_display['Valor (COP)'] = df_all_m_display['amount_cop'].apply(lambda x: f"${x:,.0f} COP")
                df_all_m_display['Mensaje'] = df_all_m_display['message'].apply(lambda x: str(x) if x else "Ninguno")
                
                df_all_m_display = df_all_m_display[['timestamp', 'Tipo de Pago', 'Cliente', 'Destino', 'Monto (SD)', 'Valor (COP)', 'Mensaje']]
                df_all_m_display.columns = ['Fecha/Hora', 'Tipo de Pago', 'Móvil / Emisor', 'Conductor / Destino', 'Tokens SD', 'Pesos Colombianos', 'Mensaje/Detalle']
                st.dataframe(df_all_m_display, use_container_width=True)


        with tab_broadcast:
            st.subheader("📢 Enviar Comunicado Global a todos los Usuarios")
            st.write("Escribe un mensaje que desees difundir de forma masiva a todos los usuarios registrados en sus bandejas de entrada (Notificaciones).")
            
            with st.form("broadcast_form"):
                broadcast_msg = st.text_area(
                    "Contenido del Mensaje (Soporta HTML básico como <b> o emojis 🚀)", 
                    placeholder="Ej. 🚀 <b>¡Atención!</b> El valor del token SIAD (SD) ha subido un 10% hoy. ¡Revisa tu balance!",
                    height=150
                )
                submit_b = st.form_submit_button("📢 Difundir Comunicado")
                
                if submit_b:
                    if not broadcast_msg.strip():
                        st.error("⚠️ El mensaje no puede estar vacío.")
                    else:
                        broadcast_notification(broadcast_msg)
                        st.success("🎉 ¡Comunicado global enviado exitosamente a todos los usuarios!")
                        st.balloons()
                        st.rerun()

        with tab_settings:
            st.subheader("⚙️ Configuración y Edición General de la Aplicación")
            st.write("Como Propietario de Alianza, tienes control total para editar precios, productos de la tienda, crear/resolver juegos, trivias, subastas y configurar los parámetros del token en tiempo real.")
            
            # --- SUB-TABS DENTRO DEL PANEL DE CONFIGURACIÓN ---
            tab_adm_store, tab_adm_trivia, tab_adm_sports, tab_adm_penny, tab_adm_games, tab_adm_token = st.tabs([
                "🛍️ Editar Tienda (Alimentos/Pines)",
                "🧠 Control Trivia",
                "⚽ Control Pronósticos",
                "🔨 Control Subastas",
                "🎡 Configuración de Juegos",
                "🪙 Parámetros Token y Nequi"
            ])
            
            # 1. EDITAR TIENDA (Pines, Alimentos, Recargas)
            with tab_adm_store:
                st.subheader("🛍️ Editar Precios e Información de la Tienda")
                st.write("Modifica el nombre, descripción, costo en tokens (SD) y tarifa de envío de alimentos de cualquier artículo de la tienda Alianza.")
                
                conn_items = get_db_connection()
                # Cargar todos los artículos incluyendo delivery_fee_sd
                try:
                    store_items_list = pd.read_sql_query("SELECT id, name, description, price_sd, item_type, delivery_fee_sd FROM store_items", conn_items)
                except Exception:
                    store_items_list = pd.read_sql_query("SELECT id, name, description, price_sd, item_type, 0.0 as delivery_fee_sd FROM store_items", conn_items)
                conn_items.close()
                
                for idx_i, item_row in store_items_list.iterrows():
                    i_id = item_row['id']
                    i_name = item_row['name']
                    i_type = item_row['item_type']
                    i_price = float(item_row['price_sd'])
                    i_desc = item_row['description']
                    i_deliv = float(item_row['delivery_fee_sd']) if item_row['delivery_fee_sd'] is not None else 0.0
                    
                    # Labels according to type
                    type_labels = {
                        'MEMBERSHIP': "🏆 Membresía VIP Alianza",
                        'GIFT_CARD': "🎁 Tarjeta de Regalo / Pin",
                        'FOOD': "🍔 Alimento o Bebida Express",
                        'CARRIER_RECHARGE': "📱 Recarga de Datos / Minutos"
                    }
                    type_label = type_labels.get(i_type, "🛒 Artículo General")
                    
                    with st.expander(f"✏️ Editar: {i_name} ({type_label})"):
                        with st.form(f"edit_store_item_form_v2_{i_id}"):
                            edit_name = st.text_input("Nombre del Artículo", value=i_name)
                            edit_desc = st.text_area("Descripción", value=i_desc, height=80)
                            edit_price = st.number_input("Costo del Artículo (SD)", value=i_price, min_value=0.0001, format="%.4f")
                            
                            # Conditionally show delivery fee if food
                            edit_delivery = 0.0
                            if i_type == 'FOOD':
                                edit_delivery = st.number_input("Costo de Envío / Domicilio (SD)", value=i_deliv, min_value=0.0, format="%.2f")
                                
                            submit_item_edit = st.form_submit_button(f"Guardar Cambios de {i_name}")
                            
                            if submit_item_edit:
                                if not edit_name.strip() or not edit_desc.strip():
                                    st.error("⚠️ El nombre y la descripción no pueden estar vacíos.")
                                else:
                                    update_store_item_price(i_id, edit_price, edit_name, edit_desc, edit_delivery)
                                    st.success(f"✅ ¡Se han guardado los cambios para '{edit_name}' con éxito!")
                                    st.rerun()

            # 2. CONTROL TRIVIA ALIANZA
            with tab_adm_trivia:
                st.subheader("🧠 Publicar y Configurar Trivia Alianza")
                st.write("Modifica la trivia activa para que los usuarios respondan y ganen tokens.")
                
                curr_trivia = get_active_trivia()
                
                with st.form("admin_trivia_form"):
                    t_question = st.text_input("Pregunta de la Trivia:", value=curr_trivia["question"] if curr_trivia else "¿De qué color es el logo de Binance?")
                    t_opt_a = st.text_input("Opción A:", value=curr_trivia["option_a"] if curr_trivia else "Rojo")
                    t_opt_b = st.text_input("Opción B:", value=curr_trivia["option_b"] if curr_trivia else "Amarillo y Negro")
                    t_opt_c = st.text_input("Opción C:", value=curr_trivia["option_c"] if curr_trivia else "Verde")
                    t_correct = st.selectbox("Opción Correcta:", ["A", "B", "C"], index=["A", "B", "C"].index(curr_trivia["correct_option"]) if curr_trivia else 1)
                    t_fee = st.number_input("Costo de Entrada a la Trivia (SD):", value=float(curr_trivia["entry_fee"]) if curr_trivia else 0.50, min_value=0.0, format="%.2f")
                    t_prize = st.number_input("Premio de la Trivia (SD):", value=float(curr_trivia["prize_sd"]) if curr_trivia else 1.50, min_value=0.0001, format="%.2f")
                    
                    submit_trivia_edit = st.form_submit_button("📢 Publicar / Actualizar Trivia Activa")
                    
                    if submit_trivia_edit:
                        conn_t_up = get_db_connection()
                        cursor_t_up = conn_t_up.cursor()
                        # Desactivar trivias anteriores
                        cursor_t_up.execute("UPDATE trivias SET active = 0")
                        # Insertar nueva trivia activa
                        cursor_t_up.execute("""
                            INSERT INTO trivias (question, option_a, option_b, option_c, correct_option, entry_fee, prize_sd, active)
                            VALUES (?, ?, ?, ?, ?, ?, ?, 1)
                        """, (t_question, t_opt_a, t_opt_b, t_opt_c, t_correct, t_fee, t_prize))
                        conn_t_up.commit()
                        conn_t_up.close()
                        
                        st.success("✅ ¡Se ha publicado la nueva trivia activa con éxito! Se han reiniciado las participaciones para esta nueva pregunta.")
                        st.rerun()

            # 3. CONTROL PRONÓSTICOS DEPORTIVOS (LA POLLA)
            with tab_adm_sports:
                st.subheader("⚽ Administrar Pronósticos Deportivos (La Polla)")
                st.write("Establece los partidos activos, el costo de participación y el premio. También puedes editar, anular o resolver cada partido y pagar a los ganadores.")
                
                active_bets = get_active_sports_bets()
                curr_bet = None
                
                if active_bets:
                    match_opts_admin = {f"⚽ {b['local_team']} vs {b['visitor_team']} (ID: #{b['id']})": b for b in active_bets}
                    selected_match_label_admin = st.selectbox("🎯 Selecciona el partido activo a editar, resolver o anular:", list(match_opts_admin.keys()), key="admin_active_match_selectbox")
                    curr_bet = match_opts_admin[selected_match_label_admin]
                else:
                    st.info("ℹ️ No hay ningún partido activo en este momento.")
                
                col_ab1, col_ab2 = st.columns(2)
                with col_ab1:
                    with st.expander("📢 Publicar Nuevo Partido Activo (Desde Cero)", expanded=(curr_bet is None)):
                        with st.form("admin_new_match_form"):
                            m_local = st.text_input("Equipo Local:", value="Colombia")
                            m_visitor = st.text_input("Equipo Visitante:", value="Argentina")
                            m_time = st.text_input("Hora de Inicio (ej. 2026-09-03 18:00):", value="Hoy 18:00")
                            m_ends_at = st.text_input("Hora de Finalización (ej. 2026-09-03 20:00):", value="Hoy 20:00")
                            m_cost = st.number_input("Costo del Ticket (SD):", value=1.0, min_value=0.0, format="%.2f")
                            m_prize = st.number_input("Premio por Acierto (SD):", value=3.0, min_value=0.0001, format="%.2f")
                            submit_new_match = st.form_submit_button("⚽ Publicar Nuevo Partido")
                            
                            if submit_new_match:
                                conn_m_up = get_db_connection()
                                cursor_m_up = conn_m_up.cursor()
                                # Insertar nuevo partido activo (no cancelamos los demás!)
                                cursor_m_up.execute("""
                                    INSERT INTO sports_bets (match_name, ticket_cost, prize_sd, status, local_team, visitor_team, match_time, ends_at, current_score, match_status)
                                    VALUES (?, ?, ?, 'ACTIVE', ?, ?, ?, ?, '0 - 0', 'No iniciado')
                                """, (f"{m_local} vs {m_visitor}", m_cost, m_prize, m_local, m_visitor, m_time, m_ends_at))
                                conn_m_up.commit()
                                conn_m_up.close()
                                st.success(f"✅ ¡Partido '{m_local} vs {m_visitor}' publicado con éxito!")
                                st.rerun()
                                
                    if curr_bet:
                        with st.expander("✏️ Editar/Actualizar Partido Seleccionado (Marcador, Tiempos, Equipos, Premio)", expanded=True):
                            with st.form("admin_edit_match_form"):
                                e_local = st.text_input("Equipo Local:", value=curr_bet["local_team"])
                                e_visitor = st.text_input("Equipo Visitante:", value=curr_bet["visitor_team"])
                                e_time = st.text_input("Hora de Inicio:", value=curr_bet["match_time"])
                                e_ends_at = st.text_input("Hora de Finalización:", value=curr_bet["ends_at"])
                                e_score = st.text_input("Marcador Actual (ej. 1 - 0):", value=curr_bet["current_score"])
                                e_status = st.text_input("Estado / Minuto (ej. En Vivo - Minuto 45):", value=curr_bet["match_status"])
                                e_cost = st.number_input("Costo del Ticket (SD):", value=float(curr_bet["ticket_cost"]), min_value=0.0, format="%.2f")
                                e_prize = st.number_input("Premio por Acierto (SD):", value=float(curr_bet["prize_sd"]), min_value=0.0001, format="%.2f")
                                submit_edit_match = st.form_submit_button("💾 Guardar Cambios del Partido Seleccionado")
                                
                                if submit_edit_match:
                                    conn_m_edit = get_db_connection()
                                    cursor_m_edit = conn_m_edit.cursor()
                                    cursor_m_edit.execute("""
                                        UPDATE sports_bets 
                                        SET ticket_cost = ?, prize_sd = ?, local_team = ?, visitor_team = ?, 
                                            match_name = ?, match_time = ?, ends_at = ?, current_score = ?, match_status = ? 
                                        WHERE id = ?
                                    """, (e_cost, e_prize, e_local, e_visitor, f"{e_local} vs {e_visitor}", e_time, e_ends_at, e_score, e_status, curr_bet["id"]))
                                    conn_m_edit.commit()
                                    conn_m_edit.close()
                                    st.success("✅ ¡Los datos del partido se han actualizado con éxito!")
                                    st.rerun()
                            
                with col_ab2:
                    if curr_bet:
                        st.write("<b>🏁 Resolver Partido Seleccionado (Pagar Premios):</b>", unsafe_allow_html=True)
                        st.warning(f"Partido a Resolver: {curr_bet['match_name']} (ID: #{curr_bet['id']})")
                        with st.form("admin_resolve_match_form"):
                            winner_choice = st.selectbox("Selecciona la Opción Ganadora:", ["LOCAL", "EMPATE", "VISITANTE"])
                            submit_resolve = st.form_submit_button("🏁 Confirmar Resultado y Pagar Ganadores")
                            
                            if submit_resolve:
                                success_res, msg_res = resolve_sports_bet(curr_bet["id"], winner_choice)
                                if success_res:
                                    st.success(msg_res)
                                    st.balloons()
                                    st.rerun()
                                else:
                                    st.error(msg_res)
                                    
                        st.markdown("---")
                        st.write("<b>❌ Anular Partido y Reembolsar Tickets:</b>", unsafe_allow_html=True)
                        st.write("Si el partido seleccionado fue suspendido, cancelado o aplazado, presiona el botón de abajo para anularlo y reembolsar el costo del ticket completo a todos los usuarios de forma automática.")
                        if st.button("❌ Anular Partido y Reembolsar Saldo", key=f"annul_sports_bet_btn_{curr_bet['id']}"):
                            with st.spinner("⏳ Procesando anulación y reembolsos en la base de datos..."):
                                success_an, msg_an = annul_sports_bet(curr_bet["id"])
                                if success_an:
                                    st.success(msg_an)
                                    import time
                                    time.sleep(1.5)
                                    st.rerun()
                                else:
                                    st.error(msg_an)

            # 4. CONTROL SUBASTAS DE CENTAVOS
            with tab_adm_penny:
                st.subheader("🔨 Configurar Subasta de Centavos")
                st.write("Configura el artículo en subasta, precio inicial, incrementos, costo de puja y el tiempo de expiración.")
                
                curr_auc = get_active_auction()
                
                with st.form("admin_auction_form"):
                    a_item = st.text_input("Artículo de la Subasta:", value=curr_auc["item_name"] if curr_auc else "Netflix Premium 1 Mes")
                    a_desc = st.text_area("Descripción del Artículo:", value=curr_auc["description"] if curr_auc else "Pin de entretenimiento digital")
                    a_price = st.number_input("Precio Inicial de Subasta (SD):", value=float(curr_auc["current_price"]) if curr_auc else 1.0, min_value=0.0001, format="%.2f")
                    a_increment = st.number_input("Incremento por puja (SD):", value=float(curr_auc["bid_increment"]) if curr_auc else 0.05, min_value=0.0001, format="%.4f")
                    a_fee = st.number_input("Costo de tarifa por puja (SD):", value=float(curr_auc["bid_fee_sd"]) if curr_auc else 0.10, min_value=0.0001, format="%.4f")
                    a_duration_mins = st.number_input("Duración de la Subasta en Minutos (desde ahora):", value=120, min_value=1)
                    
                    submit_auc_edit = st.form_submit_button("🔨 Publicar / Reiniciar Subasta Activa")
                    
                    if submit_auc_edit:
                        conn_a_up = get_db_connection()
                        cursor_a_up = conn_a_up.cursor()
                        # Finalizar anteriores activos
                        cursor_a_up.execute("UPDATE penny_auctions SET status = 'ENDED' WHERE status = 'ACTIVE'")
                        # Calcular expiración
                        ends_at_str = (datetime.utcnow() + timedelta(minutes=a_duration_mins)).strftime('%Y-%m-%d %H:%M:%S')
                        # Insertar nueva
                        cursor_a_up.execute("""
                            INSERT INTO penny_auctions (item_name, description, current_price, highest_bidder, ends_at, bid_fee_sd, bid_increment, status)
                            VALUES (?, ?, ?, '99999', ?, ?, ?, 'ACTIVE')
                        """, (a_item, a_desc, a_price, ends_at_str, a_fee, a_increment))
                        conn_a_up.commit()
                        conn_a_up.close()
                        
                        st.success(f"✅ ¡Nueva subasta de '{a_item}' iniciada con éxito! Expira en {a_duration_mins} minutos.")
                        st.rerun()

            # 5. CONFIGURACIÓN DE JUEGOS (Ruleta, PPT, Raspa, Consejos)
            with tab_adm_games:
                st.subheader("🎡 Configuración Técnica de Ruleta, Duelos y Consejos")
                st.write("Modifica el valor de las apuestas, multiplicadores de ganancias y probabilidades de los minijuegos interactivos de la Tienda.")
                
                # Cargar valores actuales
                r_cost_text, r_cost = get_game_setting('ruleta_cost', default_num=1.0)
                r_prizes, _ = get_game_setting('ruleta_prizes', default_val='0.1,0.5,1.0,2.0,5.0,0.0')
                r_prob, _ = get_game_setting('ruleta_prob', default_val='20,30,25,15,5,5')
                
                _, p_mult = get_game_setting('ppt_multiplier', default_num=1.90)
                
                _, s_cost = get_game_setting('scratch_cost', default_num=0.5)
                s_prizes, _ = get_game_setting('scratch_prizes', default_val='0.0,0.2,0.5,1.0,3.0,10.0')
                s_prob, _ = get_game_setting('scratch_prob', default_val='50,25,15,7,2,1')
                
                _, tip_cost = get_game_setting('crypto_tip_cost', default_num=0.2)
                tip_text, _ = get_game_setting('crypto_tip', default_val='')
                
                with st.form("admin_games_config_form"):
                    col_cg1, col_cg2 = st.columns(2)
                    with col_cg1:
                        st.write("<b>🎡 Parámetros de la Ruleta (Lucky Spin):</b>", unsafe_allow_html=True)
                        new_r_cost = st.number_input("Costo de Giro de Ruleta (SD):", value=float(r_cost), min_value=0.0, format="%.2f")
                        new_r_prizes = st.text_input("Premios de la Ruleta (6 valores separados por comas):", value=r_prizes)
                        new_r_prob = st.text_input("Probabilidades de la Ruleta (6 valores separados por comas, deben sumar 100):", value=r_prob)
                        
                        st.write("<b>🥊 Parámetros Piedra, Papel o Tijera (PPT):</b>", unsafe_allow_html=True)
                        new_p_mult = st.number_input("Multiplicador de Ganancia de PPT (Ej: 1.90):", value=float(p_mult), min_value=1.0, max_value=3.0, format="%.2f")
                        
                        st.write("<b>🔮 Parámetros de Alerta Cripto / Consejo del Día:</b>", unsafe_allow_html=True)
                        new_tip_cost = st.number_input("Costo para desbloquear el Consejo Cripto (SD):", value=float(tip_cost), min_value=0.0, format="%.2f")
                        new_tip_text = st.text_area("Contenido del Consejo / Alerta:", value=tip_text, height=80)
                        
                    with col_cg2:
                        st.write("<b>🎟️ Parámetros Raspa y Gana (Scratch Cards):</b>", unsafe_allow_html=True)
                        new_s_cost = st.number_input("Costo de Tarjeta Raspa y Gana (SD):", value=float(s_cost), min_value=0.0, format="%.2f")
                        new_s_prizes = st.text_input("Premios Raspa y Gana (6 valores separados por comas):", value=s_prizes)
                        new_s_prob = st.text_input("Probabilidades Raspa y Gana (6 valores separados por comas, deben sumar 100):", value=s_prob)
                        
                    submit_games_config = st.form_submit_button("🎡 Guardar Ajustes Generales de Juegos")
                    
                    if submit_games_config:
                        # Validaciones rápidas
                        r_probs_chk = [int(x) for x in new_r_prob.split(',') if x]
                        s_probs_chk = [int(x) for x in new_s_prob.split(',') if x]
                        
                        if sum(r_probs_chk) != 100 or sum(s_probs_chk) != 100:
                            st.error("⚠️ Las probabilidades de la Ruleta y del Raspa y Gana deben sumar exactamente 100.")
                        elif len(new_r_prizes.split(',')) != 6 or len(new_s_prizes.split(',')) != 6:
                            st.error("⚠️ Debes ingresar exactamente 6 valores de premios para la Ruleta y para el Raspa y Gana.")
                        else:
                            update_game_setting('ruleta_cost', '', new_r_cost)
                            update_game_setting('ruleta_prizes', new_r_prizes, 0.0)
                            update_game_setting('ruleta_prob', new_r_prob, 0.0)
                            update_game_setting('ppt_multiplier', '', new_p_mult)
                            update_game_setting('scratch_cost', '', new_s_cost)
                            update_game_setting('scratch_prizes', new_s_prizes, 0.0)
                            update_game_setting('scratch_prob', new_s_prob, 0.0)
                            update_game_setting('crypto_tip_cost', '', new_tip_cost)
                            update_game_setting('crypto_tip', new_tip_text, 0.0)
                            
                            st.success("✅ ¡Ajustes generales de los juegos guardados con éxito!")
                            st.rerun()

            # 6. CONFIGURACIÓN DEL TOKEN Y NEQUI (Muelle Original)
            with tab_adm_token:
                st.subheader("⚙️ Parámetros Cripto y Cuenta Madre")
                
                is_admin_user = (st.session_state.username == 'admin' or st.session_state.wallet_code == '99999')
                if not is_admin_user:
                    st.warning("⚠️ Solamente el usuario administrador principal (@admin) puede editar la configuración global de la plataforma y el número de Nequi oficial.")
                    st.info(f"<b>Nequi Oficial del Administrador para Recibir Pagos:</b> {token['nequi_number']}")
                else:
                    st.write("Desde aquí personalizas las características de tu propia criptomoneda y el canal de pago de forma global.")
                    with st.form("settings_form"):
                        new_name = st.text_input("Nombre de la Criptomoneda", value=token['name'])
                        new_symbol = st.text_input("Símbolo del Token", value=token['symbol'], max_chars=10)
                        new_contract = st.text_input("Dirección de Contrato (Smart Contract)", value=token['contract'])
                        new_price = st.number_input("Valor en USD de cada Token (USD)", value=token['price_usd'], min_value=0.000001, format="%.6f", step=0.01)
                        new_nequi = st.text_input("Número de Cuenta NEQUI Oficial para Recibir Pagos", value=token['nequi_number'])
                        submit_s = st.form_submit_button("Guardar Configuración Técnica")
                        
                        if submit_s:
                            if not (new_name and new_symbol and new_contract and new_nequi):
                                st.error("Todos los campos de configuración son obligatorios.")
                            else:
                                update_token_settings(new_name, new_symbol, new_contract, new_price, new_nequi)
                                st.success("¡Configuración general guardada con éxito!")
                                st.rerun()
