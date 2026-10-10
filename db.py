# ============================================================
#  db.py — ชั้นติดต่อฐานข้อมูล
# ============================================================
import mysql.connector
import config


def get_connection():
    return mysql.connector.connect(
        host=config.DB_HOST, user=config.DB_USER, password=config.DB_PASSWORD,
        database=config.DB_NAME, port=config.DB_PORT)


def run_query(sql, params=None):
    """รัน SELECT คืนผลเป็น list ของ dict"""
    conn = get_connection(); cur = conn.cursor(dictionary=True)
    cur.execute(sql, params or ()); rows = cur.fetchall()
    cur.close(); conn.close(); return rows


def run_command(sql, params=None):
    """รัน INSERT / UPDATE / DELETE แล้ว commit"""
    conn = get_connection(); cur = conn.cursor()
    cur.execute(sql, params or ()); conn.commit()
    out = {"new_id": cur.lastrowid, "affected": cur.rowcount}
    cur.close(); conn.close(); return out


# ---------- สมาชิก (member) ----------
def search_members(filters):
    sql = "SELECT * FROM member WHERE 1=1"
    params = []
    if filters.get("name"):
        sql += " AND name LIKE %s"
        params.append("%" + filters["name"] + "%")
    if filters.get("gender"):
        sql += " AND gender = %s"
        params.append(filters["gender"])
    if filters.get("package_type"):
        sql += " AND package_type = %s"
        params.append(filters["package_type"])
    sql += " ORDER BY member_id"
    return run_query(sql, params)   


def get_member(member_id):
    """ดึง สมาชิก 1 รายการตาม member_id (ใช้ตอนเปิดฟอร์มแก้ไข)"""
    sql = "SELECT * FROM member WHERE member_id = %s"
    rows = run_query(sql, (member_id,))
    return rows[0] if rows else None


def create_member(data):
    """เพิ่ม สมาชิก ใหม่ — data มีคีย์: name, gender, join_date, package_type"""
    sql = """
        INSERT INTO member (name, gender, join_date, package_type)
        VALUES (%s, %s, %s, %s)
    """
    params = (
        data.get("name"),
        data.get("gender"),
        data.get("join_date"),
        data.get("package_type")
    )
    return run_command(sql, params)


def update_member(member_id, data):
    """แก้ไข สมาชิก ตาม member_id"""
    sql = """
        UPDATE member
        SET name = %s, gender = %s, join_date = %s, package_type = %s
        WHERE member_id = %s
    """
    params = (
        data.get("name"),
        data.get("gender"),
        data.get("join_date"),
        data.get("package_type"),
        member_id
    )
    return run_command(sql, params)


def delete_member(member_id):
    """ลบ สมาชิก ตาม member_id"""
    sql = "DELETE FROM member WHERE member_id = %s"
    return run_command(sql, (member_id,))


# ---------- คลาสเรียน (gym_class) ----------
def search_classes(filters):
    """ค้นหา คลาสเรียน ตามเงื่อนไข (name, room)"""
    sql = "SELECT * FROM gym_class WHERE 1=1"
    params = []
    if filters.get("name"):
        sql += " AND name LIKE %s"
        params.append("%" + filters["name"] + "%")
    if filters.get("room"):
        sql += " AND room LIKE %s"
        params.append("%" + filters["room"] + "%")
    sql += " ORDER BY class_id"
    return run_query(sql, params)


def get_class(class_id):
    """ดึง คลาสเรียน 1 รายการตาม class_id (ใช้ตอนเปิดฟอร์มแก้ไข)"""
    sql = "SELECT * FROM gym_class WHERE class_id = %s"
    rows = run_query(sql, (class_id,))
    return rows[0] if rows else None


def create_class(data):
    """เพิ่ม คลาสเรียน ใหม่ — data มีคีย์: name, trainer_id, room, capacity, schedule_time"""
    sql = """
        INSERT INTO gym_class (name, trainer_id, room, capacity, schedule_time)
        VALUES (%s, %s, %s, %s, %s)
    """
    params = (
        data.get("name"),
        data.get("trainer_id"),
        data.get("room"),
        data.get("capacity"),
        data.get("schedule_time")
    )
    return run_command(sql, params)


def update_class(class_id, data):
    """แก้ไข คลาสเรียน ตาม class_id"""
    sql = """
        UPDATE gym_class
        SET name = %s, trainer_id = %s, room = %s, capacity = %s, schedule_time = %s
        WHERE class_id = %s
    """
    params = (
        data.get("name"),
        data.get("trainer_id"),
        data.get("room"),
        data.get("capacity"),
        data.get("schedule_time"),
        class_id
    )
    return run_command(sql, params)


def delete_class(class_id):
    """ลบ คลาสเรียน ตาม class_id"""
    sql = "DELETE FROM gym_class WHERE class_id = %s"
    return run_command(sql, (class_id,))


