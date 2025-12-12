"""
Translations Module
===================
Centralized translations for Arabic and English support.
All UI strings are defined here for easy maintenance.
"""

from typing import Dict, Any

# Supported languages
SUPPORTED_LANGUAGES = ["en", "ar"]
DEFAULT_LANGUAGE = "en"

# RTL languages
RTL_LANGUAGES = ["ar"]


def is_rtl(lang: str) -> bool:
    """Check if language is right-to-left."""
    return lang in RTL_LANGUAGES


def get_text(key: str, lang: str = "en") -> str:
    """
    Get translated text for a given key and language.
    
    Args:
        key: The translation key
        lang: Language code ('en' or 'ar')
        
    Returns:
        Translated string, falls back to English if not found
    """
    if lang not in TRANSLATIONS:
        lang = DEFAULT_LANGUAGE
    
    text = TRANSLATIONS.get(lang, {}).get(key)
    if text is None:
        # Fallback to English
        text = TRANSLATIONS.get("en", {}).get(key, key)
    return text


def get_option_text(option: str, lang: str = "en") -> str:
    """Get translated text for symptom options."""
    return OPTION_TRANSLATIONS.get(lang, {}).get(option.lower(), option)


# Main UI Translations
TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "en": {
        # Page config
        "page_title": "🔧 Intelligent Troubleshooting System",
        "page_subtitle": "AI-Powered Diagnosis for Computer & Mobile Devices",
        
        # Header
        "main_title": "🔧 Intelligent Troubleshooting System",
        "main_subtitle": "AI-Powered Diagnosis for Computer & Mobile Devices",
        
        # Sidebar
        "sidebar_title": "Troubleshooter",
        "sidebar_subtitle": "AI-Powered Diagnostics",
        "system_stats": "📊 System Stats",
        "pc_label": "💻 PC",
        "mobile_label": "📱 Mobile",
        "total_rules": "🎯 Total Rules",
        "ml_accuracy": "🧠 ML Accuracy",
        "categories_title": "🏷️ Categories",
        "quick_actions": "⚡ Quick Actions",
        "new_session": "🔄 New Session",
        "export_pdf": "📄 Export PDF",
        "download_report": "⬇️ Download Report",
        "language_title": "🌐 Language",
        "built_with": "Built with 💜 using",
        "tech_stack": "Python • Streamlit • Scikit-learn",
        "version": "v2.0 Enhanced",
        
        # Tabs
        "tab_chat": "💬 Chat Assistant",
        "tab_quick_diagnosis": "⚡ Quick Diagnosis",
        "tab_overview": "📊 System Overview",
        
        # Chat Interface
        "chat_title": "💬 Chat Assistant",
        "chat_subtitle": "Describe your problem",
        "chat_placeholder": "💭 Type your message here...",
        
        # Quick Diagnosis
        "quick_diagnosis_title": "⚡ Quick Diagnosis",
        "quick_diagnosis_subtitle": "Get instant AI-powered diagnosis",
        "computer_button": "💻 Computer / Laptop",
        "mobile_button": "📱 Mobile / Tablet",
        "describe_problem": "📝 Describe your problem",
        "problem_placeholder": "e.g., My laptop is overheating...",
        "additional_symptoms": "🔍 Additional Symptoms (Optional)",
        "diagnose_button": "🔬 Analyze & Diagnose",
        "analyzing": "🔄 Analyzing with AI...",
        "describe_first": "⚠️ Please describe your problem first!",
        
        # Diagnosis Result
        "diagnosis_complete": "Diagnosis Complete",
        "category_label": "🎯 Category",
        "ml_confidence": "ML confidence",
        "diagnosis_confidence": "🔬 Diagnosis Confidence",
        "high": "High",
        "medium": "Medium",
        "rule_label": "📋 Rule",
        "identified_cause": "🎯 Identified Cause",
        "recommended_solutions": "💡 Recommended Solutions",
        "step": "Step",
        "explanation": "📝 Technical Explanation",
        "other_causes": "🔄 Other Possible Causes",
        "download_report_btn": "📄 Download Report",
        "save_report": "⬇️ Save Report",
        
        # System Overview
        "overview_title": "📊 System Overview",
        "overview_subtitle": "Architecture and performance metrics",
        "architecture": "🏗️ Architecture",
        "technologies": "🛠️ Technologies",
        "performance": "📈 Performance",
        "model_trained": "✅ ML Model: Trained and Ready",
        "model_not_trained": "⚠️ ML Model: Not Trained",
        "model_accuracy": "Model Accuracy",
        "from_baseline": "from baseline",
        "supported_categories": "📋 Supported Categories",
        "kb_statistics": "📊 Knowledge Base Statistics",
        "total_rules_stat": "📚 Total Rules",
        "computer_stat": "💻 Computer",
        "mobile_stat": "📱 Mobile",
        "categories_stat": "🏷️ Categories",
        
        # Chatbot
        "welcome": "Welcome to the Intelligent Troubleshooting Assistant!",
        "welcome_help": "I'm here to help diagnose problems with your **computer** or **mobile device**.",
        "lets_start": "Let's get started!",
        "select_device": "What type of device are you having trouble with?",
        "computer_option": "Computer (Desktop/Laptop)",
        "mobile_option": "Mobile (Smartphone/Tablet)",
        "didnt_understand": "I didn't quite catch that. Please select your device type:",
        "type_computer": "Type **computer** for Desktop/Laptop",
        "type_mobile": "Type **mobile** for Smartphone/Tablet",
        "great_troubleshooting": "Great! You're troubleshooting a",
        "describe_problem_detail": "Now, please **describe your problem** in detail:",
        "examples": "Examples:",
        "example_overheat": "My laptop is overheating",
        "example_battery": "Battery drains fast",
        "example_slow": "Computer is slow",
        
        # Device-specific examples
        "computer_example1": "My laptop is overheating",
        "computer_example2": "Computer is running slow",
        "computer_example3": "Blue screen errors",
        "mobile_example1": "Battery drains fast",
        "mobile_example2": "Phone is overheating",
        "mobile_example3": "Screen is not responding to touch",
        
        "initial_analysis": "📊 **Initial Analysis:**",
        "appears_to_be": "Based on your description, this appears to be a",
        "issue": "issue",
        "confidence": "Confidence",
        "followup_questions": "To provide a more accurate diagnosis, I need to ask a few follow-up questions:",
        "question": "Question",
        "options": "Options",
        "got_it": "Got it!",
        "diagnosis_header": "🔍 **DIAGNOSIS COMPLETE**",
        "identified_issue": "Identified Issue",
        "category": "Category",
        "solutions": "💡 Recommended Solutions",
        "explanation_label": "📝 Explanation",
        "alternatives": "Other Possible Causes",
        "what_next": "Would you like to:",
        "type_new": "Type **new** to diagnose another problem",
        "type_details": "Type **details** for more technical information",
        "type_exit": "Type **exit** to end the session",
        "already_diagnosed": "I've already provided a diagnosis.",
        "not_sure": "I'm not sure how to respond. Type **new** to start over.",
        "goodbye": "Thank you for using the Troubleshooting Assistant! Goodbye!",
        "technical_details": "📋 **TECHNICAL DETAILS**",
        "device_type": "Device Type",
        "predicted_category": "Predicted Category",
        "collected_symptoms": "Collected Symptoms",
        "no_symptoms": "No additional symptoms collected",
        "rule_id": "Rule ID",
        "final_confidence": "Final Confidence",
        "inference_trace": "Inference Trace",
        "not_sure_option": "Not sure",
    },
    
    "ar": {
        # Page config
        "page_title": "🔧 نظام استكشاف الأخطاء الذكي",
        "page_subtitle": "تشخيص مدعوم بالذكاء الاصطناعي للكمبيوتر والموبايل",
        
        # Header
        "main_title": "🔧 نظام استكشاف الأخطاء الذكي",
        "main_subtitle": "تشخيص مدعوم بالذكاء الاصطناعي للكمبيوتر والموبايل",
        
        # Sidebar
        "sidebar_title": "مستكشف الأخطاء",
        "sidebar_subtitle": "تشخيص بالذكاء الاصطناعي",
        "system_stats": "📊 إحصائيات النظام",
        "pc_label": "💻 كمبيوتر",
        "mobile_label": "📱 موبايل",
        "total_rules": "🎯 إجمالي القواعد",
        "ml_accuracy": "🧠 دقة النموذج",
        "categories_title": "🏷️ الفئات",
        "quick_actions": "⚡ إجراءات سريعة",
        "new_session": "🔄 جلسة جديدة",
        "export_pdf": "📄 تصدير PDF",
        "download_report": "⬇️ تحميل التقرير",
        "language_title": "🌐 اللغة",
        "built_with": "صُنع بـ 💜 باستخدام",
        "tech_stack": "Python • Streamlit • Scikit-learn",
        "version": "الإصدار 2.0 المحسن",
        
        # Tabs
        "tab_chat": "💬 مساعد المحادثة",
        "tab_quick_diagnosis": "⚡ تشخيص سريع",
        "tab_overview": "📊 نظرة عامة",
        
        # Chat Interface
        "chat_title": "💬 مساعد المحادثة",
        "chat_subtitle": "اوصف مشكلتك",
        "chat_placeholder": "💭 اكتب رسالتك هنا...",
        
        # Quick Diagnosis
        "quick_diagnosis_title": "⚡ تشخيص سريع",
        "quick_diagnosis_subtitle": "احصل على تشخيص فوري بالذكاء الاصطناعي",
        "computer_button": "💻 كمبيوتر / لابتوب",
        "mobile_button": "📱 موبايل / تابلت",
        "describe_problem": "📝 اوصف مشكلتك",
        "problem_placeholder": "مثال: اللابتوب بيسخن...",
        "additional_symptoms": "🔍 أعراض إضافية (اختياري)",
        "diagnose_button": "🔬 تحليل وتشخيص",
        "analyzing": "🔄 جاري التحليل بالذكاء الاصطناعي...",
        "describe_first": "⚠️ من فضلك اوصف مشكلتك أولاً!",
        
        # Diagnosis Result
        "diagnosis_complete": "اكتمل التشخيص",
        "category_label": "🎯 الفئة",
        "ml_confidence": "ثقة النموذج",
        "diagnosis_confidence": "🔬 ثقة التشخيص",
        "high": "عالية",
        "medium": "متوسطة",
        "rule_label": "📋 القاعدة",
        "identified_cause": "🎯 السبب المحدد",
        "recommended_solutions": "💡 الحلول الموصى بها",
        "step": "الخطوة",
        "explanation": "📝 الشرح التقني",
        "other_causes": "🔄 أسباب محتملة أخرى",
        "download_report_btn": "📄 تحميل التقرير",
        "save_report": "⬇️ حفظ التقرير",
        
        # System Overview
        "overview_title": "📊 نظرة عامة على النظام",
        "overview_subtitle": "البنية ومقاييس الأداء",
        "architecture": "🏗️ البنية",
        "technologies": "🛠️ التقنيات",
        "performance": "📈 الأداء",
        "model_trained": "✅ نموذج ML: مدرب وجاهز",
        "model_not_trained": "⚠️ نموذج ML: غير مدرب",
        "model_accuracy": "دقة النموذج",
        "from_baseline": "من الأساس",
        "supported_categories": "📋 الفئات المدعومة",
        "kb_statistics": "📊 إحصائيات قاعدة المعرفة",
        "total_rules_stat": "📚 إجمالي القواعد",
        "computer_stat": "💻 كمبيوتر",
        "mobile_stat": "📱 موبايل",
        "categories_stat": "🏷️ الفئات",
        
        # Chatbot
        "welcome": "مرحباً بك في مساعد استكشاف الأخطاء الذكي!",
        "welcome_help": "أنا هنا لمساعدتك في تشخيص مشاكل **الكمبيوتر** أو **الموبايل**.",
        "lets_start": "هيا نبدأ!",
        "select_device": "ما نوع الجهاز الذي لديك مشكلة فيه؟",
        "computer_option": "كمبيوتر (مكتبي/لابتوب)",
        "mobile_option": "موبايل (هاتف ذكي/تابلت)",
        "didnt_understand": "لم أفهم، من فضلك اختر نوع الجهاز:",
        "type_computer": "اكتب **كمبيوتر** للكمبيوتر المكتبي/اللابتوب",
        "type_mobile": "اكتب **موبايل** للهاتف الذكي/التابلت",
        "great_troubleshooting": "ممتاز! أنت تستكشف مشكلة في",
        "describe_problem_detail": "الآن، من فضلك **اوصف مشكلتك** بالتفصيل:",
        "examples": "أمثلة:",
        "example_overheat": "اللابتوب بيسخن",
        "example_battery": "البطارية بتخلص بسرعة",
        "example_slow": "الكمبيوتر بطيء",
        
        # Device-specific examples
        "computer_example1": "اللابتوب بيسخن",
        "computer_example2": "الكمبيوتر بطيء",
        "computer_example3": "شاشة زرقاء بتظهر",
        "mobile_example1": "البطارية بتخلص بسرعة",
        "mobile_example2": "الموبايل بيسخن",
        "mobile_example3": "الشاشة مش بتستجيب للمس",
        
        "initial_analysis": "📊 **التحليل الأولي:**",
        "appears_to_be": "بناءً على وصفك، يبدو أن هذه مشكلة",
        "issue": "",
        "confidence": "الثقة",
        "followup_questions": "لتقديم تشخيص أدق، أحتاج لسؤالك بعض الأسئلة:",
        "question": "سؤال",
        "options": "الخيارات",
        "got_it": "فهمت!",
        "diagnosis_header": "🔍 **اكتمل التشخيص**",
        "identified_issue": "المشكلة المحددة",
        "category": "الفئة",
        "solutions": "💡 الحلول الموصى بها",
        "explanation_label": "📝 الشرح",
        "alternatives": "أسباب محتملة أخرى",
        "what_next": "هل تريد:",
        "type_new": "اكتب **جديد** لتشخيص مشكلة أخرى",
        "type_details": "اكتب **تفاصيل** لمعلومات تقنية أكثر",
        "type_exit": "اكتب **خروج** لإنهاء الجلسة",
        "already_diagnosed": "لقد قدمت التشخيص بالفعل.",
        "not_sure": "لست متأكداً كيف أرد. اكتب **جديد** للبدء من جديد.",
        "goodbye": "شكراً لاستخدامك مساعد استكشاف الأخطاء! مع السلامة!",
        "technical_details": "📋 **التفاصيل التقنية**",
        "device_type": "نوع الجهاز",
        "predicted_category": "الفئة المتوقعة",
        "collected_symptoms": "الأعراض المجمعة",
        "no_symptoms": "لم يتم جمع أعراض إضافية",
        "rule_id": "معرف القاعدة",
        "final_confidence": "الثقة النهائية",
        "inference_trace": "تتبع الاستدلال",
        "not_sure_option": "غير متأكد",
    }
}

