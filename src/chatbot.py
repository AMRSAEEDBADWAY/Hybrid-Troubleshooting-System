"""
Chatbot Module
==============
This module implements the interactive chatbot that guides users
through the troubleshooting process by:
1. Collecting device type
2. Getting problem description
3. Asking follow-up symptom questions
4. Passing data to ML + Expert System
5. Displaying diagnosis and explanation
"""

from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from dataclasses import dataclass, field

from .ml_model import TroubleshootingClassifier
from .inference_engine import InferenceEngine
from .knowledge_base import KnowledgeBase, get_symptoms_for_device_category
from .translations import get_text, get_symptom_question, get_category_name


class ChatState(Enum):
    """Enumeration of chatbot conversation states."""
    START = "start"
    DEVICE_SELECTION = "device_selection"
    PROBLEM_DESCRIPTION = "problem_description"
    SYMPTOM_QUESTIONS = "symptom_questions"
    ADDITIONAL_INFO = "additional_info"
    DIAGNOSIS = "diagnosis"
    COMPLETE = "complete"


@dataclass
class ConversationContext:
    """Stores the context of the current conversation."""
    state: ChatState = ChatState.START
    device_type: Optional[str] = None
    problem_description: Optional[str] = None
    predicted_category: Optional[str] = None
    prediction_confidence: float = 0.0
    symptoms: Dict[str, Any] = field(default_factory=dict)
    current_symptom_index: int = 0
    symptom_questions: List[tuple] = field(default_factory=list)
    diagnosis_result: Optional[Dict] = None
    chat_history: List[Dict[str, str]] = field(default_factory=list)


