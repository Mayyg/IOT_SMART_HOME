:: arg: Name Units Place UpdateTime

start "DHT" python DHT.py
timeout 3
start "Buttons" python Buttons.py
timeout 3
start "Unit" python Unit.py
timeout 3