# Category translations
CATEGORY_TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "overheating": {"en": "Overheating", "ar": "السخونة الزائدة"},
    "slow_performance": {"en": "Slow Performance", "ar": "بطء الأداء"},
    "battery_issues": {"en": "Battery Issues", "ar": "مشاكل البطارية"},
    "network_issues": {"en": "Network Issues", "ar": "مشاكل الشبكة"},
    "startup_failure": {"en": "Startup Failure", "ar": "فشل الإقلاع"},
    "screen_problems": {"en": "Screen Problems", "ar": "مشاكل الشاشة"},
    "storage_issues": {"en": "Storage Issues", "ar": "مشاكل التخزين"},
    "audio_problems": {"en": "Audio Problems", "ar": "مشاكل الصوت"},
    "app_crashes": {"en": "App Crashes", "ar": "تعطل التطبيقات"},
    "hardware_failure": {"en": "Hardware Failure", "ar": "عطل في الهاردوير"},
}

# Option translations for symptom questions
OPTION_TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "en": {
        "yes": "Yes",
        "no": "No",
        "sometimes": "Sometimes",
        "unsure": "Unsure",
        "high": "High",
        "normal": "Normal",
        "low": "Low",
        "medium": "Medium",
        "mechanical": "Mechanical (HDD)",
        "ssd": "SSD",
        "many": "Many",
        "few": "Few",
        "on": "On",
        "off": "Off",
        "blinking": "Blinking",
        "fast": "Fast",
        "slow": "Slow",
        "no_sd": "No SD Card",
    },
    "ar": {
        "yes": "نعم",
        "no": "لا",
        "sometimes": "أحياناً",
        "unsure": "غير متأكد",
        "high": "عالي",
        "normal": "عادي",
        "low": "منخفض",
        "medium": "متوسط",
        "mechanical": "ميكانيكي (HDD)",
        "ssd": "SSD",
        "many": "كثيرة",
        "few": "قليلة",
        "on": "يعمل",
        "off": "لا يعمل",
        "blinking": "يرمش",
        "fast": "سريع",
        "slow": "بطيء",
        "no_sd": "لا توجد بطاقة SD",
    }
}


