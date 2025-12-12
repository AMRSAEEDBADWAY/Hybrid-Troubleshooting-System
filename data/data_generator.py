"""
Data Generator Module
=====================
This module generates a larger training dataset with:
- Data augmentation techniques
- Bilingual support (Arabic + English)
- Balanced categories
- Text variations and synonyms
"""

import json
import random
import os

# Problem patterns for each category - English
ENGLISH_PATTERNS = {
    "overheating": [
        "my {device} is overheating",
        "the {device} gets very hot",
        "{device} heats up quickly",
        "fan is making loud noise on my {device}",
        "{device} shuts down due to heat",
        "CPU temperature too high",
        "graphics card running hot",
        "{device} overheats when gaming",
        "{device} thermal throttling",
        "my {device} is burning hot",
        "{device} feels hot to touch",
        "extreme heat from {device}",
        "heat issues with my {device}",
        "{device} temperature warning",
        "cooling system not working",
        "fan spinning very fast",
        "{device} crashes from overheating",
        "hot air from {device} vents",
        "{device} gets warm during use",
        "overheating problem on {device}",
    ],
    "slow_performance": [
        "my {device} is very slow",
        "{device} running slowly",
        "{device} is lagging",
        "programs take forever to open",
        "{device} freezes frequently",
        "system is sluggish",
        "everything is slow on my {device}",
        "{device} performance degraded",
        "apps respond slowly",
        "{device} takes long to boot",
        "{device} hangs a lot",
        "slow loading times",
        "{device} is unresponsive",
        "delayed response from {device}",
        "{device} is extremely slow",
        "performance issues on {device}",
        "{device} stuttering",
        "long wait times on {device}",
        "system lag on {device}",
        "{device} performance dropped",
    ],
    "battery_issues": [
        "battery drains very fast",
        "{device} battery dies quickly",
        "battery not holding charge",
        "{device} not charging",
        "battery percentage drops suddenly",
        "charging is very slow",
        "battery health is bad",
        "{device} turns off with battery left",
        "battery swollen",
        "power issues with {device}",
        "battery life terrible",
        "{device} won't charge properly",
        "battery depletes quickly",
        "need to charge constantly",
        "battery not lasting long",
        "{device} loses charge fast",
        "charging port not working",
        "battery replacement needed",
        "power drain on {device}",
        "{device} battery dead",
    ],
    "network_issues": [
        "can't connect to WiFi",
        "internet keeps disconnecting",
        "no network connection",
        "WiFi signal weak",
        "Bluetooth not working",
        "can't find wireless networks",
        "ethernet not connecting",
        "mobile data not working",
        "network adapter issues",
        "DNS not responding",
        "WiFi drops frequently",
        "no internet access",
        "connection timeout",
        "network error on {device}",
        "can't access internet",
        "WiFi authentication failed",
        "Bluetooth won't pair",
        "cellular data problems",
        "wireless connection unstable",
        "network keeps dropping",
    ],
    "startup_failure": [
        "{device} won't turn on",
        "stuck on boot screen",
        "Windows not starting",
        "black screen on startup",
        "{device} beeps but doesn't start",
        "boot loop problem",
        "BIOS not loading",
        "{device} stuck on logo",
        "won't boot up",
        "startup repair failed",
        "{device} not powering on",
        "system won't start",
        "endless reboot",
        "frozen on startup",
        "can't get past boot",
        "{device} dead",
        "power button not responding",
        "no display on startup",
        "{device} won't initialize",
        "failed to boot",
    ],
    "screen_problems": [
        "screen is flickering",
        "display has dead pixels",
        "monitor not showing anything",
        "screen is cracked",
        "touch screen not responding",
        "display colors wrong",
        "screen brightness too dim",
        "ghost touch on screen",
        "lines on the screen",
        "screen goes black randomly",
        "display glitching",
        "screen frozen",
        "monitor flickering",
        "screen tearing",
        "display not working",
        "blank screen",
        "screen display issues",
        "touch not registering",
        "screen unresponsive",
        "visual glitches",
    ],
    "storage_issues": [
        "hard drive full",
        "not enough disk space",
        "can't save files",
        "storage running low",
        "SSD not detected",
        "external drive not recognized",
        "storage full warning",
        "can't install apps",
        "SD card not working",
        "disk read error",
        "no space left",
        "storage problem",
        "hard drive failing",
        "disk not showing up",
        "memory card error",
        "storage corrupted",
        "can't access files",
        "drive not mounting",
        "low storage space",
        "disk space issue",
    ],
    "audio_problems": [
        "no sound from speakers",
        "audio is crackling",
        "microphone not working",
        "headphones not detected",
        "volume very low",
        "sound driver issues",
        "audio cutting out",
        "speaker buzzing noise",
        "no audio in videos",
        "speaker not working",
        "sound distorted",
        "audio delay",
        "mic not picking up voice",
        "audio static",
        "sound problems",
        "earpiece not working",
        "audio muffled",
        "no sound output",
        "speaker crackling",
        "audio quality bad",
    ],
    "app_crashes": [
        "apps keep crashing",
        "program stops working",
        "application not responding",
        "app closes unexpectedly",
        "software crashes on startup",
        "games crashing",
        "browser freezing",
        "app force closes",
        "error when opening app",
        "program has stopped working",
        "app won't load",
        "software not responding",
        "application freezes",
        "app keeps closing",
        "program crashes",
        "app not opening",
        "software error",
        "app keeps stopping",
        "game not launching",
        "app malfunction",
    ],
    "hardware_failure": [
        "RAM not recognized",
        "blue screen error",
        "clicking sounds from {device}",
        "hardware component failed",
        "motherboard issue",
        "graphics card not working",
        "power supply failure",
        "USB ports not working",
        "keyboard not responding",
        "mouse not working",
        "hardware malfunction",
        "component failure",
        "camera not working",
        "fingerprint not working",
        "buttons not responding",
        "trackpad issues",
        "sensor not working",
        "hardware error",
        "device malfunction",
        "physical damage",
    ],
}

