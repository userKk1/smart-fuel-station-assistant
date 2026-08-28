import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "station.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def get_dashboard_kpis():

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM stations")
        stations = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM transactions")
        transactions = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM maintenance")
        maintenance = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM complaints")
        complaints = cursor.fetchone()[0]

        cursor.execute("""
            SELECT
                COUNT(*),
                COALESCE(SUM(amount), 0),
                COALESCE(SUM(liters), 0)
            FROM transactions
        """)

        transactions, revenue, liters = cursor.fetchone()

        ticket_moyen = (
            revenue / transactions
            if transactions > 0
            else 0
        )


        return {
            "stations": stations,
            "transactions": transactions,
            "revenue": revenue,
            "liters": liters,
            "maintenance": maintenance,
            "complaints": complaints,
            "ticket_moyen": ticket_moyen
        }

    finally:
        conn.close()



def get_transactions_by_city():

    conn = get_connection()

    try:

        query = """
        SELECT
            s.city,
            COUNT(t.transaction_id) AS transactions
        FROM stations s
        INNER JOIN transactions t
            ON s.station_id = t.station_id
        GROUP BY s.city
        ORDER BY transactions DESC
        """

        return conn.execute(query).fetchall()

    finally:
        conn.close()



def get_failures_by_station():

    conn = get_connection()

    try:

        query = """
        SELECT
            s.station_name,
            COUNT(m.failure_type) AS failures
        FROM stations s
        INNER JOIN maintenance m
            ON s.station_id = m.station_id
        GROUP BY s.station_name
        ORDER BY failures DESC
        """

        return conn.execute(query).fetchall()

    finally:
        conn.close()



def get_low_stock():

    conn = get_connection()

    try:

        query = """
        SELECT
            s.station_name,
            i.fuel_type,
            i.current_stock,
            i.reorder_level
        FROM inventory i
        INNER JOIN stations s
            ON i.station_id = s.station_id
        WHERE i.current_stock <= i.reorder_level
        ORDER BY i.current_stock ASC
        """

        return conn.execute(query).fetchall()

    finally:
        conn.close()

def get_stations():

    conn = get_connection()

    try:

        query = """
        SELECT
            station_id,
            station_name,
            city
        FROM stations
        ORDER BY station_name
        """

        return conn.execute(query).fetchall()

    finally:
        conn.close()



def get_maintenance_summary():

    conn = get_connection()

    try:

        query = """
        SELECT
            COUNT(*) AS total_failures,
            COUNT(DISTINCT station_id) AS affected_stations
        FROM maintenance
        """

        return conn.execute(query).fetchone()

    finally:
        conn.close()



def get_maintenance_by_station():

    conn = get_connection()

    try:

        query = """
        SELECT
            s.station_name,
            s.city,
            COUNT(m.failure_type) AS failures
        FROM maintenance m
        INNER JOIN stations s
            ON m.station_id = s.station_id
        GROUP BY s.station_id, s.station_name, s.city
        ORDER BY failures DESC
        """

        return conn.execute(query).fetchall()

    finally:
        conn.close()



def get_maintenance_by_type():

    conn = get_connection()

    try:

        query = """
        SELECT
            failure_type,
            COUNT(*) AS occurrences
        FROM maintenance
        GROUP BY failure_type
        ORDER BY occurrences DESC
        """

        return conn.execute(query).fetchall()

    finally:
        conn.close()



def get_maintenance_details():

    conn = get_connection()

    try:

        query = """
        SELECT
            m.maintenance_id,
            s.station_name,
            s.city,
            m.failure_type
        FROM maintenance m
        INNER JOIN stations s
            ON m.station_id = s.station_id
        ORDER BY m.maintenance_id DESC
        """

        return conn.execute(query).fetchall()

    finally:
        conn.close()



def get_complaints_summary():

    conn = get_connection()

    try:

        query = """
        SELECT
            COUNT(*) AS total_complaints,
            COUNT(DISTINCT station_id) AS affected_stations
        FROM complaints
        """

        return conn.execute(query).fetchone()

    finally:
        conn.close()



