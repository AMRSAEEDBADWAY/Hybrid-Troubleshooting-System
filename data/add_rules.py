
import json
import os

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

def add_computer_rules():
    new_rules = [
        # Overheating extension
        {
            "id": "COMP_HEAT_006",
            "category": "overheating",
            "conditions": {"device": "computer", "gpu_hot": true, "gaming": true},
            "cause": "GPU overheating under load",
            "solutions": ["Adjust GPU fan curve", "Clean GPU heatsink", "Reduce game graphics settings"],
            "confidence": 0.85
        },
        {
            "id": "COMP_HEAT_007",
            "category": "overheating",
            "conditions": {"device": "computer", "laptop_bottom_hot": true},
            "cause": "Blocked laptop intake vents",
            "solutions": ["Use laptop on hard surface", "Clean bottom vents", "Use cooling pad"],
            "confidence": 0.88
        },
        # Slow performance extension
        {
            "id": "COMP_SLOW_007",
            "category": "slow_performance",
            "conditions": {"device": "computer", "slow_boot": true, "hdd_old": true},
            "cause": "Aging mechanical hard drive",
            "solutions": ["Disable startup apps", "Replace HDD with SSD", "Check HDD health"],
            "confidence": 0.82
        },
        {
            "id": "COMP_SLOW_008",
            "category": "slow_performance",
            "conditions": {"device": "computer", "typing_delay": true},
            "cause": "High CPU usage or keylogger",
            "solutions": ["Check Task Manager for CPU hogs", "Scan for malware", "Update keyboard drivers"],
            "confidence": 0.75
        },
        {
            "id": "COMP_SLOW_009",
            "category": "slow_performance",
            "conditions": {"device": "computer", "browser_slow": true},
            "cause": "Too many browser tabs/extensions",
            "solutions": ["Close unused tabs", "Disable unused extensions", "Clear browser cache"],
            "confidence": 0.90
        },
        # Network extension
        {
            "id": "COMP_NET_007",
            "category": "network_issues",
            "conditions": {"device": "computer", "vpn_connected": true, "no_internet": true},
            "cause": "VPN connection issue",
            "solutions": ["Disconnect VPN", "Check VPN server status", "Reinstall VPN client"],
            "confidence": 0.85
        },
        {
            "id": "COMP_NET_008",
            "category": "network_issues",
            "conditions": {"device": "computer", "weak_wifi_signal": true},
            "cause": "Distance from router or interference",
            "solutions": ["Move closer to router", "Use 5GHz band if close, 2.4GHz if far", "Install WiFi extender"],
            "confidence": 0.80
        },
        {
            "id": "COMP_NET_009",
            "category": "network_issues",
            "conditions": {"device": "computer", "slow_download": true},
            "cause": "Bandwidth saturation",
            "solutions": ["Stop other downloads", "Check router QoS settings", "Run speed test"],
            "confidence": 0.78
        },
        # Audio extension
        {
            "id": "COMP_AUDIO_006",
            "category": "audio_problems",
            "conditions": {"device": "computer", "sound_distorted": true, "high_volume": true},
            "cause": "Speaker clipping or damage",
            "solutions": ["Lower volume", "Adjust equalizer settings", "Test with headphones to isolate issue"],
            "confidence": 0.80
        },
        {
            "id": "COMP_AUDIO_007",
            "category": "audio_problems",
            "conditions": {"device": "computer", "hdmi_no_sound": true},
            "cause": "Wrong audio output device (HDMI)",
            "solutions": ["Select HDMI/TV as playback device", "Update graphics drivers", "Check HDMI cable"],
            "confidence": 0.90
        },
        # Screen extension
        {
            "id": "COMP_SCREEN_006",
            "category": "screen_problems",
            "conditions": {"device": "computer", "blurry_text": true},
            "cause": "Incorrect DPI scaling or resolution",
            "solutions": ["Adjust display scaling", "Set resolution to 'Native'", "Use ClearType text tuner"],
            "confidence": 0.85
        },
        {
            "id": "COMP_SCREEN_007",
            "category": "screen_problems",
            "conditions": {"device": "computer", "screen_tearing": true, "games": true},
            "cause": "V-Sync disabled",
            "solutions": ["Enable V-Sync in game", "Limit FPS to monitor refresh rate", "Update GPU drivers"],
            "confidence": 0.88
        },
        # Storage extension
        {
            "id": "COMP_STORAGE_006",
            "category": "storage_issues",
            "conditions": {"device": "computer", "cannot_copy_file": true, "file_too_large": true},
            "cause": "FAT32 file system limitation",
            "solutions": ["Format drive to NTFS or exFAT", "Split file into smaller parts", "Use different drive"],
            "confidence": 0.95
        },
        {
            "id": "COMP_STORAGE_007",
            "category": "storage_issues",
            "conditions": {"device": "computer", "ssd_slow": true},
            "cause": "TRIM not enabled or drive full",
            "solutions": ["Enable TRIM", "Free up space (keep 10-20% free)", "Update firmware"],
            "confidence": 0.82
        },
        # Startup extension
        {
            "id": "COMP_START_006",
            "category": "startup_failure",
            "conditions": {"device": "computer", "windows_update_loop": true},
            "cause": "Corrupted Windows Update",
            "solutions": ["Boot safe mode", "Run Windows Update Troubleshooter", "Delete SoftwareDistribution folder"],
            "confidence": 0.88
        },
        {
            "id": "COMP_START_007",
            "category": "startup_failure",
            "conditions": {"device": "computer", "slow_boot_ssd": true},
            "cause": "Fast Startup bug or too many apps",
            "solutions": ["Disable Fast Startup", "Check startup apps", "Update chipset drivers"],
            "confidence": 0.75
        },
        # App extension
        {
            "id": "COMP_APP_005",
            "category": "app_crashes",
            "conditions": {"device": "computer", "dll_missing_error": true},
            "cause": "Missing Visual C++ Redistributable",
            "solutions": ["Install Visual C++ Redistributable All-in-One", "Reinstall program", "Run CFC /scannow"],
            "confidence": 0.92
        },
        {
            "id": "COMP_APP_006",
            "category": "app_crashes",
            "conditions": {"device": "computer", "office_crash": true},
            "cause": "Add-in conflict",
            "solutions": ["Start Office in Safe Mode", "Disable add-ins", "Repair Office installation"],
            "confidence": 0.85
        },
        # Battery extension
        {
            "id": "COMP_BATT_004",
            "category": "battery_issues",
            "conditions": {"device": "computer", "plugged_not_charging_high_pct": true},
            "cause": "Smart charging battery protection",
            "solutions": ["Check manufacturer battery settings", "This is normal feature to extend life", "Disable smart charging if 100% needed"],
            "confidence": 0.90
        },
        {
            "id": "COMP_BATT_005",
            "category": "battery_issues",
            "conditions": {"device": "computer", "battery_report_needed": true},
            "cause": "Diagnostic request",
            "solutions": ["Run 'powercfg /batteryreport'", "Check generated HTML report", "Check charge cycle count"],
            "confidence": 1.0
        },
        # Hardware extension
        {
            "id": "COMP_HW_006",
            "category": "hardware_failure",
            "conditions": {"device": "computer", "touchpad_not_working": true},
            "cause": "Touchpad disabled or driver issue",
            "solutions": ["Check function key toggle (Fn+F7 etc)", "Check settings", "Update drivers"],
            "confidence": 0.88
        },
        {
            "id": "COMP_HW_007",
            "category": "hardware_failure",
            "conditions": {"device": "computer", "printer_not_found": true},
            "cause": "Printer connection or spooler",
            "solutions": ["Restart Print Spooler service", "Remove and re-add printer", "Check USB/Network connection"],
            "confidence": 0.82
        },
        {
            "id": "COMP_HW_008",
            "category": "hardware_failure",
            "conditions": {"device": "computer", "mouse_lag": true},
            "cause": "Interference or surface issue",
            "solutions": ["Use mousepad", "Move receiver closer", "Check mouse batteries"],
            "confidence": 0.80
        },
        {
            "id": "COMP_HW_009",
            "category": "hardware_failure",
            "conditions": {"device": "computer", "webcam_black": true},
            "cause": "Privacy shutter or permissions",
            "solutions": ["Open privacy shutter", "Check camera privacy settings", "Check antivirus blocking camera"],
            "confidence": 0.90
        },
        {
            "id": "COMP_HW_010",
            "category": "hardware_failure",
            "conditions": {"device": "computer", "coil_whine": true},
            "cause": "GPU/PSU electrical vibration",
            "solutions": ["Cap framerate (FPS)", "Change PSU (if severe)", "Normal phenomenon in high power GPUs"],
            "confidence": 0.85
        },
        {
            "id": "COMP_BSOD_004",
            "category": "hardware_failure",
            "conditions": {"device": "computer", "bsod_after_update": true},
            "cause": "Bad update",
            "solutions": ["Uninstall recent update", "System Restore", "Wait for patch"],
            "confidence": 0.85
        },
        {
            "id": "COMP_BSOD_005",
            "category": "hardware_failure",
            "conditions": {"device": "computer", "bsod_whea_uncorrectable": true},
            "cause": "Hardware error (CPU/Voltage)",
            "solutions": ["Reset BIOS/Overclocking", "Check CPU cooling", "Test hardware stability"],
            "confidence": 0.88
        },
        {
            "id": "COMP_SEC_001",
            "category": "security",
            "conditions": {"device": "computer", "ransomware": true},
            "cause": "Ransomware infection",
            "solutions": ["Disconnect internet immediately", "Do not pay ransom", "Restore from offline backup"],
            "confidence": 0.95
        },
        {
            "id": "COMP_SEC_002",
            "category": "security",
            "conditions": {"device": "computer", "popups_everywhere": true},
            "cause": "Adware infection",
            "solutions": ["Run AdwCleaner", "Reset browser settings", "Check installed programs"],
            "confidence": 0.90
        },
        {
            "id": "COMP_SEC_003",
            "category": "security",
            "conditions": {"device": "computer", "account_hacked": true},
            "cause": "Compromised credentials",
            "solutions": ["Change passwords immediately on another device", "Enable 2FA", "Scan for keyloggers"],
            "confidence": 0.95
        }
    ]
    return new_rules