class TroubleshootingChatbot:
    """
    Interactive chatbot for device troubleshooting.
    
    Guides users through a conversation to:
    1. Identify the type of device
    2. Understand the problem
    3. Collect relevant symptoms
    4. Provide diagnosis and recommendations
    """
    
    def __init__(self):
        """Initialize the chatbot with ML model and inference engine."""
        self.classifier = TroubleshootingClassifier()
        self.knowledge_base = KnowledgeBase()
        self.inference_engine = InferenceEngine(self.knowledge_base)
        self.context = ConversationContext()
        
        # Ensure model is ready
        if not self.classifier.is_trained:
            if not self.classifier.load_model():
                print("Training ML model...")
                self.classifier.train_model()
    
    def reset(self) -> None:
        """Reset the conversation to start state."""
        self.context = ConversationContext()
        self.inference_engine.reset()
    
    def add_to_history(self, role: str, message: str) -> None:
        """Add a message to chat history."""
        self.context.chat_history.append({
            "role": role,
            "message": message
        })
    
    def get_greeting(self, lang: str = "en") -> str:
        """Get the initial greeting message in specified language."""
        if lang == "ar":
            greeting = f"""👋 **{get_text('welcome', lang)}**

{get_text('welcome_help', lang)}

**{get_text('lets_start', lang)}**

{get_text('select_device', lang)}

- 💻 **{get_text('computer_option', lang)}**
- 📱 **{get_text('mobile_option', lang)}**"""
        else:
            greeting = f"""👋 **{get_text('welcome', lang)}**

{get_text('welcome_help', lang)}

**{get_text('lets_start', lang)}**

{get_text('select_device', lang)}

- 💻 **{get_text('computer_option', lang)}**
- 📱 **{get_text('mobile_option', lang)}**"""
        
        self.context.state = ChatState.DEVICE_SELECTION
        return greeting
    
    def process_device_selection(self, user_input: str, lang: str = "en") -> str:
        """Process device type selection (supports Arabic & English)."""
        user_input_lower = user_input.lower().strip()
        
        # English and Arabic keywords for computer
        computer_keywords = ["computer", "pc", "laptop", "desktop", "windows", "mac", 
                            "كمبيوتر", "لابتوب", "حاسوب", "كومبيوتر", "لاب توب", "حاسب"]
        # English and Arabic keywords for mobile
        mobile_keywords = ["mobile", "phone", "android", "iphone", "ios", "tablet", "smartphone",
                          "موبايل", "تليفون", "هاتف", "جوال", "تلفون", "اندرويد", "ايفون", "تابلت"]
        
        if any(word in user_input_lower for word in computer_keywords):
            self.context.device_type = "computer"
            device_name = get_text('computer_button', lang)
            example1 = get_text('computer_example1', lang)
            example2 = get_text('computer_example2', lang)
            example3 = get_text('computer_example3', lang)
        elif any(word in user_input_lower for word in mobile_keywords):
            self.context.device_type = "mobile"
            device_name = get_text('mobile_button', lang)
            example1 = get_text('mobile_example1', lang)
            example2 = get_text('mobile_example2', lang)
            example3 = get_text('mobile_example3', lang)
        else:
            msg = f"""{get_text('didnt_understand', lang)}

- {get_text('type_computer', lang)}
- {get_text('type_mobile', lang)}"""
            return msg
        
        self.context.state = ChatState.PROBLEM_DESCRIPTION
        
        msg = f"""{get_text('great_troubleshooting', lang)} **{device_name}**.

{get_text('describe_problem_detail', lang)}

{get_text('examples', lang)}
- {example1}
- {example2}
- {example3}"""
        return msg

    
    def process_problem_description(self, user_input: str, lang: str = "en") -> str:
        """Process the problem description and classify it."""
        self.context.problem_description = user_input
        
        # Use ML model to classify the problem
        prediction = self.classifier.predict_with_confidence(user_input)
        
        self.context.predicted_category = prediction["predicted_category"]
        self.context.prediction_confidence = prediction["confidence"]
        
        # Get symptom questions for this category
        self.context.symptom_questions = get_symptoms_for_device_category(
            self.context.device_type,
            self.context.predicted_category
        )
        
        category_display = get_category_name(self.context.predicted_category, lang)
        confidence_display = f"{self.context.prediction_confidence:.0%}"
        
        if self.context.symptom_questions:
            self.context.state = ChatState.SYMPTOM_QUESTIONS
            self.context.current_symptom_index = 0
            
            # Get first question
            first_question = self._get_current_symptom_question(lang)
            
            return f"""{get_text('initial_analysis', lang)}
{get_text('appears_to_be', lang)} **{category_display}** {get_text('issue', lang)}
({get_text('confidence', lang)}: {confidence_display})

{get_text('followup_questions', lang)}

{first_question}"""
        else:
            # No symptom questions available, go directly to diagnosis
            return self._generate_diagnosis(lang)
    
    def _get_current_symptom_question(self, lang: str = "en") -> str:
        """Get the current symptom question formatted for display."""
        if self.context.current_symptom_index >= len(self.context.symptom_questions):
            return ""
        
        symptom_key, question, options = self.context.symptom_questions[self.context.current_symptom_index]
        
        question_num = self.context.current_symptom_index + 1
        total_questions = len(self.context.symptom_questions)
        
        # Get translated question
        translated_question = get_symptom_question(symptom_key, lang)
        options_display = " / ".join([f"**{opt}**" for opt in options])
        
        return f"""**{get_text('question', lang)} {question_num}/{total_questions}:**
{translated_question}

{get_text('options', lang)}: {options_display}"""
    
    def process_symptom_response(self, user_input: str, lang: str = "en") -> str:
        """Process a symptom question response."""
        if self.context.current_symptom_index >= len(self.context.symptom_questions):
            return self._generate_diagnosis(lang)
        
        symptom_key, question, options = self.context.symptom_questions[self.context.current_symptom_index]
        
        # Try to match user input to options
        user_input_lower = user_input.lower().strip()
        matched_option = None
        
        for option in options:
            if option.lower() in user_input_lower or user_input_lower in option.lower():
                matched_option = option
                break
        
        if matched_option is None:
            # Try fuzzy matching (English + Arabic)
            yes_words = ["y", "yeah", "yep", "yup", "affirmative", "اه", "ايوه", "نعم", "اة", "صح", "ايوا", "اي"]
            no_words = ["n", "nope", "nah", "negative", "لا", "لأ", "مش", "مفيش", "ابدا"]
            
            if user_input_lower in yes_words:
                matched_option = "yes"
            elif user_input_lower in no_words:
                matched_option = "no"
            else:
                matched_option = user_input_lower
        
        # Store the symptom
        self.context.symptoms[symptom_key] = matched_option
        
        # Move to next question
        self.context.current_symptom_index += 1
        
        if self.context.current_symptom_index < len(self.context.symptom_questions):
            next_question = self._get_current_symptom_question(lang)
            return f"{get_text('got_it', lang)} {next_question}"
        else:
            # All questions answered, generate diagnosis
            return self._generate_diagnosis(lang)
    
    def _generate_diagnosis(self, lang: str = "en") -> str:
        """Generate the final diagnosis using the inference engine."""
        self.context.state = ChatState.DIAGNOSIS
        
        # Run the inference engine
        result = self.inference_engine.diagnose(
            device_type=self.context.device_type,
            category=self.context.predicted_category,
            symptoms=self.context.symptoms
        )
        
        self.context.diagnosis_result = result
        self.context.state = ChatState.COMPLETE
        
        diagnosis = result["diagnosis"]
        category_display = get_category_name(diagnosis['category'], lang)
        
        # Format solutions
        solutions_list = "\n".join([f"   {i+1}. {sol}" for i, sol in enumerate(diagnosis["solutions"])])
        
        # Format confidence
        confidence_pct = f"{diagnosis['confidence']:.0%}"
        
        # Check for alternatives
        alternatives_text = ""
        if result.get("alternative_diagnoses"):
            alt_list = []
            for alt in result["alternative_diagnoses"][:2]:
                alt_list.append(f"   - {alt['cause']} ({alt['confidence']:.0%})")
            alt_header = get_text('alternatives', lang)
            alternatives_text = f"\n\n**{alt_header}:**\n" + "\n".join(alt_list)
        
        return f"""
🔍 **{get_text('diagnosis_header', lang)}**
{'='*50}

**{get_text('identified_issue', lang)}:**
🎯 {diagnosis['cause']}

**{get_text('category', lang)}:** {category_display}
**{get_text('confidence', lang)}:** {confidence_pct}

**{get_text('solutions', lang)}:**
{solutions_list}

**{get_text('explanation_label', lang)}:**
{diagnosis['explanation']}{alternatives_text}

{'='*50}
{get_text('what_next', lang)}
- {get_text('type_new', lang)}
- {get_text('type_details', lang)}
- {get_text('type_exit', lang)}"""
    
    def process_message(self, user_input: str, lang: str = "en") -> str:
        """
        Main method to process user messages.
        
        Args:
            user_input: The user's message
            lang: Language code ('en' or 'ar')
            
        Returns:
            The chatbot's response
        """
        user_input = user_input.strip()
        
        # Add to history
        self.add_to_history("user", user_input)
        
        # Check for special commands
        user_input_lower = user_input.lower()
        
        if user_input_lower in ["new", "restart", "reset", "start over", "جديد", "من الاول", "اعادة"]:
            self.reset()
            response = self.get_greeting(lang)
            self.add_to_history("assistant", response)
            return response
        
        if user_input_lower in ["exit", "quit", "bye", "goodbye", "خروج", "باي", "مع السلامة"]:
            response = get_text('goodbye', lang)
            self.add_to_history("assistant", response)
            return response
        
        if user_input_lower in ["details", "تفاصيل"] and self.context.state == ChatState.COMPLETE:
            response = self._get_technical_details(lang)
            self.add_to_history("assistant", response)
            return response
        
        # Process based on current state
        if self.context.state == ChatState.START:
            response = self.get_greeting(lang)
        
        elif self.context.state == ChatState.DEVICE_SELECTION:
            response = self.process_device_selection(user_input, lang)
        
        elif self.context.state == ChatState.PROBLEM_DESCRIPTION:
            response = self.process_problem_description(user_input, lang)
        
        elif self.context.state == ChatState.SYMPTOM_QUESTIONS:
            response = self.process_symptom_response(user_input, lang)
        
        elif self.context.state == ChatState.COMPLETE:
            response = f"""{get_text('already_diagnosed', lang)}

{get_text('what_next', lang)}
- {get_text('type_new', lang)}
- {get_text('type_details', lang)}
- {get_text('type_exit', lang)}"""
        
        else:
            response = get_text('not_sure', lang)
        
        # Add to history
        self.add_to_history("assistant", response)
        
        return response
    
    def _get_technical_details(self, lang: str = "en") -> str:
        """Get technical details about the diagnosis."""
        if not self.context.diagnosis_result:
            return get_text('no_symptoms', lang) if lang == "ar" else "No diagnosis available yet."
        
        result = self.context.diagnosis_result
        diagnosis = result["diagnosis"]
        
        # Build inference trace
        trace = "\n".join(self.inference_engine.inference_trace[-10:])  # Last 10 steps
        
        symptoms_text = "\n".join([f"   - {k}: {v}" for k, v in self.context.symptoms.items()])
        no_symptoms = get_text('no_symptoms', lang)
        
        return f"""
📋 **{get_text('technical_details', lang)}**
{'='*50}

**{get_text('device_type', lang)}:** {self.context.device_type}
**{get_text('predicted_category', lang)}:** {get_category_name(self.context.predicted_category, lang)}
**{get_text('ml_confidence', lang)}:** {self.context.prediction_confidence:.2%}

**{get_text('collected_symptoms', lang)}:**
{symptoms_text if symptoms_text else f"   {no_symptoms}"}

**{get_text('rule_id', lang)}:** {diagnosis.get('rule_id', 'N/A')}
**{get_text('final_confidence', lang)}:** {diagnosis['confidence']:.2%}

**{get_text('inference_trace', lang)}:**
```
{trace}
```
{'='*50}"""
    
    def get_chat_history(self) -> List[Dict[str, str]]:
        """Get the complete chat history."""
        return self.context.chat_history
    
    def get_context_summary(self) -> Dict:
        """Get a summary of the current conversation context."""
        return {
            "state": self.context.state.value,
            "device_type": self.context.device_type,
            "predicted_category": self.context.predicted_category,
            "symptoms_collected": len(self.context.symptoms),
            "has_diagnosis": self.context.diagnosis_result is not None
        }


if __name__ == "__main__":
    # Interactive test
    print("=" * 60)
    print("Troubleshooting Chatbot - Interactive Test")
    print("=" * 60)
    
    chatbot = TroubleshootingChatbot()
    
    # Start conversation
    print("\n" + chatbot.get_greeting())
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if not user_input:
            continue
        
        response = chatbot.process_message(user_input)
        print(f"\nAssistant: {response}")
        
        if "goodbye" in response.lower():
            break