# Problem patterns for each category - Arabic
ARABIC_PATTERNS = {
    "overheating": [
        "{device} بيسخن جدا",
        "حرارة {device} عالية",
        "المروحة صوتها عالي في {device}",
        "{device} بيطفي من الحرارة",
        "سخونة شديدة في {device}",
        "{device} ساخن جدا",
        "مشكلة حرارة في {device}",
        "{device} بيسخن وانا بلعب",
        "تحذير حرارة على {device}",
        "{device} حار للمس",
        "المعالج حرارته مرتفعة",
        "كارت الشاشة بيسخن",
        "{device} بيعمل ثروتلينج",
        "مشكلة التبريد في {device}",
        "{device} سخونته زيادة",
        "التهوية مش كويسة",
        "{device} بيطفي من السخونة",
        "المروحة مش شغالة كويس",
        "حرارة المعالج فوق الطبيعي",
        "{device} ساخن اوي",
    ],
    "slow_performance": [
        "{device} بطيء جدا",
        "{device} تقيل",
        "أداء {device} ضعيف",
        "البرامج بتفتح ببطء",
        "{device} بيهنج كتير",
        "{device} مش بيستجيب",
        "كل حاجة بطيئة على {device}",
        "{device} لاج",
        "التطبيقات بطيئة",
        "{device} بياخد وقت يفتح",
        "الجهاز ثقيل",
        "سرعة {device} قلت",
        "{device} بيتأخر في الاستجابة",
        "الاداء بقى سيء",
        "{device} بطيء في التحميل",
        "البطء الشديد في {device}",
        "{device} مش سريع زي الاول",
        "تهنيج مستمر",
        "الجهاز واقف",
        "اللاج كتير على {device}",
    ],
    "battery_issues": [
        "البطارية بتخلص بسرعة",
        "{device} الشحن بينزل بسرعة",
        "البطارية مش بتشحن",
        "الشحن بطيء جدا",
        "عمر البطارية قصير",
        "{device} مش بيشحن",
        "البطارية منتفخة",
        "الشحن بينزل فجأة",
        "مشكلة في شحن {device}",
        "البطارية خربانة",
        "{device} بيفصل والشحن موجود",
        "الباور مش كويس",
        "بطارية {device} ضعيفة",
        "الشاحن مش شغال",
        "منفذ الشحن فيه مشكلة",
        "البطارية بتروح بسرعة",
        "محتاج اشحن كل شوية",
        "البطارية مش ماسكة",
        "مشاكل الطاقة",
        "الشحن مش واصل",
    ],
    "network_issues": [
        "الواي فاي مش شغال",
        "النت بيفصل",
        "مفيش اتصال",
        "اشارة الواي فاي ضعيفة",
        "البلوتوث مش شغال",
        "مش لاقي شبكات",
        "الايثرنت مش شغال",
        "الداتا مش شغالة",
        "مشكلة في الشبكة",
        "DNS مش شغال",
        "الانترنت واقف",
        "الاتصال بيقطع",
        "مفيش نت",
        "مشكلة اتصال",
        "الشبكة مش مستقرة",
        "واي فاي مش بيتصل",
        "البلوتوث مش بيعمل باير",
        "خط الموبايل مش شغال",
        "النت بطيء",
        "الوايرلس فيه مشكلة",
    ],
    "startup_failure": [
        "{device} مش بيفتح",
        "واقف على شاشة البوت",
        "الويندوز مش بيفتح",
        "شاشة سودا عند التشغيل",
        "{device} بيصفر ومش بيفتح",
        "بيفتح ويقفل لوحده",
        "البايوس مش شغال",
        "{device} واقف على اللوجو",
        "مش بيعمل بوت",
        "اصلاح التشغيل فشل",
        "{device} ميت",
        "زر الباور مش شغال",
        "مفيش صورة عند التشغيل",
        "{device} مش بيشتغل",
        "بوت لوب",
        "الجهاز مش راضي يفتح",
        "توقف عند بداية التشغيل",
        "مشكلة في الاقلاع",
        "{device} طفي ومش راضي يفتح",
        "فشل في التشغيل",
    ],
    "screen_problems": [
        "الشاشة بترعش",
        "فيه نقط ميتة في الشاشة",
        "الشاشة مش بتظهر حاجة",
        "الشاشة مكسورة",
        "التاتش مش شغال",
        "الوان الشاشة غلط",
        "الشاشة باهتة",
        "لمسات وهمية على الشاشة",
        "خطوط على الشاشة",
        "الشاشة بتطفي لوحدها",
        "الديسبلاي فيه مشكلة",
        "الشاشة فريزة",
        "وميض في الشاشة",
        "تمزق الصورة",
        "الشاشة سودا",
        "الشاشة مش بتستجيب",
        "مشاكل العرض",
        "اللمس مش بيشتغل",
        "جليتشات في الشاشة",
        "شاشة سوداء",
    ],
    "storage_issues": [
        "الهارد ممتلي",
        "مفيش مساحة",
        "مش قادر احفظ ملفات",
        "تحذير المساحة منخفضة",
        "SSD مش ظاهر",
        "الهارد الخارجي مش ظاهر",
        "التخزين ممتلئ",
        "مش قادر انزل تطبيقات",
        "الميموري كارد مش شغالة",
        "خطأ قراءة القرص",
        "مفيش مساحة فاضية",
        "مشكلة تخزين",
        "الهارد بيفشل",
        "الدرايف مش ظاهر",
        "خطأ كارت الميموري",
        "التخزين تالف",
        "مش قادر اوصل للملفات",
        "الدرايف مش بيعمل ماونت",
        "المساحة خلصت",
        "مشكلة مساحة القرص",
    ],
    "audio_problems": [
        "مفيش صوت",
        "الصوت بيقطع",
        "المايك مش شغال",
        "السماعات مش ظاهرة",
        "الصوت واطي",
        "مشكلة في تعريف الصوت",
        "الصوت بيفصل",
        "صوت تشويش من السماعة",
        "مفيش صوت في الفيديوهات",
        "سماعة {device} مش شغالة",
        "الصوت مشوش",
        "تأخير في الصوت",
        "المايك مش بياخد صوت",
        "استاتيك في الصوت",
        "مشاكل الصوت",
        "السماعة الداخلية مش شغالة",
        "الصوت مكتوم",
        "مفيش صوت خارج",
        "طقطقة في السماعة",
        "جودة الصوت سيئة",
    ],
    "app_crashes": [
        "التطبيقات بتقفل لوحدها",
        "البرنامج واقف",
        "التطبيق مش بيستجيب",
        "الابلكيشن بيقفل فجأة",
        "البرامج بتكرش",
        "الالعاب بتقفل",
        "المتصفح بيهنج",
        "التطبيق بيعمل فورس كلوز",
        "رسالة خطأ لما بفتح التطبيق",
        "البرنامج توقف عن العمل",
        "التطبيق مش بيفتح",
        "البرنامج مش بيستجيب",
        "التطبيق بيفريز",
        "الابليكيشن بيوقع",
        "كراش في البرنامج",
        "التطبيق مش راضي يفتح",
        "خطأ في البرنامج",
        "التطبيق بيقف",
        "اللعبة مش بتشتغل",
        "عطل في التطبيق",
    ],
    "hardware_failure": [
        "الرام مش ظاهرة",
        "شاشة زرقا",
        "صوت طقطقة من {device}",
        "قطعة هاردوير خربانة",
        "مشكلة في المازربورد",
        "كارت الشاشة مش شغال",
        "الباور سبلاي خربان",
        "منافذ USB مش شغالة",
        "الكيبورد مش بيستجيب",
        "الماوس مش شغال",
        "عطل في الهاردوير",
        "قطعة فشلت",
        "الكاميرا مش شغالة",
        "البصمة مش شغالة",
        "الازرار مش شغالة",
        "التراك باد فيه مشكلة",
        "السينسور مش شغال",
        "خطأ هاردوير",
        "الجهاز فيه عطل",
        "ضرر فيزيائي",
    ],
}