def get_complaints_by_station():

    conn = get_connection()

    try:

        query = """
        SELECT
            s.station_name,
            s.city,
            COUNT(c.complaint_id) AS complaints
        FROM complaints c
        INNER JOIN stations s
            ON c.station_id = s.station_id
        GROUP BY s.station_id, s.station_name, s.city
        ORDER BY complaints DESC
        """

        return conn.execute(query).fetchall()

    finally:
        conn.close()



def get_complaints_details():

    conn = get_connection()

    try:

        query = """
        SELECT *
        FROM complaints
        ORDER BY complaint_id DESC
        """

        return conn.execute(query).fetchall()

    finally:
        conn.close()



def get_complaints_columns():

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute("PRAGMA table_info(complaints)")

        return [
            column[1]
            for column in cursor.fetchall()
        ]

    finally:
        conn.close()



def get_transactions_summary():

    conn = get_connection()

    try:

        query = """
        SELECT
            COUNT(*) AS total_transactions,
            COUNT(DISTINCT station_id) AS active_stations
        FROM transactions
        """

        return conn.execute(query).fetchone()

    finally:
        conn.close()



def get_transactions_by_station():

    conn = get_connection()

    try:

        query = """
        SELECT
            s.station_name,
            s.city,
            COUNT(t.transaction_id) AS transactions
        FROM transactions t
        INNER JOIN stations s
            ON t.station_id = s.station_id
        GROUP BY s.station_id, s.station_name, s.city
        ORDER BY transactions DESC
        """

        return conn.execute(query).fetchall()

    finally:
        conn.close()



def get_transactions_by_city():

    conn = get_connection()

    try:

        query = """
        SELECT
            s.city,
            COUNT(t.transaction_id) AS transactions
        FROM transactions t
        INNER JOIN stations s
            ON t.station_id = s.station_id
        GROUP BY s.city
        ORDER BY transactions DESC
        """

        return conn.execute(query).fetchall()

    finally:
        conn.close()



def get_transactions_details():

    conn = get_connection()

    try:

        query = """
        SELECT *
        FROM transactions
        ORDER BY transaction_id DESC
        """

        return conn.execute(query).fetchall()

    finally:
        conn.close()



def get_transactions_columns():

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute("PRAGMA table_info(transactions)")

        return [
            column[1]
            for column in cursor.fetchall()
        ]

    finally:
        conn.close()




def get_monthly_sales():

    conn = get_connection()

    try:

        query = """
        SELECT
            strftime('%Y-%m', datetime) AS month,
            SUM(amount) AS revenue
        FROM transactions
        WHERE datetime IS NOT NULL
          AND amount IS NOT NULL
        GROUP BY month
        ORDER BY month
        """

        return conn.execute(query).fetchall()

    finally:
        conn.close()




def get_top_stations(limit=5):

    conn = get_connection()

    try:

        query = """
        SELECT
            s.station_name,
            s.city,
            COUNT(t.transaction_id) AS transactions,
            SUM(t.amount) AS revenue,
            SUM(t.liters) AS liters
        FROM transactions t
        INNER JOIN stations s
            ON t.station_id = s.station_id
        GROUP BY
            s.station_id,
            s.station_name,
            s.city
        ORDER BY revenue DESC
        LIMIT ?
        """

        return conn.execute(query, (limit,)).fetchall()

    finally:
        conn.close()




def get_stations():

    conn = get_connection()

    try:

        query = """
        SELECT
            s.station_id,
            s.station_name,
            s.city,
            i.fuel_type,
            i.tank_capacity,
            i.current_stock,
            i.reorder_level
        FROM stations s
        LEFT JOIN inventory i
            ON s.station_id = i.station_id
        ORDER BY s.station_name, i.fuel_type
        """

        return conn.execute(query).fetchall()

    finally:
        conn.close()




def get_pumps():

    conn = get_connection()

    try:

        query = """
        SELECT
            pump_id,
            station_name,
            fuel_type,
            installation_date,
            age,
            status,
            usage_count,
            repair_end_date
        FROM pumps
        ORDER BY station_name, pump_id
        """

        return conn.execute(query).fetchall()

    finally:
        conn.close()