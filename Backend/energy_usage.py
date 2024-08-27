import datetime
import firebase_admin
from firebase_admin import credentials, db


# file này được dùng để tính toán điện năng tiêu thụ mỗi tháng, đặt lịch chạy tự động mỗi đầu tháng bằng cron job
# Khởi tạo Firebase
cred = credentials.Certificate("/home/namqu/Desktop/project/Backend/sic-iot-ab9de-firebase-adminsdk-jhrmc-451e31a7b4.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sic-iot-ab9de-default-rtdb.asia-southeast1.firebasedatabase.app'
})

def get_daily_energy(date):
    ref = db.reference(f'energy_usage/{date}')
    data = ref.get()

    if data:
        return data.get('total_energy_consumed', 0)
    return 0

def calculate_monthly_energy():
    today = datetime.datetime.now().date()
    first_day_of_month = (today.replace(day=1) - datetime.timedelta(days=1)).replace(day=1)
    last_day_of_month = (today.replace(day=1) - datetime.timedelta(days=1))

    total_energy = 0
    current_date = first_day_of_month

    while current_date <= last_day_of_month:
        date_str = current_date.isoformat()
        total_energy += get_daily_energy(date_str)
        current_date += datetime.timedelta(days=1)

    # Đẩy tổng điện năng tiêu thụ tháng lên Firebase
    monthly_ref = db.reference(f'monthly_energy_usage/{first_day_of_month.year}/{first_day_of_month.month}')
    monthly_ref.set({
        'total_energy_consumed': total_energy,
        'month': f"{first_day_of_month.year}-{first_day_of_month.month}"
    })

    print(f"Tổng điện năng tiêu thụ từ {first_day_of_month} đến {last_day_of_month}: {total_energy} Wh")

if __name__ == "__main__":
    calculate_monthly_energy()
