import os

replacements = {
    'backend/app/mobile_forensics/location_engine.py': [('MobileLocation', 'ForensicMobileLocation')],
    'backend/app/mobile_forensics/device_manager.py': [('MobileDevice', 'ForensicMobileDevice')],
    'backend/app/mobile_forensics/communication_engine.py': [('MobileCommunication', 'ForensicMobileCommunication')],
}

for filepath, reps in replacements.items():
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read()
        for old, new in reps:
            content = content.replace(old, new)
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Fixed {filepath}")
