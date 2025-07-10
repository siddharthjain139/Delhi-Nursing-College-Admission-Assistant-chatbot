import streamlit as st
import re

# Define the assistant class
class NursingAdmissionAssistant:
    def __init__(self):
        self.current_state = st.session_state.get("current_state", "initial_greeting")
        self.conversation_active = st.session_state.get("conversation_active", True)
        self.context_stack = st.session_state.get("context_stack", [])
        self.previous_intents = st.session_state.get("previous_intents", [])
        self.entity_memory = st.session_state.get("entity_memory", {
            'user_has_biology': None,
            'interested_in_program': None
        })
        
        self.positive_responses = {
            'yes', 'haan', 'y', 'h', 'ok', 'okay', 'continue', 
            'more', 'batao', 'tell me more', 'kya hai', 'please',
            'sure', 'go ahead', 'proceed'
        }
        self.negative_responses = {
            'no', 'nahi', 'n', 'stop', 'end', 'quit', 
            'not now', 'later', 'exit', 'enough', 'cancel'
        }

    def normalize_input(self, text):
        text = text.lower()
        text = re.sub(r'[^a-z0-9\u0900-\u097f\s]', '', text)
        text = ' '.join(text.split())
        synonym_map = {
            'yeah': 'yes', 'nhi': 'no', 'ha': 'yes',
            'yup': 'yes', 'nah': 'no', 'not': 'no'
        }
        for key, value in synonym_map.items():
            text = text.replace(key, value)
        return text

    def is_positive(self, text):
        return any(pos in text for pos in self.positive_responses)

    def is_negative(self, text):
        return any(neg in text for neg in self.negative_responses)

    def update_state(self, key, value):
        st.session_state[key] = value

    def add_bot_message(self, msg):
        st.session_state.chat_history.append(("Assistant", msg))

    def handle_response(self, user_input):
        norm_input = self.normalize_input(user_input)

        if not st.session_state.conversation_active:
            return

        # Contextual triggers
        if self.current_state != "additional_help":
            if 'fee' in norm_input:
                return self.handle_fee_structure("yes")
            elif 'hostel' in norm_input:
                return self.handle_hostel_facilities("yes")
            elif 'location' in norm_input:
                return self.handle_college_location("yes")
            elif 'scholar' in norm_input:
                return self.handle_scholarships("yes")
            elif 'admis' in norm_input:
                return self.handle_admission_details("yes")

        # State routing
        if self.current_state == "initial_greeting":
            self.handle_initial_greeting(norm_input)
        elif self.current_state == "biology_check":
            self.handle_biology_check(norm_input)
        elif self.current_state == "program_details":
            self.handle_program_details(norm_input)
        elif self.current_state == "fee_structure":
            self.handle_fee_structure(norm_input)
        elif self.current_state == "hostel_facilities":
            self.handle_hostel_facilities(norm_input)
        elif self.current_state == "college_location":
            self.handle_college_location(norm_input)
        elif self.current_state == "recognition":
            self.handle_recognition(norm_input)
        elif self.current_state == "clinical_training":
            self.handle_clinical_training(norm_input)
        elif self.current_state == "scholarships":
            self.handle_scholarships(norm_input)
        elif self.current_state == "admission_details":
            self.handle_admission_details(norm_input)
        elif self.current_state == "final":
            self.handle_final_response(norm_input)
        elif self.current_state == "additional_help":
            self.handle_additional_help(norm_input)

    # State handlers
    def handle_initial_greeting(self, text):
        if self.is_positive(text):
            self.update_state("current_state", "biology_check")
            self.add_bot_message("Did you study Biology in your 12th grade? (Yes/No)")
        elif self.is_negative(text):
            self.end_conversation()
        else:
            self.add_bot_message("Please respond with Yes/Haan or No/Nahi.")

    def handle_biology_check(self, text):
        if self.is_positive(text):
            self.update_state("current_state", "program_details")
            st.session_state.entity_memory['user_has_biology'] = True
            self.add_bot_message("Great! Let me tell you about our B.Sc Nursing program. It's a full-time 4-year degree.")
            self.add_bot_message("Would you like more details about the program? (Yes/No)")
        elif self.is_negative(text):
            st.session_state.entity_memory['user_has_biology'] = False
            self.add_bot_message("B.Sc Nursing mein admission ke liye Biology avashyak hai. (Biology is mandatory for taking admission)")
            self.offer_additional_help()
        else:
            self.add_bot_message("Please answer with Yes or No - did you study Biology in 12th grade?")

    def handle_program_details(self,text):
        if self.is_positive(text):
            self.update_state("current_state", "fee_structure")
            st.session_state.entity_memory['user_has_biology'] = True
            self.add_bot_message("Our program includes: Patient care, Medical sciences, Clinical practice, and Hospital management.")
            self.add_bot_message("Would you like information about the fee structure? (Yes/No)")
        elif self.is_negative(text):
            st.session_state.entity_memory['user_has_biology'] = False
            self.offer_additional_help()

    def handle_fee_structure(self, text):
        if self.is_positive(text):
            self.update_state("current_state", "hostel_facilities")
            st.session_state.entity_memory['user_has_biology'] = True
            self.add_bot_message("Annual Fee: Tuition ₹60,000 + Bus ₹10,000 = ₹70,000.")
            self.add_bot_message("Installments: ₹30,000, ₹20,000, ₹20,000.")
            self.add_bot_message("Would you like to know about our hostel facilities? (Yes/No)")
        elif self.is_negative(text):
            st.session_state.entity_memory['user_has_biology'] = False
            self.offer_additional_help()
        

    def handle_hostel_facilities(self, text):
        if self.is_positive(text):
            self.update_state("current_state", "college_location")
            st.session_state.entity_memory['user_has_biology'] = True
            self.add_bot_message("Hostel includes: 24/7 electricity, CCTV security, and wardens.")
            self.add_bot_message("Would you like the college location? (Yes/No)")
        elif self.is_negative(text):
            st.session_state.entity_memory['user_has_biology'] = False
            self.offer_additional_help()

    def handle_college_location(self, text):
        if self.is_positive(text):
            self.update_state("current_state", "recognition")
            st.session_state.entity_memory['user_has_biology'] = True
            self.add_bot_message("The college is in Delhi. Great connectivity and educational hub.")
            self.add_bot_message("Would you like to know about our recognition? (Yes/No)")
        elif self.is_negative(text):
            st.session_state.entity_memory['user_has_biology'] = False
            self.offer_additional_help()

    def handle_recognition(self, text):
        if self.is_positive(text):
            self.update_state("current_state", "clinical_training")
            st.session_state.entity_memory['user_has_biology'] = True
        
            self.add_bot_message("Recognized by Indian Nursing Council (INC).")
            self.add_bot_message("Would you like to know about clinical training locations? (Yes/No)")
        elif self.is_negative(text):
            st.session_state.entity_memory['user_has_biology'] = False
            self.offer_additional_help() 

    def handle_clinical_training(self, text):
        if self.is_positive(text):
            self.update_state("current_state", "scholarships")
            st.session_state.entity_memory['user_has_biology'] = True
        
            self.add_bot_message("Training at District Hospitals, CHCs, Ranchi Neurosurgery Hospital.")
            self.add_bot_message("Would you like to know about scholarships? (Yes/No)")
        elif self.is_negative(text):
            st.session_state.entity_memory['user_has_biology'] = False
            self.offer_additional_help() 

    def handle_scholarships(self, text):
        if self.is_positive(text):
            self.update_state("current_state", "admission_details")
            st.session_state.entity_memory['user_has_biology'] = True
        
            self.add_bot_message("Scholarships: ₹18,000–₹48,000 depending on eligibility.")
            self.add_bot_message("Would you like to know admission eligibility? (Yes/No)")
        elif self.is_negative(text):
            st.session_state.entity_memory['user_has_biology'] = False
            self.offer_additional_help() 

    def handle_admission_details(self, text):
        if self.is_positive(text):
            self.update_state("current_state", "final")
            st.session_state.entity_memory['user_has_biology'] = True
        
            self.add_bot_message("Eligibility: Biology in 12th, PNT Exam, Age 17–35. Seats: 60.")
            self.add_bot_message("Would you like anything else? (Yes/No)")
        elif self.is_negative(text):
            st.session_state.entity_memory['user_has_biology'] = False
            self.offer_additional_help() 

    def handle_final_response(self, text):
        if self.is_positive(text):
            self.offer_additional_help()
        else:
            self.end_conversation()

    def handle_additional_help(self, text):
        self.update_state("current_state", "additional_help")
        norm = self.normalize_input(text)

        keyword_map = {
            "program": ("program_details", self.handle_program_details),
            "fees": ("fee_structure", self.handle_fee_structure),
            "fee": ("fee_structure", self.handle_fee_structure),
            "hostel": ("hostel_facilities", self.handle_hostel_facilities),
            "location": ("college_location", self.handle_college_location),
            "recognition": ("recognition", self.handle_recognition),
            "recogn": ("recognition", self.handle_recognition),
            "training": ("clinical_training", self.handle_clinical_training),
            "clinic": ("clinical_training", self.handle_clinical_training),
            "scholarship": ("scholarships", self.handle_scholarships),
            "scholar": ("scholarships", self.handle_scholarships),
            "admission": ("admission_details", self.handle_admission_details),
            
        }

        for keyword, (state, handler) in keyword_map.items():
            if keyword in norm:
                self.update_state("current_state", state)
                handler("yes")
                return

        if self.is_negative(norm):
            self.end_conversation()
        else:
            self.add_bot_message("What info would you like? Options: Program, Fees, Hostel, Location, Recognition, Training, Scholarships, Admission")


    def offer_additional_help(self):
        self.update_state("current_state", "additional_help")
        self.handle_additional_help("")

    def end_conversation(self):
        self.add_bot_message("Thank you for your interest in Delhi Nursing College. Have a great day!")
        self.update_state("conversation_active", False)


# === Streamlit App ===
st.title("🎓 Delhi Nursing College Admission Assistant")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.current_state = "initial_greeting"
    st.session_state.conversation_active = True
    st.session_state.context_stack = []
    st.session_state.entity_memory = {}

assistant = NursingAdmissionAssistant()

# Show chat history
for role, msg in st.session_state.chat_history:
    st.chat_message(role).markdown(msg)

# Start chat
if st.session_state.current_state == "initial_greeting" and not st.session_state.chat_history:
    assistant.add_bot_message("Hello! Welcome to Delhi Nursing College. Are you interested in admission to our B.Sc Nursing program? (Yes/Haan or No/Nahi)")
    st.rerun()

# User input
if st.session_state.conversation_active:
    user_input = st.chat_input("Type your message here...")
    if user_input:
        st.session_state.chat_history.append(("User", user_input))
        assistant.handle_response(user_input)
        st.rerun()