def add_mobile_rules():
    new_rules = [
        # Battery
        {
            "id": "MOB_BATT_008",
            "category": "battery_issues",
            "conditions": {"device": "mobile", "battery_drops_suddenly": true},
            "cause": "Battery calibration needed or dead cell",
            "solutions": ["Calibrate battery (0-100% cycle)", "Replace battery", "Check voltage"],
            "confidence": 0.85
        },
        {
            "id": "MOB_BATT_009",
            "category": "battery_issues",
            "conditions": {"device": "mobile", "wireless_charging_fail": true},
            "cause": "Case too thick or misalignment",
            "solutions": ["Remove phone case", "Align center of phone with pad", "Check charger power"],
            "confidence": 0.88
        },
        # Overheating
        {
            "id": "MOB_HEAT_005",
            "category": "overheating",
            "conditions": {"device": "mobile", "camera_overheat": true},
            "cause": "Extended high-res video recording",
            "solutions": ["Stop recording", "Lower resolution/FPS", "Remove case"],
            "confidence": 0.90
        },
        {
            "id": "MOB_HEAT_006",
            "category": "overheating",
            "conditions": {"device": "mobile", "gps_nav_hot": true},
            "cause": "GPS + Screen + Data usage",
            "solutions": ["Place near AC vent", "Turn off screen when not looking", "Download offline maps"],
            "confidence": 0.85
        },
        # Slow
        {
            "id": "MOB_SLOW_006",
            "category": "slow_performance",
            "conditions": {"device": "mobile", "keyboard_lag": true},
            "cause": "Keyboard app cache or dictionary issue",
            "solutions": ["Clear keyboard app cache", "Reset keyboard dictionary", "Try different keyboard app"],
            "confidence": 0.80
        },
        {
            "id": "MOB_SLOW_007",
            "category": "slow_performance",
            "conditions": {"device": "mobile", "camera_lag": true},
            "cause": "Camera app or storage speed",
            "solutions": ["Save to internal storage not SD", "Clear camera cache", "Restart device"],
            "confidence": 0.82
        },
        # Network
        {
            "id": "MOB_NET_006",
            "category": "network_issues",
            "conditions": {"device": "mobile", "calls_dropping": true},
            "cause": "Weak signal or carrier issue",
            "solutions": ["Enable WiFi calling", "Check carrier settings update", "Replace SIM card"],
            "confidence": 0.82
        },
        {
            "id": "MOB_NET_007",
            "category": "network_issues",
            "conditions": {"device": "mobile", "hotspot_no_internet": true},
            "cause": "APN settings or data limit",
            "solutions": ["Check APN type for DUN", "Check data plan limits", "Use 2.4GHz band for compatibility"],
            "confidence": 0.80
        },
        {
            "id": "MOB_NET_008",
            "category": "network_issues",
            "conditions": {"device": "mobile", "nfc_not_working": true},
            "cause": "NFC off or sensor location",
            "solutions": ["Enable NFC in settings", "Tap top/back of phone", "Remove thick case"],
            "confidence": 0.88
        },
        # Screen
        {
            "id": "MOB_SCREEN_006",
            "category": "screen_problems",
            "conditions": {"device": "mobile", "screen_rotation_fail": true},
            "cause": "Accelerometer stuck or rotation locked",
            "solutions": ["Unlock auto-rotation", "Calibrate compass/sensors", "Restart device"],
            "confidence": 0.85
        },
        {
            "id": "MOB_SCREEN_007",
            "category": "screen_problems",
            "conditions": {"device": "mobile", "proximity_sensor_issue": true},
            "cause": "Screen protector blocking sensor",
            "solutions": ["Remove screen protector", "Clean top bezel area", "Test sensor code"],
            "confidence": 0.88
        },
        # App
        {
            "id": "MOB_APP_006",
            "category": "app_crashes",
            "conditions": {"device": "mobile", "google_play_stop": true},
            "cause": "Play Services issue",
            "solutions": ["Clear Play Store cache", "Clear Play Services data", "Remove/Add Google Account"],
            "confidence": 0.85
        },
        {
            "id": "MOB_APP_007",
            "category": "app_crashes",
            "conditions": {"device": "mobile", "whatsapp_backup_stuck": true},
            "cause": "Network or Google Drive issue",
            "solutions": ["Check connection", "Update Google Play Services", "Clear WhatsApp cache"],
            "confidence": 0.80
        },
        # Storage
        {
            "id": "MOB_STORAGE_004",
            "category": "storage_issues",
            "conditions": {"device": "mobile", "system_storage_huge": true},
            "cause": "Log files or cache accumulation",
            "solutions": ["Dial *#9900# (Samsung) to clear logs", "Factory reset", "Root access to clear log folder (advanced)"],
            "confidence": 0.75
        },
        {
            "id": "MOB_STORAGE_005",
            "category": "storage_issues",
            "conditions": {"device": "mobile", "sd_card_corrupt": true},
            "cause": "Corrupted filesystem",
            "solutions": ["Format SD card in PC", "CHKDSK repair", "Replace SD card"],
            "confidence": 0.85
        },
        # Audio
        {
            "id": "MOB_AUDIO_004",
            "category": "audio_problems",
            "conditions": {"device": "mobile", "mic_muffled": true},
            "cause": "Debris in mic hole",
            "solutions": ["Clean mic hole with needle gently", "Remove case blockage", "Record voice memo to test"],
            "confidence": 0.88
        },
        {
            "id": "MOB_AUDIO_005",
            "category": "audio_problems",
            "conditions": {"device": "mobile", "bluetooth_lag": true},
            "cause": "Codec latency",
            "solutions": ["Use gaming mode", "Forget/Repair device", "Check codec instructions"],
            "confidence": 0.78
        },
        # Charge/Start
        {
            "id": "MOB_START_004",
            "category": "startup_failure",
            "conditions": {"device": "mobile", "moisture_detected": true},
            "cause": "Wet charging port",
            "solutions": ["Dry port with fan", "Wait 2-4 hours", "Use wireless charging"],
            "confidence": 0.95
        },
        {
            "id": "MOB_START_005",
            "category": "startup_failure",
            "conditions": {"device": "mobile", "fastboot_mode": true},
            "cause": "Volume button stuck",
            "solutions": ["Hold power button long press", "Check volume buttons", "Restart"],
            "confidence": 0.90
        },
        # Hardware
        {
            "id": "MOB_HW_004",
            "category": "hardware_failure",
            "conditions": {"device": "mobile", "vibra_not_working": true},
            "cause": "Vibration motor failure or settings",
            "solutions": ["Test in diagnostic menu", "Check sound settings", "Hardware repair"],
            "confidence": 0.82
        },
        {
            "id": "MOB_HW_005",
            "category": "hardware_failure",
            "conditions": {"device": "mobile", "face_unlock_fail": true},
            "cause": "Dirty camera or ambient light",
            "solutions": ["Clean front camera", "Re-register face", "Improve lighting"],
            "confidence": 0.85
        },
        {
            "id": "MOB_HW_006",
            "category": "hardware_failure",
            "conditions": {"device": "mobile", "sim_not_detected": true},
            "cause": "SIM damage or tray issue",
            "solutions": ["Clean SIM contacts", "Try different SIM", "Insert paper piece for pressure"],
            "confidence": 0.85
        },
        {
            "id": "MOB_SEC_001",
            "category": "security",
            "conditions": {"device": "mobile", "random_ads": true},
            "cause": "Adware app",
            "solutions": ["Check recently installed apps", "Use antivirus scan", "Revoke 'Display over other apps' permission"],
            "confidence": 0.92
        },
        {
            "id": "MOB_SEC_002",
            "category": "security",
            "conditions": {"device": "mobile", "phone_remote_controlled": true},
            "cause": "Spyware or Accessibility abuse",
            "solutions": ["Factory reset immediately", "Check Accessibility services", "Disconnect internet"],
            "confidence": 0.95
        }
    ]
    return new_rules