def get_category_name(category: str, lang: str = "en") -> str:
    """Get translated category name."""
    cat_trans = CATEGORY_TRANSLATIONS.get(category, {})
    return cat_trans.get(lang, category.replace("_", " ").title())


# Symptom Questions Translations
SYMPTOM_QUESTIONS: Dict[str, Dict[str, str]] = {
    # Computer - Overheating
    "fan_noise": {"en": "Is the fan making loud noise?", "ar": "هل المروحة تصدر صوت عالي؟"},
    "hot_surface": {"en": "Is the device hot to touch?", "ar": "هل الجهاز ساخن عند لمسه؟"},
    "thermal_paste_old": {"en": "Is the computer more than 3 years old without thermal paste change?", "ar": "هل الكمبيوتر عمره أكثر من 3 سنوات بدون تغيير المعجون الحراري؟"},
    "poor_ventilation": {"en": "Is the computer in an enclosed or dusty area?", "ar": "هل الكمبيوتر في مكان مغلق أو مليء بالغبار؟"},
    "high_cpu_usage": {"en": "Is CPU usage constantly high?", "ar": "هل استخدام المعالج مرتفع باستمرار؟"},
    
    # Computer - Slow Performance
    "ram_usage": {"en": "Is RAM usage high (above 80%)?", "ar": "هل استخدام الذاكرة مرتفع (فوق 80%)؟"},
    "hdd_type": {"en": "What type of storage does the computer have?", "ar": "ما نوع وحدة التخزين في الكمبيوتر؟"},
    "startup_programs": {"en": "Are there many programs that start with Windows?", "ar": "هل هناك برامج كثيرة تبدأ مع الويندوز؟"},
    "malware_detected": {"en": "Has any malware been detected recently?", "ar": "هل تم اكتشاف أي فيروسات مؤخراً؟"},
    "os_outdated": {"en": "Is the operating system outdated?", "ar": "هل نظام التشغيل قديم؟"},
    
    # Computer - Startup Failure
    "power_led": {"en": "Is the power LED on?", "ar": "هل ضوء الطاقة يعمل؟"},
    "beep_codes": {"en": "Are there any beep sounds on startup?", "ar": "هل هناك أصوات صفير عند التشغيل؟"},
    "boot_loop": {"en": "Does the computer restart repeatedly?", "ar": "هل الكمبيوتر يعيد التشغيل بشكل متكرر؟"},
    "black_screen": {"en": "Is the screen completely black?", "ar": "هل الشاشة سوداء تماماً؟"},
    "fans_running": {"en": "Are the fans running?", "ar": "هل المراوح تعمل؟"},
    
    # Computer - Network Issues
    "adapter_disabled": {"en": "Is the network adapter enabled?", "ar": "هل محول الشبكة مفعل؟"},
    "dns_error": {"en": "Are you getting DNS errors?", "ar": "هل تظهر أخطاء DNS؟"},
    "ethernet_no_connection": {"en": "Is this an ethernet connection issue?", "ar": "هل هذه مشكلة في اتصال الإيثرنت؟"},
    "driver_outdated": {"en": "Are network drivers updated?", "ar": "هل تعريفات الشبكة محدثة؟"},
    
    # Computer - Screen Problems
    "flickering": {"en": "Is the screen flickering?", "ar": "هل الشاشة ترمش؟"},
    "dead_pixels": {"en": "Are there dead or stuck pixels?", "ar": "هل توجد بكسلات ميتة أو عالقة؟"},
    "dim_display": {"en": "Is the display unusually dim?", "ar": "هل الشاشة خافتة بشكل غير طبيعي؟"},
    "color_distortion": {"en": "Are colors displayed incorrectly?", "ar": "هل الألوان تظهر بشكل غير صحيح؟"},
    
    # Computer - Storage Issues
    "disk_full": {"en": "Is the disk almost full?", "ar": "هل القرص ممتلئ تقريباً؟"},
    "drive_not_detected": {"en": "Is a drive not being detected?", "ar": "هل هناك قرص لا يتم التعرف عليه؟"},
    "disk_read_errors": {"en": "Are there disk read/write errors?", "ar": "هل هناك أخطاء في القراءة/الكتابة؟"},
    
    # Computer - Audio Problems
    "no_sound": {"en": "Is there no sound at all?", "ar": "هل لا يوجد صوت على الإطلاق؟"},
    "crackling_audio": {"en": "Is the audio crackling or distorted?", "ar": "هل الصوت يطقطق أو مشوه؟"},
    "headphones_not_detected": {"en": "Are headphones/speakers not detected?", "ar": "هل لا يتم التعرف على السماعات؟"},
    
    # Computer - Hardware Failure
    "blue_screen": {"en": "Are you getting blue screen errors?", "ar": "هل تظهر شاشة زرقاء؟"},
    "usb_ports_dead": {"en": "Are USB ports not working?", "ar": "هل منافذ USB لا تعمل؟"},
    "random_shutdowns": {"en": "Does the computer shut down randomly?", "ar": "هل الكمبيوتر ينطفئ بشكل عشوائي؟"},
    "clicking_sounds": {"en": "Are there clicking sounds from the computer?", "ar": "هل تسمع أصوات نقر من الكمبيوتر؟"},
    
    # Computer - App Crashes
    "specific_app": {"en": "Is only one specific app crashing?", "ar": "هل تطبيق واحد فقط يتعطل؟"},
    "all_apps_crashing": {"en": "Are multiple apps crashing?", "ar": "هل عدة تطبيقات تتعطل؟"},
    "games_crashing": {"en": "Do games specifically crash?", "ar": "هل الألعاب تحديداً تتعطل؟"},
    
    # Computer - Battery Issues
    "battery_drain_fast": {"en": "Is the battery draining faster than expected?", "ar": "هل البطارية تنفد أسرع من المتوقع؟"},
    "not_charging": {"en": "Is the laptop not charging?", "ar": "هل اللابتوب لا يشحن؟"},
    "battery_swollen": {"en": "Is the battery visibly swollen?", "ar": "هل البطارية منتفخة بشكل ملحوظ؟"},
    
    # Mobile - Battery Issues
    "battery_drain": {"en": "How fast is the battery draining?", "ar": "ما سرعة نفاد البطارية؟"},
    "screen_brightness": {"en": "Is screen brightness usually high?", "ar": "هل سطوع الشاشة عالي عادةً؟"},
    "background_apps": {"en": "Are there many apps running in background?", "ar": "هل هناك تطبيقات كثيرة تعمل في الخلفية؟"},
    "location_always_on": {"en": "Is location/GPS always on?", "ar": "هل الموقع/GPS يعمل دائماً؟"},
    "charging_slow": {"en": "Is charging slower than usual?", "ar": "هل الشحن أبطأ من المعتاد؟"},
    
    # Mobile - Overheating
    "hot_while_charging": {"en": "Does it get hot while charging?", "ar": "هل يسخن أثناء الشحن؟"},
    "hot_during_games": {"en": "Does it overheat during gaming?", "ar": "هل يسخن أثناء الألعاب؟"},
    "hot_always": {"en": "Is it always hot even during light use?", "ar": "هل ساخن دائماً حتى مع الاستخدام الخفيف؟"},
    
    # Mobile - Slow Performance
    "storage_full": {"en": "Is storage almost full?", "ar": "هل مساحة التخزين ممتلئة تقريباً؟"},
    "too_many_apps": {"en": "Are there many apps installed?", "ar": "هل هناك تطبيقات كثيرة مثبتة؟"},
    "ram_low": {"en": "Is available RAM usually low?", "ar": "هل الذاكرة المتاحة منخفضة عادةً؟"},
    
    # Mobile - Network Issues
    "wifi_not_connecting": {"en": "Is WiFi not connecting?", "ar": "هل الواي فاي لا يتصل؟"},
    "mobile_data_not_working": {"en": "Is mobile data not working?", "ar": "هل بيانات الموبايل لا تعمل؟"},
    "bluetooth_not_pairing": {"en": "Is Bluetooth not pairing?", "ar": "هل البلوتوث لا يقترن؟"},
    "no_signal": {"en": "Is there no cell signal?", "ar": "هل لا توجد إشارة؟"},
    
    # Mobile - Screen Problems
    "touch_not_responding": {"en": "Is touch not responding?", "ar": "هل اللمس لا يستجيب؟"},
    "ghost_touches": {"en": "Are there ghost/phantom touches?", "ar": "هل هناك لمسات وهمية؟"},
    "screen_flickering": {"en": "Is the screen flickering?", "ar": "هل الشاشة ترمش؟"},
    
    # Mobile - App Crashes
    "app_crashing": {"en": "Is a specific app crashing?", "ar": "هل تطبيق معين يتعطل؟"},
    "app_outdated": {"en": "Is the problematic app outdated?", "ar": "هل التطبيق المشكل قديم؟"},
    "multiple_apps_crashing": {"en": "Are multiple apps crashing?", "ar": "هل عدة تطبيقات تتعطل؟"},
    
    # Mobile - Storage Issues
    "storage_full_warning": {"en": "Is there a storage full warning?", "ar": "هل يظهر تحذير امتلاء التخزين؟"},
    "sd_card_not_detected": {"en": "Is SD card not detected?", "ar": "هل بطاقة SD لا يتم التعرف عليها؟"},
    
    # Mobile - Startup Failure
    "stuck_on_logo": {"en": "Is device stuck on logo?", "ar": "هل الجهاز عالق على الشعار؟"},
    "not_turning_on": {"en": "Is device not turning on?", "ar": "هل الجهاز لا يعمل؟"},
    "restarting_randomly": {"en": "Is device restarting randomly?", "ar": "هل الجهاز يعيد التشغيل عشوائياً؟"},
    
    # Mobile - Hardware Failure
    "camera_not_working": {"en": "Is the camera not working?", "ar": "هل الكاميرا لا تعمل؟"},
    "fingerprint_not_working": {"en": "Is fingerprint sensor not working?", "ar": "هل مستشعر البصمة لا يعمل؟"},
    "buttons_not_working": {"en": "Are physical buttons not working?", "ar": "هل الأزرار لا تعمل؟"},
}


def get_symptom_question(symptom_key: str, lang: str = "en") -> str:
    """Get translated symptom question."""
    question = SYMPTOM_QUESTIONS.get(symptom_key, {})
    return question.get(lang, question.get("en", symptom_key))
