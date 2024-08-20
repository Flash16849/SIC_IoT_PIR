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
    __tablename__ = 'energy_usage_daily'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    energy_usage = Column(Float, nullable=False)

# Tạo bảng nếu chưa có
Base.metadata.create_all(engine)

# Tạo session để tương tác với cơ sở dữ liệu
Session = sessionmaker(bind=engine)
session = Session()

# API để thêm dữ liệu điện năng tiêu thụ hàng ngày
@app.route('/update_usage', methods=['POST'])
def update_usage():
    data = request.json

    try:
        # Lấy dữ liệu từ JSON
        date_str = data.get('Ngày')
        energy_usage = data.get('Điện năng tiêu thụ trong ngày')

        # Chuyển đổi ngày từ chuỗi thành đối tượng date
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

        # Tạo bản ghi mới
        new_record = EnergyUsageDaily(date=date, energy_usage=energy_usage)

        # Thêm bản ghi vào cơ sở dữ liệu
        session.add(new_record)
        session.commit()

        return jsonify({"status": "success", "message": "Dữ liệu đã được cập nhật"}), 200
    except Exception as e:
        session.rollback()  # Quay lại nếu có lỗi
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


