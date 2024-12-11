#LED, 아두이노 조도센서, 인체감지 센서 동작코드
import RPi.GPIO as GPIO
import time

# 핀 번호 설정 (BCM 모드 사용)
GPIO.setmode(GPIO.BCM)

# 핀 번호 정의
LDR_PIN = 18         # 조도 센서 연결 핀 (아날로그 센서를 MCP3008 등으로 변환 필요)
LED_PIN = 23         # LED 연결 핀
PIR_PIN = 24         # HC-SR501 연결 핀

# 핀 모드 설정
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(PIR_PIN, GPIO.IN)

def read_ldr(pin):
    """조도 센서 값 읽기 (간이 디지털 방식)"""
    count = 0
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)
    time.sleep(0.1)  # 방전 대기

    GPIO.setup(pin, GPIO.IN)
    # 센서의 충전 시간 측정
    while (GPIO.input(pin) == GPIO.LOW):
        count += 1
    return count

def main():
    try:
        print("시작 중...")
        while True:
            # PIR 센서 확인
            pir_state = GPIO.input(PIR_PIN)
            if pir_state:
                print("[PIR] 움직임 감지!")
            else:
                print("[PIR] 움직임 없음")

            # 조도 센서 값 확인
            ldr_value = read_ldr(LDR_PIN)
            print(f"[LDR] 조도 값: {ldr_value}")

            # LED 제어 (조도 값 기준)
            if ldr_value > 1000:  # 값은 환경에 따라 조정 필요
                GPIO.output(LED_PIN, GPIO.HIGH)
                print("[LED] 켜짐")
            else:
                GPIO.output(LED_PIN, GPIO.LOW)
                print("[LED] 꺼짐")

            time.sleep(1)

    except KeyboardInterrupt:
        print("프로그램 종료 중...")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
