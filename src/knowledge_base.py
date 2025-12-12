"""
Knowledge Base Module
=====================
This module handles loading and managing the rules for both 
computer and mobile device troubleshooting.

The knowledge base contains:
- 50+ rules for computer problems
- 40+ rules for mobile problems
- Each rule has: conditions, cause, solutions, confidence
"""

import json
import os
from typing import Dict, List, Optional, Any


class KnowledgeBase:
    """
    Knowledge Base class that stores and manages troubleshooting rules.
    
    Attributes:
        computer_rules (List[Dict]): Rules for computer troubleshooting
        mobile_rules (List[Dict]): Rules for mobile troubleshooting
        all_rules (List[Dict]): Combined rules from both categories
    """
    
    def __init__(self, data_dir: str = None):
        """
        Initialize the Knowledge Base.
        
        Args:
            data_dir: Path to the data directory containing rule files.
                     If None, uses the default 'data' folder.
        """
        if data_dir is None:
            # Get the directory where this file is located
            current_dir = os.path.dirname(os.path.abspath(__file__))
            data_dir = os.path.join(os.path.dirname(current_dir), "data")
        
        self.data_dir = data_dir
        self.computer_rules: List[Dict] = []
        self.mobile_rules: List[Dict] = []
        self.all_rules: List[Dict] = []
        
        # Load rules on initialization
        self._load_rules()
    
    def _load_rules(self) -> None:
        """Load rules from JSON files."""
        # Load computer rules
        computer_file = os.path.join(self.data_dir, "computer_rules.json")
        if os.path.exists(computer_file):
            with open(computer_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.computer_rules = data.get("rules", [])
        
        # Load mobile rules
        mobile_file = os.path.join(self.data_dir, "mobile_rules.json")
        if os.path.exists(mobile_file):
            with open(mobile_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.mobile_rules = data.get("rules", [])
        
        # Combine all rules
        self.all_rules = self.computer_rules + self.mobile_rules
        
        print(f"Loaded {len(self.computer_rules)} computer rules")
        print(f"Loaded {len(self.mobile_rules)} mobile rules")
        print(f"Total rules: {len(self.all_rules)}")
    
    def get_rules_by_device(self, device_type: str) -> List[Dict]:
        """
        Get rules filtered by device type.
        
        Args:
            device_type: Either 'computer' or 'mobile'
            
        Returns:
            List of rules for the specified device type
        """
        if device_type.lower() == "computer":
            return self.computer_rules
        elif device_type.lower() == "mobile":
            return self.mobile_rules
        else:
            return self.all_rules
    
    def get_rules_by_category(self, category: str, device_type: str = None) -> List[Dict]:
        """
        Get rules filtered by problem category.
        
        Args:
            category: Problem category (e.g., 'overheating', 'slow_performance')
            device_type: Optional device type filter
            
        Returns:
            List of rules matching the category
        """
        if device_type:
            rules = self.get_rules_by_device(device_type)
        else:
            rules = self.all_rules
        
        return [rule for rule in rules if rule.get("category") == category]
    
    def get_rule_by_id(self, rule_id: str) -> Optional[Dict]:
        """
        Get a specific rule by its ID.
        
        Args:
            rule_id: The unique identifier of the rule
            
        Returns:
            The rule dict or None if not found
        """
        for rule in self.all_rules:
            if rule.get("id") == rule_id:
                return rule
        return None
    
    def get_all_categories(self) -> List[str]:
        """
        Get a list of all unique problem categories.
        
        Returns:
            List of category names
        """
        categories = set()
        for rule in self.all_rules:
            if "category" in rule:
                categories.add(rule["category"])
        return sorted(list(categories))
    
    def get_symptoms_for_category(self, category: str, device_type: str = None) -> List[str]:
        """
        Get all possible symptoms for a given category.
        
        Args:
            category: The problem category
            device_type: Optional device type filter
            
        Returns:
            List of symptom keys from rule conditions
        """
        rules = self.get_rules_by_category(category, device_type)
        symptoms = set()
        
        for rule in rules:
            conditions = rule.get("conditions", {})
            for key in conditions.keys():
                if key not in ["device"]:  # Exclude device from symptoms
                    symptoms.add(key)
        
        return sorted(list(symptoms))
    
    def match_conditions(self, rule: Dict, user_symptoms: Dict) -> tuple:
        """
        Check if user symptoms match a rule's conditions.
        
        Args:
            rule: The rule to check
            user_symptoms: Dict of symptoms provided by user
            
        Returns:
            Tuple of (match_score, matched_conditions, unmatched_conditions)
        """
        conditions = rule.get("conditions", {})
        matched = []
        unmatched = []
        
        for key, expected_value in conditions.items():
            if key in user_symptoms:
                user_value = user_symptoms[key]
                
                # Handle different types of matching
                if isinstance(expected_value, bool):
                    if user_value == expected_value:
                        matched.append(key)
                    else:
                        unmatched.append(key)
                elif isinstance(expected_value, str):
                    # Partial string matching
                    if str(user_value).lower() == expected_value.lower():
                        matched.append(key)
                    else:
                        unmatched.append(key)
                else:
                    if user_value == expected_value:
                        matched.append(key)
                    else:
                        unmatched.append(key)
            else:
                # Condition not provided by user
                unmatched.append(key)
        
        # Calculate match score
        total_conditions = len(conditions)
        if total_conditions == 0:
            match_score = 0
        else:
            match_score = len(matched) / total_conditions
        
        return match_score, matched, unmatched
    
    def find_matching_rules(self, user_symptoms: Dict, 
                           device_type: str = None,
                           category: str = None,
                           min_match_score: float = 0.5) -> List[Dict]:
        """
        Find rules that match the user's symptoms.
        
        Args:
            user_symptoms: Dict of symptoms provided by user
            device_type: Optional device type filter
            category: Optional category filter
            min_match_score: Minimum match score to include rule (0.0 to 1.0)
            
        Returns:
            List of matching rules with match info, sorted by score
        """
        # Get relevant rules
        if category:
            rules = self.get_rules_by_category(category, device_type)
        elif device_type:
            rules = self.get_rules_by_device(device_type)
        else:
            rules = self.all_rules
        
        matches = []
        for rule in rules:
            match_score, matched, unmatched = self.match_conditions(rule, user_symptoms)
            
            if match_score >= min_match_score:
                matches.append({
                    "rule": rule,
                    "match_score": match_score,
                    "matched_conditions": matched,
                    "unmatched_conditions": unmatched
                })
        
        # Sort by match score (highest first) and then by rule confidence
        matches.sort(key=lambda x: (x["match_score"], x["rule"].get("confidence", 0)), reverse=True)
        
        return matches


# ----- Symptom definitions for the chatbot -----
COMPUTER_SYMPTOMS = {
    "overheating": [
        ("fan_noise", "Is the fan making loud noise?", ["yes", "no", "sometimes"]),
        ("hot_surface", "Is the device hot to touch?", ["yes", "no"]),
        ("thermal_paste_old", "Is the computer more than 3 years old without thermal paste change?", ["yes", "no", "unsure"]),
        ("poor_ventilation", "Is the computer in an enclosed or dusty area?", ["yes", "no"]),
        ("high_cpu_usage", "Is CPU usage constantly high?", ["yes", "no", "unsure"]),
    ],
    "slow_performance": [
        ("ram_usage", "Is RAM usage high (above 80%)?", ["high", "normal", "unsure"]),
        ("hdd_type", "What type of storage does the computer have?", ["mechanical", "ssd", "unsure"]),
        ("startup_programs", "Are there many programs that start with Windows?", ["many", "few", "unsure"]),
        ("malware_detected", "Has any malware been detected recently?", ["yes", "no", "unsure"]),
        ("os_outdated", "Is the operating system outdated?", ["yes", "no", "unsure"]),
    ],
    "startup_failure": [
        ("power_led", "Is the power LED on?", ["on", "off", "blinking"]),
        ("beep_codes", "Are there any beep sounds on startup?", ["yes", "no"]),
        ("boot_loop", "Does the computer restart repeatedly?", ["yes", "no"]),
        ("black_screen", "Is the screen completely black?", ["yes", "no"]),
        ("fans_running", "Are the fans running?", ["yes", "no"]),
    ],
    "network_issues": [
        ("adapter_disabled", "Is the network adapter enabled?", ["yes", "no", "unsure"]),
        ("dns_error", "Are you getting DNS errors?", ["yes", "no", "unsure"]),
        ("ethernet_no_connection", "Is this an ethernet connection issue?", ["yes", "no"]),
        ("driver_outdated", "Are network drivers updated?", ["yes", "no", "unsure"]),
    ],
    "screen_problems": [
        ("flickering", "Is the screen flickering?", ["yes", "no"]),
        ("dead_pixels", "Are there dead or stuck pixels?", ["yes", "no"]),
        ("dim_display", "Is the display unusually dim?", ["yes", "no"]),
        ("color_distortion", "Are colors displayed incorrectly?", ["yes", "no"]),
    ],
    "storage_issues": [
        ("disk_full", "Is the disk almost full?", ["yes", "no"]),
        ("drive_not_detected", "Is a drive not being detected?", ["yes", "no"]),
        ("disk_read_errors", "Are there disk read/write errors?", ["yes", "no", "unsure"]),
    ],
    "audio_problems": [
        ("no_sound", "Is there no sound at all?", ["yes", "no"]),
        ("crackling_audio", "Is the audio crackling or distorted?", ["yes", "no"]),
        ("headphones_not_detected", "Are headphones/speakers not detected?", ["yes", "no"]),
    ],
    "hardware_failure": [
        ("blue_screen", "Are you getting blue screen errors?", ["yes", "no"]),
        ("usb_ports_dead", "Are USB ports not working?", ["yes", "no"]),
        ("random_shutdowns", "Does the computer shut down randomly?", ["yes", "no"]),
        ("clicking_sounds", "Are there clicking sounds from the computer?", ["yes", "no"]),
    ],
    "app_crashes": [
        ("specific_app", "Is only one specific app crashing?", ["yes", "no"]),
        ("all_apps_crashing", "Are multiple apps crashing?", ["yes", "no"]),
        ("games_crashing", "Do games specifically crash?", ["yes", "no"]),
    ],
    "battery_issues": [
        ("battery_drain_fast", "Is the battery draining faster than expected?", ["yes", "no"]),
        ("not_charging", "Is the laptop not charging?", ["yes", "no"]),
        ("battery_swollen", "Is the battery visibly swollen?", ["yes", "no"]),
    ],
}

MOBILE_SYMPTOMS = {
    "battery_issues": [
        ("battery_drain", "How fast is the battery draining?", ["fast", "normal", "slow"]),
        ("screen_brightness", "Is screen brightness usually high?", ["high", "medium", "low"]),
        ("background_apps", "Are there many apps running in background?", ["many", "few", "unsure"]),
        ("location_always_on", "Is location/GPS always on?", ["yes", "no"]),
        ("charging_slow", "Is charging slower than usual?", ["yes", "no"]),
    ],
    "overheating": [
        ("hot_while_charging", "Does it get hot while charging?", ["yes", "no"]),
        ("hot_during_games", "Does it overheat during gaming?", ["yes", "no"]),
        ("hot_always", "Is it always hot even during light use?", ["yes", "no"]),
    ],
    "slow_performance": [
        ("storage_full", "Is storage almost full?", ["yes", "no", "unsure"]),
        ("too_many_apps", "Are there many apps installed?", ["yes", "no"]),
        ("os_outdated", "Is the OS outdated?", ["yes", "no", "unsure"]),
        ("ram_low", "Is available RAM usually low?", ["yes", "no", "unsure"]),
    ],
    "network_issues": [
        ("wifi_not_connecting", "Is WiFi not connecting?", ["yes", "no"]),
        ("mobile_data_not_working", "Is mobile data not working?", ["yes", "no"]),
        ("bluetooth_not_pairing", "Is Bluetooth not pairing?", ["yes", "no"]),
        ("no_signal", "Is there no cell signal?", ["yes", "no"]),
    ],
    "screen_problems": [
        ("touch_not_responding", "Is touch not responding?", ["yes", "no", "sometimes"]),
        ("ghost_touches", "Are there ghost/phantom touches?", ["yes", "no"]),
        ("screen_flickering", "Is the screen flickering?", ["yes", "no"]),
    ],
    "app_crashes": [
        ("app_crashing", "Is a specific app crashing?", ["yes", "no"]),
        ("app_outdated", "Is the problematic app outdated?", ["yes", "no", "unsure"]),
        ("multiple_apps_crashing", "Are multiple apps crashing?", ["yes", "no"]),
    ],
    "storage_issues": [
        ("storage_full_warning", "Is there a storage full warning?", ["yes", "no"]),
        ("sd_card_not_detected", "Is SD card not detected?", ["yes", "no", "no_sd"]),
    ],
    "audio_problems": [
        ("no_sound", "Is there no sound from speakers?", ["yes", "no"]),
        ("headphones_not_detected", "Are headphones not detected?", ["yes", "no"]),
    ],
    "startup_failure": [
        ("stuck_on_logo", "Is device stuck on logo?", ["yes", "no"]),
        ("not_turning_on", "Is device not turning on?", ["yes", "no"]),
        ("restarting_randomly", "Is device restarting randomly?", ["yes", "no"]),
    ],
    "hardware_failure": [
        ("camera_not_working", "Is the camera not working?", ["yes", "no"]),
        ("fingerprint_not_working", "Is fingerprint sensor not working?", ["yes", "no"]),
        ("buttons_not_working", "Are physical buttons not working?", ["yes", "no"]),
    ],
}


def get_symptoms_for_device_category(device_type: str, category: str) -> List[tuple]:
    """
    Get the symptom questions for a specific device type and category.
    
    Args:
        device_type: 'computer' or 'mobile'
        category: The problem category
        
    Returns:
        List of (symptom_key, question, options) tuples
    """
    if device_type.lower() == "computer":
        return COMPUTER_SYMPTOMS.get(category, [])
    else:
        return MOBILE_SYMPTOMS.get(category, [])


if __name__ == "__main__":
    # Test the knowledge base
    kb = KnowledgeBase()
    
    print("\n--- Categories ---")
    print(kb.get_all_categories())
    
    print("\n--- Sample Computer Overheating Rules ---")
    rules = kb.get_rules_by_category("overheating", "computer")
    for rule in rules[:2]:
        print(f"  {rule['id']}: {rule['cause']}")
    
    print("\n--- Testing Rule Matching ---")
    test_symptoms = {
        "device": "computer",
        "fan_noise": "loud",
        "hot_surface": True
    }
    matches = kb.find_matching_rules(test_symptoms, device_type="computer", category="overheating")
    for match in matches[:2]:
        print(f"  Match: {match['rule']['id']} (score: {match['match_score']:.2f})")
        print(f"  Cause: {match['rule']['cause']}")
