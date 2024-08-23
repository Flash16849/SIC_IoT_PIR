from flask import Flask, request, jsonify
import pymysql
import datetime

app = Flask(__name__)

# Hàm kết nối với cơ sở dữ liệu MySQL
def get_db_connection():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='147258',
        database='energy_management',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection


@app.route('/get_usage', methods=['GET'])
def get_usage():
    try:
        # Lấy ngày từ query parameter
        date_str = request.args.get('date')
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

        connection = get_db_connection()
        cursor = connection.cursor()

        # Truy vấn cơ sở dữ liệu để lấy dữ liệu của ngày đó
        sql = "SELECT * FROM energy_usage_daily WHERE date = %s"
        cursor.execute(sql, (date,))
        records = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify(records), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


# POST
@app.route('/update_usage', methods=['POST'])
def update_usage():
    data = request.json

    try:
        # Lấy dữ liệu từ JSON
        date_str = data.get('Ngày')
        e_usage = data.get('Điện năng tiêu thụ trong ngày')

        # Chuyển đổi ngày từ chuỗi thành đối tượng date
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

        connection = get_db_connection()
        cursor = connection.cursor()

        # Cập nhật hoặc chèn dữ liệu vào bảng energy_usage_daily
        sql = """
        INSERT INTO energy_usage_daily (date, e_usage_daily)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE e_usage_daily = e_usage_daily + VALUES(e_usage_daily)
        """
        cursor.execute(sql, (date, e_usage))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"status": "success", "message": "Dữ liệu đã được cập nhật"}), 200
    except Exception as e:
        connection.rollback()
        return jsonify({"status": "error", "message": str(e)}), 400
    

@app.route('/update_monthly_total', methods=['POST'])
def update_monthly_total():
    data = request.json

    try:
        date_str = data.get('Ngày')
        total_energy = data.get('Tổng điện năng')

        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").month

        connection = get_db_connection()
        cursor = connection.cursor()

        # Cập nhật hoặc chèn dữ liệu vào bảng energy_usage_monthly
        sql = """
        INSERT INTO energy_usage_monthly (date, e_usage_monthly)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE e_usage_monthly = e_usage_monthly + VALUES(e_usage_monthly)
        """
        cursor.execute(sql, (date, total_energy))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"status": "success", "message": "Dữ liệu hàng tháng đã được lưu"}), 200
    except Exception as e:
        connection.rollback()
        return jsonify({"status": "error", "message": str(e)}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