# ---------- การจอง (booking) ----------
def search_bookings(filters):
    """ค้นหา การจอง ตามเงื่อนไข (member_id, class_id, status)"""
    sql = "SELECT * FROM booking WHERE 1=1"
    params = []
    if filters.get("member_id"):
        sql += " AND member_id = %s"
        params.append(filters["member_id"])
    if filters.get("class_id"):
        sql += " AND class_id = %s"
        params.append(filters["class_id"])
    if filters.get("status"):
        sql += " AND status = %s"
        params.append(filters["status"])
    sql += " ORDER BY booking_id"
    return run_query(sql, params)


def get_booking(booking_id):
    """ดึง การจอง 1 รายการตาม booking_id (ใช้ตอนเปิดฟอร์มแก้ไข)"""
    sql = "SELECT * FROM booking WHERE booking_id = %s"
    rows = run_query(sql, (booking_id,))
    return rows[0] if rows else None


def create_booking(data):
    """เพิ่ม การจอง ใหม่ — data มีคีย์: member_id, class_id, book_date, status"""
    sql = """
        INSERT INTO booking (member_id, class_id, book_date, status)
        VALUES (%s, %s, %s, %s)
    """
    params = (
        data.get("member_id"),
        data.get("class_id"),
        data.get("book_date"),
        data.get("status")
    )
    return run_command(sql, params)


def update_booking(booking_id, data):
    """แก้ไข การจอง ตาม booking_id"""
    sql = """
        UPDATE booking
        SET member_id = %s, class_id = %s, book_date = %s, status = %s
        WHERE booking_id = %s
    """
    params = (
        data.get("member_id"),
        data.get("class_id"),
        data.get("book_date"),
        data.get("status"),
        booking_id
    )
    return run_command(sql, params)


def delete_booking(booking_id):
    """ลบ การจอง ตาม booking_id"""
    sql = "DELETE FROM booking WHERE booking_id = %s"
    return run_command(sql, (booking_id,))


# ============================================================
#  REPORT (รายงาน — ใช้ JOIN + GROUP BY + subquery)
# ============================================================
def report_summary():
    """ตัวเลขสรุปบนการ์ด dashboard — คืน dict เช่น {"members": 10, ...}"""
    members = run_query("SELECT COUNT(*) AS total FROM member")[0]["total"]
    classes = run_query("SELECT COUNT(*) AS total FROM gym_class")[0]["total"]
    bookings = run_query("SELECT COUNT(*) AS total FROM booking")[0]["total"]
    trainers = run_query("SELECT COUNT(*) AS total FROM trainer")[0]["total"]
    return {
        "members": members,
        "classes": classes,
        "bookings": bookings,
        "trainers": trainers
    }


def report_popular_classes():
    """📈 คลาสยอดนิยม (Most Booked)"""
    sql = """
        SELECT 
            c.class_id,
            c.name AS class_name,
            COUNT(b.booking_id) AS total_bookings
        FROM gym_class c
        INNER JOIN booking b ON c.class_id = b.class_id
        GROUP BY c.class_id, c.name
        ORDER BY total_bookings DESC
        LIMIT 5
    """
    return run_query(sql)


def report_trainers_above_avg():
    """🏅 เทรนเนอร์ที่มีผู้จองมากกว่าค่าเฉลี่ย (Above Average)"""
    sql = """
        SELECT 
            t.trainer_id,
            t.name AS trainer_name,
            COUNT(b.booking_id) AS total_bookings
        FROM trainer t
        INNER JOIN gym_class c ON t.trainer_id = c.trainer_id
        INNER JOIN booking b ON c.class_id = b.class_id
        GROUP BY t.trainer_id, t.name
        HAVING COUNT(b.booking_id) > (
            SELECT AVG(booking_count)
            FROM (
                SELECT COUNT(b2.booking_id) AS booking_count
                FROM trainer t2
                INNER JOIN gym_class c2 ON t2.trainer_id = c2.trainer_id
                INNER JOIN booking b2 ON c2.class_id = b2.class_id
                GROUP BY t2.trainer_id
            ) AS sub
        )
        ORDER BY total_bookings DESC
    """
    return run_query(sql)


def report_class_equipment():
    """🧰 อุปกรณ์ที่ใช้ในแต่ละคลาส (Join 3 Tables)"""
    sql = """
        SELECT 
            c.class_id,
            c.name AS class_name,
            e.equip_id,
            e.name AS equipment_name
        FROM class_equipment ce
        INNER JOIN gym_class c ON ce.class_id = c.class_id
        INNER JOIN equipment e ON ce.equip_id = e.equip_id
        ORDER BY c.class_id, e.equip_id
    """
    return run_query(sql)