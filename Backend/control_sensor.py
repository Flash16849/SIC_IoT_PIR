import RPi.GPIO as GPIO
import time
import datetime
import BlynkLib
import requests
import smbus



blynk = BlynkLib.Blynk("B8W1d5gvQKvi1Lve-ZRiRtoWRmlZBJLI")

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
        GPIO.output(RELAY_PIN, GPIO.HIGH)
        print("Đèn bật")
        time.sleep(5)
        # 0.0013888889 là 5s đổi sang giờ
        E = 9 * 0.0038888189
        call_API(E)
        GPIO.output(RELAY_PIN, GPIO.LOW)
        


def read_light():
    data = bus.read_i2c_block_data(BH1750_ADDRESS, BH1750_CONTINUOUS_HIGH_RES_MODE, 2)
    light_level = (data[0] << 8) | data[1]  # Kết hợp hai byte thành một giá trị
    return light_level / 1.2  # Chuyển đổi giá trị thành lux
            

startTime = 0
endTime = 0

@blynk.on("V1")
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
        duration = (endTime - startTime) * 0.0002777778
        E = 9 * duration
        call_API(E)
        ledBlynk = False
        GPIO.output(RELAY_PIN, GPIO.LOW)
        pirEnabled = True  # Bật lại PIR khi Blynk không điều khiển

        


# Gửi dữ liệu tới API Flask
def call_API(E):
    response = requests.post('http://localhost:5000/update_usage', 
            json={'Ngày': datetime.datetime.now().date().isoformat(), 'Điện năng tiêu thụ trong ngày': E})

    print(response.json())

try:
    while True:
        light_level = read_light()

        if light_level < 20 and pirEnabled:
            motion_detected()
        blynk.run()
        time.sleep(1)
    
        
except KeyboardInterrupt:
    print("Kết thúc chương trình.")
finally:
    GPIO.cleanup()  # Đảm bảo GPIO được dọn dẹp khi kết thúc chương trình






# # if x is not '12:00:00':
# # 	print("correct")


# import requests
# import datetime

# E = 500.0  # Giả sử đây là điện năng tiêu thụ được tính toán

