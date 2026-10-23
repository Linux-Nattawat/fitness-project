# ============================================================
#  app.py — เว็บแอป Flask (ทำให้เสร็จแล้ว ★ ไม่ต้องแก้)
#  รัน:  python app.py  แล้วเปิด http://127.0.0.1:5000
# ============================================================
from flask import Flask, request, jsonify, render_template
from mysql.connector import IntegrityError
import db

app = Flask(__name__)


def safe(fn, *args, **kwargs):
    try:
        return jsonify({
            "ok": True,
            "data": fn(*args, **kwargs)
        })

    except ValueError as e:
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 400

    except LookupError as e:
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 404

    except IntegrityError as e:
        if e.errno == 1452:
            message = (
                "ไม่พบรหัสอ้างอิง "
                "กรุณาตรวจสอบรหัสสมาชิกหรือรหัสคลาส"
            )
        elif e.errno == 1062:
            message = "มีข้อมูลซ้ำกับรายการเดิม"
        else:
            message = "ข้อมูลขัดกับเงื่อนไขของฐานข้อมูล"

        return jsonify({
            "ok": False,
            "error": message
        }), 400

    except NotImplementedError as e:
        return jsonify({
            "ok": False,
            "todo": True,
            "error": str(e)
        }), 501

    except Exception:
        app.logger.exception("API error")

        return jsonify({
            "ok": False,
            "error": (
                "เกิดข้อผิดพลาด "
                "กรุณาดูรายละเอียดในหน้าต่างที่รัน Python"
            )
        }), 500


@app.route("/")
def page_home():
    return render_template("index.html")

@app.route("/report")
def page_report():
    return render_template("report.html")


# ---- สมาชิก ----
@app.route("/api/members", methods=["GET"])
def members_list():
    filters = {k: v for k, v in request.args.items() if v}
    return safe(db.search_members, filters)

@app.route("/api/members/<int:_id>", methods=["GET"])
def member_get(_id):
    return safe(db.get_member, _id)

@app.route("/api/members", methods=["POST"])
def member_create():
    return safe(db.create_member, request.json)

@app.route("/api/members/<int:_id>", methods=["PUT"])
def member_update(_id):
    return safe(db.update_member, _id, request.json)

@app.route("/api/members/<int:_id>", methods=["DELETE"])
def member_delete(_id):
    return safe(db.delete_member, _id)

# ---- คลาสเรียน ----
@app.route("/api/classes", methods=["GET"])
def classes_list():
    filters = {k: v for k, v in request.args.items() if v}
    return safe(db.search_classes, filters)

@app.route("/api/classes/<int:_id>", methods=["GET"])
def class_get(_id):
    return safe(db.get_class, _id)

@app.route("/api/classes", methods=["POST"])
def class_create():
    return safe(db.create_class, request.json)

@app.route("/api/classes/<int:_id>", methods=["PUT"])
def class_update(_id):
    return safe(db.update_class, _id, request.json)

@app.route("/api/classes/<int:_id>", methods=["DELETE"])
def class_delete(_id):
    return safe(db.delete_class, _id)

# ---- การจอง ----
@app.route("/api/bookings", methods=["GET"])
def bookings_list():
    filters = {k: v for k, v in request.args.items() if v}
    return safe(db.search_bookings, filters)

@app.route("/api/bookings/<int:_id>", methods=["GET"])
def booking_get(_id):
    return safe(db.get_booking, _id)

@app.route("/api/bookings", methods=["POST"])
def booking_create():
    return safe(db.create_booking, request.json)

@app.route("/api/bookings/<int:_id>", methods=["PUT"])
def booking_update(_id):
    return safe(db.update_booking, _id, request.json)

@app.route("/api/bookings/<int:_id>", methods=["DELETE"])
def booking_delete(_id):
    return safe(db.delete_booking, _id)


@app.route("/api/reports/summary")
def report_summary():
    return safe(db.report_summary)

@app.route("/api/reports/popular-classes")
def route_report_popular_classes():
    return safe(db.report_popular_classes)

@app.route("/api/reports/top-trainers")
def route_report_trainers_above_avg():
    return safe(db.report_trainers_above_avg)

@app.route("/api/reports/class-equipment")
def route_report_class_equipment():
    return safe(db.report_class_equipment)

# ---- รีวิว ----
@app.route("/api/reviews", methods=["GET"])
def reviews_list():
    return safe(db.search_reviews, request.args.to_dict())

@app.route("/api/reviews/<int:_id>", methods=["GET"])
def review_get(_id):
    return safe(db.get_review, _id)

@app.route("/api/reviews", methods=["POST"])
def review_create():
    return safe(
        db.create_review,
        request.get_json(silent=True)
    )

@app.route("/api/reviews/<int:_id>", methods=["PUT"])
def review_update(_id):
    return safe(
        db.update_review,
        _id,
        request.get_json(silent=True)
    )

@app.route("/api/reviews/<int:_id>", methods=["DELETE"])
def review_delete(_id):
    return safe(db.delete_review, _id)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
