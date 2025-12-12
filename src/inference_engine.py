"""
Inference Engine Module
=======================
This module implements the reasoning engine for the expert system.
It supports:
- Forward Chaining: Data-driven reasoning (symptoms → diagnosis)
- Backward Chaining: Goal-driven reasoning (hypothesis → verification)
- Explanation Facility: Generates human-readable explanations
"""

from typing import Dict, List, Optional, Tuple, Any
from .knowledge_base import KnowledgeBase


class InferenceEngine:
    """
    Inference Engine that applies rules to facts and generates diagnoses.
    
    Supports both forward and backward chaining reasoning strategies.
    """
    
    def __init__(self, knowledge_base: KnowledgeBase = None):
        """
        Initialize the Inference Engine.
        
        Args:
            knowledge_base: KnowledgeBase instance. If None, creates a new one.
        """
        self.kb = knowledge_base if knowledge_base else KnowledgeBase()
        self.working_memory: Dict[str, Any] = {}
        self.inference_trace: List[str] = []
        self.fired_rules: List[Dict] = []
    
    def reset(self) -> None:
        """Reset the inference engine state."""
        self.working_memory = {}
        self.inference_trace = []
        self.fired_rules = []
    
    def add_fact(self, key: str, value: Any) -> None:
        """
        Add a fact to working memory.
        
        Args:
            key: The fact name (e.g., 'fan_noise')
            value: The fact value (e.g., 'loud')
        """
        self.working_memory[key] = value
        self.inference_trace.append(f"Added fact: {key} = {value}")
    
    def add_facts(self, facts: Dict[str, Any]) -> None:
        """
        Add multiple facts to working memory.
        
        Args:
            facts: Dictionary of facts to add
        """
        for key, value in facts.items():
            self.add_fact(key, value)
    
    def forward_chain(self, device_type: str = None, 
                     category: str = None,
                     min_confidence: float = 0.5) -> List[Dict]:
        """
        Forward Chaining: Apply rules based on known facts.
        
        This is data-driven reasoning:
        1. Look at all known facts
        2. Find rules whose conditions match the facts
        3. Fire those rules and add conclusions
        
        Args:
            device_type: Filter rules by device type
            category: Filter rules by category
            min_confidence: Minimum confidence threshold
            
        Returns:
            List of diagnosis results with explanations
        """
        self.inference_trace.append("Starting Forward Chaining...")
        
        # Get matching rules from knowledge base
        matches = self.kb.find_matching_rules(
            user_symptoms=self.working_memory,
            device_type=device_type,
            category=category,
            min_match_score=min_confidence
        )
        
        diagnoses = []
        for match in matches:
            rule = match["rule"]
            match_score = match["match_score"]
            matched_conditions = match["matched_conditions"]
            
            # Calculate final confidence
            rule_confidence = rule.get("confidence", 0.8)
            final_confidence = match_score * rule_confidence
            
            if final_confidence >= min_confidence:
                self.fired_rules.append(rule)
                self.inference_trace.append(
                    f"Fired rule: {rule['id']} (confidence: {final_confidence:.2f})"
                )
                
                diagnosis = {
                    "rule_id": rule["id"],
                    "category": rule.get("category", "unknown"),
                    "cause": rule.get("cause", "Unknown cause"),
                    "cause_ar": rule.get("cause_ar", rule.get("cause", "Unknown cause")),
                    "solutions": rule.get("solutions", []),
                    "solutions_ar": rule.get("solutions_ar", rule.get("solutions", [])),
                    "confidence": final_confidence,
                    "matched_conditions": matched_conditions,
                    "explanation": self._generate_explanation(rule, matched_conditions)
                }
                diagnoses.append(diagnosis)
        
        self.inference_trace.append(f"Forward chaining complete. Found {len(diagnoses)} diagnoses.")
        return diagnoses
    
    def backward_chain(self, hypothesis: str, 
                      device_type: str = None) -> Tuple[bool, List[str]]:
        """
        Backward Chaining: Verify if a hypothesis can be proven.
        
        This is goal-driven reasoning:
        1. Start with a hypothesis (e.g., 'cooling_system_failure')
        2. Find rules that could prove this hypothesis
        3. Check if conditions are satisfied
        
        Args:
            hypothesis: The hypothesis to verify (cause to check)
            device_type: Filter rules by device type
            
        Returns:
            Tuple of (is_proven, required_facts)
        """
        self.inference_trace.append(f"Starting Backward Chaining for hypothesis: {hypothesis}")
        
        # Find rules that conclude this hypothesis
        rules = self.kb.get_rules_by_device(device_type) if device_type else self.kb.all_rules
        supporting_rules = [r for r in rules if hypothesis.lower() in r.get("cause", "").lower()]
        
        if not supporting_rules:
            self.inference_trace.append(f"No rules found that support hypothesis: {hypothesis}")
            return False, []
        
        for rule in supporting_rules:
            conditions = rule.get("conditions", {})
            required_facts = []
            all_satisfied = True
            
            for key, expected_value in conditions.items():
                if key in self.working_memory:
                    actual_value = self.working_memory[key]
                    if not self._values_match(actual_value, expected_value):
                        all_satisfied = False
                        required_facts.append(f"{key} should be {expected_value}")
                else:
                    required_facts.append(f"Need to know: {key}")
                    all_satisfied = False
            
            if all_satisfied:
                self.inference_trace.append(f"Hypothesis PROVEN by rule: {rule['id']}")
                return True, []
            else:
                self.inference_trace.append(
                    f"Rule {rule['id']} needs: {', '.join(required_facts)}"
                )
        
        return False, required_facts
    
    def _values_match(self, actual: Any, expected: Any) -> bool:
        """Check if two values match (with type flexibility)."""
        if isinstance(expected, bool):
            if isinstance(actual, str):
                return actual.lower() in ["yes", "true", "1"] if expected else actual.lower() in ["no", "false", "0"]
            return actual == expected
        elif isinstance(expected, str):
            return str(actual).lower() == expected.lower()
        else:
            return actual == expected
    
    def _generate_explanation(self, rule: Dict, matched_conditions: List[str]) -> str:
        """
        Generate a human-readable explanation for why a diagnosis was made.
        
        Args:
            rule: The fired rule
            matched_conditions: List of condition keys that matched
            
        Returns:
            Explanation string
        """
        conditions_text = []
        for cond in matched_conditions:
            value = self.working_memory.get(cond, "unknown")
            conditions_text.append(f"{cond.replace('_', ' ')} = {value}")
        
        if conditions_text:
            conditions_str = ", ".join(conditions_text)
            explanation = (
                f"The system concluded '{rule.get('cause', 'this issue')}' because "
                f"the following conditions were met: {conditions_str}."
            )
        else:
            explanation = f"The system identified a potential issue: {rule.get('cause', 'unknown')}."
        
        return explanation
    
    def diagnose(self, device_type: str, category: str, 
                symptoms: Dict[str, Any]) -> Dict:
        """
        Main diagnosis method - combines ML prediction with expert rules.
        
        Args:
            device_type: 'computer' or 'mobile'
            category: Problem category from ML classifier
            symptoms: Dictionary of symptoms collected from user
            
        Returns:
            Complete diagnosis result with solutions and explanation
        """
        self.reset()
        
        # Add all facts to working memory
        self.add_fact("device", device_type)
        self.add_facts(symptoms)
        
        # Run forward chaining
        diagnoses = self.forward_chain(
            device_type=device_type,
            category=category,
            min_confidence=0.3
        )
        
        if diagnoses:
            # Get the best diagnosis
            best = diagnoses[0]
            
            return {
                "success": True,
                "diagnosis": {
                    "cause": best["cause"],
                    "cause_ar": best.get("cause_ar", best["cause"]),
                    "category": best["category"],
                    "confidence": best["confidence"],
                    "solutions": best["solutions"],
                    "solutions_ar": best.get("solutions_ar", best["solutions"]),
                    "explanation": best["explanation"],
                    "rule_id": best["rule_id"]
                },
                "alternative_diagnoses": diagnoses[1:3] if len(diagnoses) > 1 else [],
                "inference_trace": self.inference_trace
            }
        else:
            # No specific rule matched - provide general advice
            return {
                "success": False,
                "diagnosis": {
                    "cause": f"General {category.replace('_', ' ')} issue",
                    "category": category,
                    "confidence": 0.5,
                    "solutions": self._get_general_solutions(category, device_type),
                    "explanation": (
                        f"Based on the symptoms provided, this appears to be a "
                        f"{category.replace('_', ' ')} problem. Consider the general "
                        f"troubleshooting steps recommended."
                    ),
                    "rule_id": None
                },
                "alternative_diagnoses": [],
                "inference_trace": self.inference_trace
            }
    
    def _get_general_solutions(self, category: str, device_type: str) -> List[str]:
        """Get general solutions for a category when no specific rule matches."""
        general_solutions = {
            "overheating": [
                "Ensure proper ventilation around the device",
                "Clean dust from vents and fans",
                "Avoid using in direct sunlight or hot environments",
                "Consider replacing thermal paste (for computers)",
            ],
            "slow_performance": [
                "Close unused applications",
                "Restart the device",
                "Check for available updates",
                "Free up storage space",
                "Scan for malware",
            ],
            "battery_issues": [
                "Check battery health in settings",
                "Reduce screen brightness",
                "Close background applications",
                "Use original charger",
                "Consider battery replacement if old",
            ],
            "network_issues": [
                "Toggle airplane mode on and off",
                "Restart the router/modem",
                "Forget and reconnect to network",
                "Update network drivers",
                "Check for service outages",
            ],
            "startup_failure": [
                "Perform a hard reset",
                "Check power connections",
                "Try booting in safe mode",
                "Check for recent hardware changes",
            ],
            "screen_problems": [
                "Restart the device",
                "Check display connections",
                "Adjust display settings",
                "Update display drivers",
            ],
            "storage_issues": [
                "Delete unnecessary files",
                "Clear app caches",
                "Move files to cloud storage",
                "Check for disk errors",
            ],
            "audio_problems": [
                "Check volume settings",
                "Ensure correct output device is selected",
                "Update audio drivers",
                "Test with different audio source",
            ],
            "app_crashes": [
                "Update the application",
                "Clear app cache and data",
                "Reinstall the application",
                "Check for system updates",
            ],
            "hardware_failure": [
                "Restart the device",
                "Check all connections",
                "Run hardware diagnostics",
                "Consult a professional technician",
            ],
        }
        return general_solutions.get(category, ["Restart the device and try again", "Consult technical support"])
    
    def get_trace(self) -> str:
        """Get the complete inference trace as a formatted string."""
        return "\n".join(self.inference_trace)


if __name__ == "__main__":
    # Test the inference engine
    engine = InferenceEngine()
    
    print("=== Testing Inference Engine ===\n")
    
    # Test forward chaining
    test_symptoms = {
        "fan_noise": "loud",
        "hot_surface": True,
        "thermal_paste_old": True
    }
    
    result = engine.diagnose(
        device_type="computer",
        category="overheating",
        symptoms=test_symptoms
    )
    
    print("Diagnosis Result:")
    print(f"  Cause: {result['diagnosis']['cause']}")
    print(f"  Confidence: {result['diagnosis']['confidence']:.2%}")
    print(f"  Solutions:")
    for sol in result['diagnosis']['solutions']:
        print(f"    - {sol}")
    print(f"\n  Explanation: {result['diagnosis']['explanation']}")
    
    print("\n" + "="*50 + "\n")
    
    # Test backward chaining
    engine.reset()
    engine.add_facts(test_symptoms)
    engine.add_fact("device", "computer")
    
    is_proven, needed = engine.backward_chain("Dust accumulation", "computer")
    print(f"Hypothesis 'Dust accumulation' proven: {is_proven}")
    if needed:
        print(f"  Still needed: {needed}")
