import time

try:
    var = True
    while var:
        print("Test")
        time.sleep(1)
    print("end")

except KeyboardInterrupt:
    var = False