# Device keywords
DEVICES_EN = ["computer", "laptop", "PC", "phone", "tablet", "device", "system", "machine"]
DEVICES_AR = ["الكمبيوتر", "اللابتوب", "الجهاز", "الموبايل", "التابلت", "الهاتف", "التليفون", "الحاسوب"]


def generate_variations(pattern: str, devices: list) -> list:
    """Generate variations of a pattern with different devices."""
    variations = []
    for device in devices:
        text = pattern.replace("{device}", device)
        variations.append(text)
    return variations


def augment_text(text: str) -> list:
    """Create augmented versions of text."""
    augmented = [text]
    
    # Add with prefix/suffix
    prefixes_en = ["I have a problem: ", "Help! ", "Issue: ", "Problem: ", "Can you help? ", "Please help, ", ""]
    prefixes_ar = ["عندي مشكلة: ", "محتاج مساعدة! ", "المشكلة: ", "ساعدني ", "من فضلك ساعدني ", ""]
    
    suffixes_en = ["", " please help", " what should I do?", " need help", " can you fix it?", " urgent"]
    suffixes_ar = ["", " محتاج مساعدة", " ايه الحل؟", " عايز حل", " ممكن تساعدني؟", " ضروري"]
    
    # Determine if Arabic or English
    is_arabic = any('\u0600' <= c <= '\u06FF' for c in text)
    
    prefixes = prefixes_ar if is_arabic else prefixes_en
    suffixes = suffixes_ar if is_arabic else suffixes_en
    
    # Add variations
    for prefix in random.sample(prefixes, min(2, len(prefixes))):
        for suffix in random.sample(suffixes, min(2, len(suffixes))):
            new_text = prefix + text + suffix
            if new_text != text:
                augmented.append(new_text.strip())
    
    return augmented


