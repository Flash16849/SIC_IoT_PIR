from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import datetime
import asyncio
import websockets
import traceback

app = Flask(__name__)
CORS(app)  # Bật CORS cho toàn bộ API

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




# Lấy điện năng tiêu thụ theo ngày
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

#Lấy 10 ngày điện năng tiêu thụ để đưa lên biểu đồ frontend
@app.route('/get_e_date', methods=['GET'])
def get_e_date():
    try:

        connection = get_db_connection()
        cursor = connection.cursor()

        # Truy vấn cơ sở dữ liệu để lấy dữ liệu của ngày đó
        sql = """SELECT date, e_usage_daily FROM energy_usage_daily
        WHERE date >= CURDATE() - INTERVAL 10 DAY ORDER BY date ASC;
        """

        cursor.execute(sql)
        records = cursor.fetchall()
        print(records)

        cursor.close()
        connection.close()

        # Chuyển đổi kết quả thành định dạng JSON
        result = [{"date": record['date'].strftime("%Y-%m-%d"), "e_usage_daily": record['e_usage_daily']} for record in records]

        return jsonify(result), 200
    except Exception as e:
        print(f"Error: {e}")  # Log lỗi vào console
        traceback.print_exc()  # In chi tiết lỗi ra console
        return jsonify({"status": "error", "message": str(e)}), 400


# POST
@app.route('/update_usage', methods=['POST'])
def update_usage():
    data = request.json

    try:
        # Lấy dữ liệu từ JSON
        date = data.get('Ngày')
        e_usage = data.get('Điện năng tiêu thụ trong ngày')

        # Chuyển đổi ngày từ chuỗi thành đối tượng date
        

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

        month = datetime.datetime.strptime(date_str, "%Y-%m-%d").month

        connection = get_db_connection()
        cursor = connection.cursor()

        # Cập nhật hoặc chèn dữ liệu vào bảng energy_usage_monthly
        sql = """
        INSERT INTO energy_usage_monthly (month, e_usage_monthly)
        VALUES (%s, %s)
        """
        cursor.execute(sql, (month, total_energy))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"status": "success", "message": "Dữ liệu hàng tháng đã được lưu"}), 200
    except Exception as e:
        connection.rollback()
        return jsonify({"status": "error", "message": str(e)}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
