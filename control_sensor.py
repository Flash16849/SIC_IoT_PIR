import RPi.GPIO as GPIO
import time
import datetime
import BlynkLib
import requests
# import asyncio
# import websockets



blynk = BlynkLib.Blynk("B8W1d5gvQKvi1Lve-ZRiRtoWRmlZBJLI")

# Thiết lập chân GPIO
LED_PIN = 17  # GPIO của LED
PIR_PIN = 18  # GPIO của cảm biến PIR

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)

# Thiết lập PWM trên GPIO17 với tần số 100Hz
pwm = GPIO.PWM(LED_PIN, 100)
pwm.start(0)  # Bắt đầu PWM với độ sáng 0%




pirEnabled = True  # Mặc định PIR được bật
ledBlynk = False   # Mặc định Blynk không hoạt động
ledFrontend = False

def motion_detected():
    E = 0

    if GPIO.input(PIR_PIN):
        print("Chuyển động phát hiện!")
        pwm.ChangeDutyCycle(70)
        time.sleep(5)
        E = (1.5 * 0.7) * 5
        call_API(E)
    else:
        pwm.ChangeDutyCycle(0)
            

startTime = 0
endTime = 0
changeTime = 0
brightLevel = 0

@blynk.on("V1")
def blynk_controlled(value):
    global pirEnabled
    global ledBlynk
    global ledFrontend

    global startTime
    global endTime
    global changeTime
    global brightLevel
    E = 0

    if int(value[0]) != 0:  # Blynk bật đèn
        startTime = time.time()
        brightLevel = 0.7

        ledBlynk = True
        pirEnabled = False  # Tắt PIR khi Blynk điều khiển đèn
        ledFrontend = False
        pwm.ChangeDutyCycle(70)

    else:  # Blynk tắt đèn
        endTime = time.time()
        duration = endTime - startTime
        P = 1.5 * brightLevel
        E = P * duration
        call_API(E)
        ledBlynk = False
        pwm.ChangeDutyCycle(0)
        pirEnabled = True  # Bật lại PIR khi Blynk không điều khiển


@blynk.on("V2")
def brightness_controlled(value):
    global ledBlynk
    global changeTime
    global brightLevel
    E = 0

    if ledBlynk is not False:  # Blynk bật đèn
        changeTime = time.time()
        pwm.ChangeDutyCycle(int(value[0]))
        duration = changeTime - startTime
        P = 1.5 * brightLevel
        E = P * duration
        call_API(E)
        startTime = changeTime
        brightLevel = int(value[0])
        


# # async def control_led(websocket, path):
# #     async for message in websocket:
# #         data = message.split(',')
# #         action = data[0]
# #         if action == 'on' and pirEnabled is not True:
# #             brightness = int(data[1])
# #             pwm.ChangeDutyCycle(brightness)
# #             print(f"Đèn được bật với độ sáng: {brightness}%")
# #         elif action == 'off':
# #             pwm.ChangeDutyCycle(0)
# #             print("Đèn đã tắt")

# # # Khởi động WebSocket server
# # start_server = websockets.serve(control_led, '0.0.0.0', 6789)

# # asyncio.get_event_loop().run_until_complete(start_server)
# # asyncio.get_event_loop().run_forever()


try:
    now = datetime.datetime.now()
    while True:
        if pirEnabled and ledFrontend is not True:
            motion_detected()
        blynk.run()
        # asyncio.get_event_loop().run_forever()
        time.sleep(0.5)
        
except KeyboardInterrupt:
    print("Kết thúc chương trình.")
finally:
    pwm.stop()  # Dừng PWM
    GPIO.cleanup()  # Đảm bảo GPIO được dọn dẹp khi kết thúc chương trình


# Gửi dữ liệu tới API Flask
def call_API(E):
    response = requests.post('http://localhost:5000/update_usage', 
            json={'Ngày': datetime.datetime.now().date().isoformat(), 'Điện năng tiêu thụ trong ngày': E})

    print(response.json())



# # if x is not '12:00:00':
# # 	print("correct")


# import requests
# import datetime

# E = 500.0  # Giả sử đây là điện năng tiêu thụ được tính toán

