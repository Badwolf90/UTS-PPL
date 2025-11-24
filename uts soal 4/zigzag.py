import time
import sys
import os

# FITUR 1: Weather System - animasi berubah sesuai cuaca (hujan, cerah, berawan)
# FITUR 2: Battery Saver Mode - otomatis kurangi frame rate saat sudah lama berjalan

indent = 0
indentIncreasing = True
weather_state = "sunny"
weather_duration = 0
start_time = time.time()
frame_count = 0

# Definisi cuaca
WEATHER_PATTERNS = {
    "sunny": {"char": "☀", "speed": 0.08, "color": "\033[93m"},  # Kuning
    "rainy": {"char": "🌧", "speed": 0.15, "color": "\033[94m"},  # Biru
    "cloudy": {"char": "☁", "speed": 0.12, "color": "\033[97m"}, # Putih
    "stormy": {"char": "⚡", "speed": 0.05, "color": "\033[95m"}  # Ungu
}

def change_weather():
    """Ganti cuaca secara acak setiap 15 detik"""
    import random
    weathers = ["sunny", "rainy", "cloudy", "stormy"]
    new_weather = random.choice(weathers)
    return new_weather

def get_weather_background(weather, width=50):
    """Buat latar belakang sesuai cuaca"""
    import random
    bg = [' '] * width
    
    if weather == "rainy":
        # Hujan - garis vertikal acak
        for i in range(0, width, 3):
            if random.random() > 0.5:
                bg[i] = '|'
    elif weather == "cloudy":
        # Berawan - titik-titik
        for i in range(0, width, 5):
            if random.random() > 0.6:
                bg[i] = '·'
    elif weather == "stormy":
        # Badai - garis miring
        for i in range(0, width, 4):
            if random.random() > 0.7:
                bg[i] = '/'
    
    return ''.join(bg)

def get_battery_mode(runtime_minutes):
    """Tentukan mode berdasarkan lama program berjalan"""
    if runtime_minutes < 2:
        return "high_performance", 1.0
    elif runtime_minutes < 5:
        return "balanced", 1.5
    else:
        return "battery_saver", 2.5

def clear_screen():
    """Clear terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

try:
    print("=== ZIGZAG WEATHER SYSTEM ===")
    print("🌤  Cuaca akan berubah otomatis!")
    print("🔋 Battery saver aktif setelah 5 menit\n")
    time.sleep(2)
    
    while True:
        # Hitung runtime
        runtime = time.time() - start_time
        runtime_minutes = runtime / 60
        
        # Battery saver mode
        battery_mode, speed_multiplier = get_battery_mode(runtime_minutes)
        
        # Ganti cuaca setiap 15 detik
        if weather_duration >= 15:
            weather_state = change_weather()
            weather_duration = 0
            clear_screen()
            weather_info = WEATHER_PATTERNS[weather_state]
            print(f"\n🌈 Cuaca berubah menjadi: {weather_state.upper()} {weather_info['char']}")
            print(f"⚡ Mode: {battery_mode.replace('_', ' ').title()}\n")
        
        # Ambil data cuaca
        weather_info = WEATHER_PATTERNS[weather_state]
        color = weather_info["color"]
        char = weather_info["char"]
        base_speed = weather_info["speed"]
        
        # Background cuaca
        background = get_weather_background(weather_state)
        
        # Tampilkan frame
        spaces = ' ' * indent
        print(f"{background[:indent]}{color}{char * 8}\033[0m{background[indent+8:]}")
        
        # Delay dengan weather speed dan battery multiplier
        actual_speed = base_speed * speed_multiplier
        time.sleep(actual_speed)
        
        # Update indent
        if indentIncreasing:
            indent += 1
            if indent == 20:
                indentIncreasing = False
        else:
            indent -= 1
            if indent == 0:
                indentIncreasing = True
        
        # Update counters
        frame_count += 1
        weather_duration += actual_speed
        
        # Status setiap 30 frame
        if frame_count % 30 == 0:
            print(f"\n📊 Runtime: {int(runtime_minutes)}m {int(runtime % 60)}s | Weather: {weather_state} | Mode: {battery_mode}")
            print(f"🎬 Frames: {frame_count} | Speed: {actual_speed:.2f}s\n")

except KeyboardInterrupt:
    runtime = time.time() - start_time
    print(f"\n\n=== SESSION COMPLETE ===")
    print(f"⏱  Total runtime: {int(runtime/60)}m {int(runtime%60)}s")
    print(f"🎬 Total frames: {frame_count}")
    print(f"🌦  Final weather: {weather_state}")
    sys.exit()