def generate_dataset(examples_per_category: int = 100) -> list:
    """Generate a balanced dataset with specified examples per category."""
    dataset = []
    categories = list(ENGLISH_PATTERNS.keys())
    
    for category in categories:
        category_examples = []
        
        # Generate English examples
        en_patterns = ENGLISH_PATTERNS[category]
        for pattern in en_patterns:
            variations = generate_variations(pattern, DEVICES_EN)
            for var in variations:
                augmented = augment_text(var)
                for aug in augmented:
                    category_examples.append({
                        "text": aug,
                        "category": category
                    })
        
        # Generate Arabic examples
        ar_patterns = ARABIC_PATTERNS[category]
        for pattern in ar_patterns:
            variations = generate_variations(pattern, DEVICES_AR)
            for var in variations:
                augmented = augment_text(var)
                for aug in augmented:
                    category_examples.append({
                        "text": aug,
                        "category": category
                    })
        
        # Shuffle and limit
        random.shuffle(category_examples)
        category_examples = category_examples[:examples_per_category]
        
        # If we don't have enough, duplicate
        while len(category_examples) < examples_per_category:
            category_examples.append(random.choice(category_examples))
        
        dataset.extend(category_examples)
    
    random.shuffle(dataset)
    return dataset


def save_dataset(dataset: list, output_path: str):
    """Save dataset to JSON file."""
    data = {"examples": dataset}
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(dataset)} examples to {output_path}")


if __name__ == "__main__":
    # Generate dataset
    print("Generating enhanced training dataset...")
    dataset = generate_dataset(examples_per_category=100)
    
    # Save to data directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(current_dir, "training_data.json")
    
    save_dataset(dataset, output_path)
    
    # Print statistics
    print("\nDataset Statistics:")
    print(f"Total examples: {len(dataset)}")
    
    from collections import Counter
    categories = Counter([ex["category"] for ex in dataset])
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count}")
