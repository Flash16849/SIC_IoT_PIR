import requests
import datetime

# URL của API Flask để lấy dữ liệu từ cơ sở dữ liệu
BASE_URL = 'http://localhost:5000'

def get_energy_consumption(date):
    #Lấy dữ liệu điện năng tiêu thụ cho một ngày cụ thể.
    response = requests.get(f'{BASE_URL}/get_daily_usage', params={'date': date})
    if response.status_code == 200:
        data = response.json()
        total_energy = sum([record['e_usage'] for record in data])
        total_energy /= 3600
        return round(total_energy, 2)
    else:
        print(f"Error fetching data for {date}: {response.json().get('message')}")
        return 0

def calculate_daily_energy():
    #Tính toán điện năng tiêu thụ cho ngày hôm qua.
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).date().isoformat()
    total_energy = get_energy_consumption(yesterday)
    
    # Gửi tổng năng lượng tiêu thụ lên bảng khác trong cơ sở dữ liệu
    response = requests.post(f'{BASE_URL}/update_daily_total', 
                             json={'Ngày': yesterday, 'Tổng điện năng': total_energy})
    
    if response.status_code == 200:
        print(f"Tổng điện năng tiêu thụ ngày {yesterday}: {total_energy} mWh")
    else:
        print(f"Error updating daily total: {response.json().get('message')}")

# def calculate_weekly_energy():
#     #Tính toán điện năng tiêu thụ cho tuần trước.
#     today = datetime.datetime.now().date()
#     start_of_week = (today - datetime.timedelta(days=today.weekday(), weeks=1)).isoformat()
#     end_of_week = (start_of_week + datetime.timedelta(days=6)).isoformat()

#     total_energy = 0
#     current_date = start_of_week

#     while current_date <= end_of_week:
#         total_energy += get_energy_consumption(current_date)
#         current_date = (datetime.datetime.strptime(current_date, "%Y-%m-%d").date() + datetime.timedelta(days=1)).isoformat()
    
#     # Gửi tổng năng lượng tiêu thụ tuần lên bảng khác trong cơ sở dữ liệu
#     response = requests.post(f'{BASE_URL}/update_weekly_total', 
#                              json={'Tuần bắt đầu': start_of_week, 'Tổng điện năng': total_energy})

#     if response.status_code == 200:
#         print(f"Tổng điện năng tiêu thụ tuần từ {start_of_week} đến {end_of_week}: {total_energy} Wh")
#     else:
#         print(f"Error updating weekly total: {response.json().get('message')}")

def calculate_monthly_energy():
    #Tính toán điện năng tiêu thụ cho tháng trước.
    today = datetime.datetime.now().date()
    first_day_of_month = (today.replace(day=1) - datetime.timedelta(days=1)).replace(day=1).isoformat()
    last_day_of_month = (today.replace(day=1) - datetime.timedelta(days=1)).isoformat()

    total_energy = 0
    current_date = first_day_of_month

    while current_date <= last_day_of_month:
        total_energy += get_energy_consumption(current_date)
        current_date = (datetime.datetime.strptime(current_date, "%Y-%m-%d").date() + datetime.timedelta(days=1)).isoformat()
    
    # Gửi tổng năng lượng tiêu thụ tháng lên bảng khác trong cơ sở dữ liệu
    response = requests.post(f'{BASE_URL}/update_monthly_total', 
                             json={'Ngày': first_day_of_month, 'Tổng điện năng': total_energy})

    if response.status_code == 200:
        print(f"Tổng điện năng tiêu thụ tháng từ {first_day_of_month} đến {last_day_of_month}: {total_energy} Wh")
    else:
        print(f"Error updating monthly total: {response.json().get('message')}")

if __name__ == "__main__":
    calculate_daily_energy()
    # calculate_weekly_energy()
    calculate_monthly_energy()