def main():
    base_dir = r"d:\Hybrid Intelligent Troubleshooting System for Computers & Mobile Devices\data"
    comp_path = os.path.join(base_dir, "computer_rules.json")
    mob_path = os.path.join(base_dir, "mobile_rules.json")
    
    # Update Computer Rules
    print("Updating computer rules...")
    try:
        comp_data = load_json(comp_path)
        existing_ids = {r["id"] for r in comp_data.get("rules", [])}
        new_comp_rules = add_computer_rules()
        added_count = 0
        for rule in new_comp_rules:
            if rule["id"] not in existing_ids:
                comp_data["rules"].append(rule)
                added_count += 1
        save_json(comp_path, comp_data)
        print(f"Added {added_count} new computer rules. Total: {len(comp_data['rules'])}")
    except Exception as e:
        print(f"Error updating computer rules: {e}")

    # Update Mobile Rules
    print("Updating mobile rules...")
    try:
        mob_data = load_json(mob_path)
        existing_ids = {r["id"] for r in mob_data.get("rules", [])}
        new_mob_rules = add_mobile_rules()
        added_count = 0
        for rule in new_mob_rules:
            if rule["id"] not in existing_ids:
                mob_data["rules"].append(rule)
                added_count += 1
        save_json(mob_path, mob_data)
        print(f"Added {added_count} new mobile rules. Total: {len(mob_data['rules'])}")
    except Exception as e:
        print(f"Error updating mobile rules: {e}")

if __name__ == "__main__":
    true = True # JS compatibility
    false = False
    main()
