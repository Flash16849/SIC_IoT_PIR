import time
import datetime
import smbus
import RPi.GPIO as GPIO
import firebase_admin
from firebase_admin import credentials, db
import BlynkLib


cred = credentials.Certificate("/home/namqu/Desktop/project/Backend/sic-iot-ab9de-firebase-adminsdk-jhrmc-451e31a7b4.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sic-iot-ab9de-default-rtdb.asia-southeast1.firebasedatabase.app'
})



blynk = BlynkLib.Blynk('azfeon74f5YOhQ6nveu6x-H684Yg9NkL')

# Địa chỉ I2C của BH1750
BH1750_ADDRESS = 0x23

# Lệnh đo ánh sáng liên tục ở độ phân giải cao
BH1750_CONTINUOUS_HIGH_RES_MODE = 0x10

# Thiết lập I2C
bus = smbus.SMBus(1)

# Thiết lập chân GPIO cho relay
RELAY_PIN = 16  # Chọn chân GPIO mà bạn đã kết nối với chân IN của relay

# Thiết lập chân GPIO
PIR_PIN = 18  # GPIO của cảm biến PIR

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(RELAY_PIN, GPIO.OUT)



pirEnabled = True  # Mặc định PIR được bật
ledBlynk = False   # Mặc định Blynk không hoạt động


def motion_detected():
    E = 0

    if GPIO.input(PIR_PIN):
        print("Chuyển động phát hiện!")
        print("Đèn bật")
        GPIO.output(RELAY_PIN, GPIO.HIGH)
        time.sleep(5)
        GPIO.output(RELAY_PIN, GPIO.LOW)
        # 0.0013888889 là 5s đổi sang giờ
        E = 9 * 0.0038888189
        call_firebase(E)

    else:
        GPIO.output(RELAY_PIN, GPIO.LOW)
        


def read_light():
    data = bus.read_i2c_block_data(BH1750_ADDRESS, BH1750_CONTINUOUS_HIGH_RES_MODE, 2)
    light_level = (data[0] << 8) | data[1]  # Kết hợp hai byte thành một giá trị
    return light_level / 1.2  # Chuyển đổi giá trị thành lux
            

startTime = 0
endTime = 0

@blynk.on('V1')
def blynk_controlled(value):
    global pirEnabled
    global ledBlynk

    global startTime
    global endTime
    E = 0

    if int(value[0]) != 0:  # Blynk bật đèn
        startTime = time.time()

        ledBlynk = True
        pirEnabled = False  # Tắt PIR khi Blynk điều khiển đèn
        GPIO.output(RELAY_PIN, GPIO.HIGH)

    else:  # Blynk tắt đèn
        endTime = time.time()
        # 1s = 0.0002777778h và đèn có P = 9
        duration = (endTime - startTime) * 0.0002777778
        E = 9 * duration 
        call_firebase(E)
        ledBlynk = False
        GPIO.output(RELAY_PIN, GPIO.LOW)
        pirEnabled = True  # Bật lại PIR khi Blynk không điều khiển

        


def call_firebase(E):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    ref = db.reference(f'energy_usage/{today}')
    
    def update_transaction(current_data):
        if current_data is None:
            return {
                'total_energy_consumed': E,
                'last_updated': int(datetime.datetime.now().timestamp())
            }
        else:
            current_data['total_energy_consumed'] += E
            current_data['last_updated'] = int(datetime.datetime.now().timestamp())
            return current_data
    
    ref.transaction(update_transaction)
    print(f"Đã cập nhật {E} Wh lên Firebase.")


try:
    while True:
        light_level = read_light()
        print(light_level)
        if light_level < 20 and pirEnabled:
            motion_detected()
        blynk.run()
        time.sleep(0.5)

    
        
except KeyboardInterrupt:
    print("Kết thúc chương trình.")
finally:
    GPIO.cleanup()  # Đảm bảo GPIO được dọn dẹp khi kết thúc chương trình