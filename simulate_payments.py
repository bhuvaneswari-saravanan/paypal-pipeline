# ============================================
# PAYPAL PAYMENT SIMULATOR
# Simulates real PayPal transactions! 
# ============================================

import psycopg2
import uuid
import random
import time
from faker import Faker
from datetime import datetime

# ---- SETUP ----
fake = Faker()

# ---- DATABASE CONFIG ----
DB_CONFIG = {
    "host":     "localhost",
    "database": "paypal_db",
    "user":     "postgres",
    "password": "1613",
    "port":     "5432"
}

# ---- PAYMENT SETTINGS ----
CURRENCIES = ["USD", "SGD", "MYR", "EUR", "GBP"]
STATUSES = ["success", "success", "success", "failed", "pending"]
TRANSACTION_TYPES = ["payment", "transfer", "refund", "withdrawal"]
MERCHANTS = [
    "shopee.com", "grab.com", "lazada.sg",
    "amazon.com", "netflix.com", "spotify.com",
    "airbnb.com", "uber.com", "foodpanda.sg"
]
COUNTRIES = ["SG", "MY", "ID", "TH", "PH", "VN", "US", "GB"]

# ---- GENERATE ONE FAKE TRANSACTION ----
def generate_transaction():
    return {
        "transaction_id":   str(uuid.uuid4()),
        "sender_email":     fake.email(),
        "receiver_email":   random.choice(MERCHANTS),
        "amount":           round(random.uniform(1.00, 999.99), 2),
        "currency":         random.choice(CURRENCIES),
        "status":           random.choice(STATUSES),
        "country":          random.choice(COUNTRIES),
        "transaction_type": random.choice(TRANSACTION_TYPES),
        "created_at":       datetime.now()
    }

# ---- SAVE TO DATABASE ----
def save_transaction(conn, txn):
    cursor = conn.cursor()
    sql = """
        INSERT INTO transactions
        (transaction_id, sender_email, receiver_email,
         amount, currency, status, country,
         transaction_type, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        txn["transaction_id"],
        txn["sender_email"],
        txn["receiver_email"],
        txn["amount"],
        txn["currency"],
        txn["status"],
        txn["country"],
        txn["transaction_type"],
        txn["created_at"]
    )
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()

# ---- MAIN ----
def main():
    print("=" * 55)
    print("PAYPAL PAYMENT SIMULATOR STARTED!")
    print("=" * 55)

    conn = psycopg2.connect(**DB_CONFIG)
    print("Connected to PayPal database!")
    print("Generating transactions every 2 seconds...")
    print("Press Ctrl+C to stop\n")

    count = 0
    while True:
        try:
            txn = generate_transaction()
            save_transaction(conn, txn)
            count += 1

            status_icon = if txn["status"] == "success" else "❌"
            print(f"{status_icon} #{count} | "
                  f"{txn['sender_email'][:20]:<20} | "
                  f"${txn['amount']:>7.2f} {txn['currency']} | "
                  f"{txn['status']:<8} | "
                  f"{txn['country']}")

            time.sleep(2)

        except KeyboardInterrupt:
            print(f"\n Stopped! Total transactions: {count}")
            break
        except Exception as e:
            print(f" Error: {e}")
            break

    conn.close()
    print("Done!")

if __name__ == "__main__":
    main()



    import psycopg2
from psycopg2.extras import execute_values

def push_to_postgres(transactions_list):
    try:
        # DB_CONFIG use panni connect panrom
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # Batch insert query
        query = """
        INSERT INTO transactions (
            transaction_id, sender_email, receiver_email, amount, 
            currency, status, country, transaction_type, created_at
        ) VALUES %s
        """
        
        # Transactions list-a values-a mathi push panrom
        execute_values(cur, query, transactions_list)
        
        conn.commit()
        print(f"Successfully inserted {len(transactions_list)} records!")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()
