import smbus2
import time
import RPi.GPIO as GPIO

# I2C 주소 (GY-302는 기본적으로 0x23 주소를 사용)
I2C_ADDRESS = 0x23

# 라즈베리파이에서 사용할 GPIO 핀 설정
LED_PIN = 18

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# I2C 버스 설정
bus = smbus2.SMBus(1)  # 1번 I2C 버스를 사용

# GY-302(BH1750) 센서에서 데이터 읽기 함수
def read_light():
    # 센서에 'One-time High-Resolution Mode' 명령 보내기
    bus.write_byte(I2C_ADDRESS, 0x10)
    time.sleep(0.2)  # 데이터가 준비되기를 기다리기
    data = bus.read_i2c_block_data(I2C_ADDRESS, 0, 2)
    
    # 조도 값 계산
    light_level = (data[0] << 8) + data[1]
    return light_level

# LED 밝기 조절 함수 (PWM 사용)
def set_led_brightness(brightness):
    pwm = GPIO.PWM(LED_PIN, 1000)  # 1kHz 주파수로 PWM 설정
    pwm.start(0)  # 초기 값 0% (꺼짐)
    
    # 조도 값에 따라 LED 밝기 설정 (0-1023의 범위를 0-100%로 변환)
    duty_cycle = (brightness / 1023) * 100
    pwm.ChangeDutyCycle(duty_cycle)
    
    return pwm

# 메인 코드
try:
    while True:
        light = read_light()  # GY-302 센서로부터 조도 값 읽기
        print(f"now JODO value: {light} lx")
        
        # LED 밝기 조절
        pwm = set_led_brightness(light)
        
        # 1초마다 값을 갱신
        time.sleep(1)
        
except KeyboardInterrupt:
    print("end")
    
finally:
    GPIO.cleanup()  # GPIO 리소스 정리
