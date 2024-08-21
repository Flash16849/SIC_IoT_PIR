from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

app = Flask(__name__)

# Cấu hình kết nối với cơ sở dữ liệu MySQL
DATABASE_URI = 'mysql+pymysql://root:147258@localhost/energy_management'
engine = create_engine(DATABASE_URI)
Base = declarative_base()

# Định nghĩa model tương ứng với bảng energy_usage_daily
class EnergyUsageDaily(Base):
    __tablename__ = 'energy_consumed'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    e_usage = Column(Float, nullable=False)

# Mô hình lưu trữ điện năng tiêu thụ hàng ngày
class DailyEnergyTotal(Base):
    __tablename__ = 'energy_usage_daily'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    e_usage_daily = Column(Float, nullable=False)

# Mô hình lưu trữ điện năng tiêu thụ hàng tuần
class WeeklyEnergyTotal(Base):
    __tablename__ = 'energy_usage_weekly'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    e_usage_weekly = Column(Float, nullable=False)

# Mô hình lưu trữ điện năng tiêu thụ hàng tháng
class MonthlyEnergyTotal(Base):
    __tablename__ = 'energy_usage_monthly'
    id = Column(Integer, primary_key=True)
    date = Column(Integer, nullable=False)
    e_usage_monthly = Column(Float, nullable=False)


# Tạo bảng nếu chưa có
Base.metadata.create_all(engine)

# Tạo session để tương tác với cơ sở dữ liệu
Session = sessionmaker(bind=engine)
session = Session()

#GET///////////////////////////////////////////////////////
@app.route('/get_daily_usage', methods=['GET'])
def get_daily_usage():
    try:
        # Lấy ngày từ query parameter
        date_str = request.args.get('date')
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

        # Truy vấn cơ sở dữ liệu để lấy dữ liệu của ngày đó
        records = session.query(EnergyUsageDaily).filter_by(date=date).all()

        # Chuyển đổi kết quả thành danh sách các dict
        data = [{'id': record.id, 'date': record.date.isoformat(), 'e_usage': record.e_usage} for record in records]

        return jsonify(data), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400
#GET///////////////////////////////////////////////////////END



#POST////////////////////////////////////////////////
# API để thêm dữ liệu điện năng tiêu thụ
@app.route('/update_usage', methods=['POST'])
def update_usage():
    data = request.json

    try:
        # Lấy dữ liệu từ JSON
        date_str = data.get('Ngày')
        e_usage = data.get('Điện năng tiêu thụ trong ngày')

        # Chuyển đổi ngày từ chuỗi thành đối tượng date
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

        # Tạo bản ghi mới
        new_record = EnergyUsageDaily(date=date, e_usage=e_usage)

        # Thêm bản ghi vào cơ sở dữ liệu
        session.add(new_record)
        session.commit()

        return jsonify({"status": "success", "message": "Dữ liệu đã được cập nhật"}), 200
    except Exception as e:
        session.rollback()  # Quay lại nếu có lỗi
        return jsonify({"status": "error", "message": str(e)}), 400
    

@app.route('/update_daily_total', methods=['POST'])
def update_daily_total():
    data = request.json

    try:
        date_str = data.get('Ngày')
        total_energy = data.get('Tổng điện năng')

        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

        # Tạo bản ghi mới hoặc cập nhật bản ghi hiện có
        record = session.query(DailyEnergyTotal).filter_by(date=date).first()
        if record:
            record.total_energy = total_energy
        else:
            new_record = DailyEnergyTotal(date=date, total_energy=total_energy)
            session.add(new_record)

        session.commit()

        return jsonify({"status": "success", "message": "Dữ liệu hàng ngày đã được lưu"}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 400


# @app.route('/update_weekly_total', methods=['POST'])
# def update_weekly_total():
#     data = request.json

#     try:
#         date_str = data.get('Ngày')
#         total_energy = data.get('Tổng điện năng')

#         date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

#         # Tạo bản ghi mới hoặc cập nhật bản ghi hiện có
#         record = session.query(WeeklyEnergyTotal).filter_by(date=date).first()
#         if record:
#             record.total_energy = total_energy
#         else:
#             new_record = WeeklyEnergyTotal(date=date, total_energy=total_energy)
#             session.add(new_record)

#         session.commit()

#         return jsonify({"status": "success", "message": "Dữ liệu hàng tuần đã được lưu"}), 200
#     except Exception as e:
#         session.rollback()
#         return jsonify({"status": "error", "message": str(e)}), 400


@app.route('/update_monthly_total', methods=['POST'])
def update_monthly_total():
    data = request.json

    try:
        date_str = data.get('Ngày')
        total_energy = data.get('Tổng điện năng')

        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").month

        # Tạo bản ghi mới hoặc cập nhật bản ghi hiện có
        record = session.query(MonthlyEnergyTotal).filter_by(date=date).first()
        if record:
            record.total_energy = total_energy
        else:
            new_record = MonthlyEnergyTotal(date=date, total_energy=total_energy)
            session.add(new_record)

        session.commit()

        return jsonify({"status": "success", "message": "Dữ liệu hàng tháng đã được lưu"}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 400
#POST////////////////////////////////////////////////END



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


