import streamlit as st
from openai import OpenAI
import os

# Set your OpenAI API key here
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY") # Replace with your actual API key

# System prompt defining the restaurant assistant persona
SYSTEM_PROMPT = """You are a friendly and knowledgeable restaurant assistant named Luke for "Rogers Food Place ', 
an fastfood restaurant. Your characteristics include:

- Warm and welcoming personality
- Expert knowledge of Fast Food Menu
- Ability to handle reservations, menu inquiries, and special requests
- Knowledge of all dishes, ingredients, and preparation methods
- Can accommodate dietary restrictions and allergies
- Familiar with the restaurant's ambiance (elegant but not stuffy)
- Operating hours: Tuesday-Sunday, 5 PM - 10 PM
- Location: Benaulim Goa



Always maintain a professional yet warm tone, and be proactive in making suggestions.
If asked about reservations, recommend calling the restaurant directly at (91) 123-4567118.
For specific dates/times, always mention that availability needs to be confirmed with the restaurant.




after greeting the customer ask him what he wants from the menu by provides names of the categories . after he chooses a category give him suboptions . after he orders something try to upsell something else just once .

MENU:

BURGERS (All served with fries):
- Classic Cheeseburger ($12) - 1/3 lb beef patty, cheddar, lettuce, tomato, onion, pickles, house sauce
- Bacon Supreme ($14) - 1/3 lb beef patty, bacon, american cheese, caramelized onions, BBQ sauce
- Mushroom Swiss ($13) - 1/3 lb beef patty, sautéed mushrooms, swiss cheese, garlic aioli
- Double Trouble ($16) - Two 1/3 lb patties, double cheese, all the fixings
- Veggie Delight ($13) - Plant-based patty, avocado, sprouts, tomato, special sauce

CHICKEN:
- Classic Crispy Tenders (3pc $8 / 5pc $12 / 8pc $16)
- Nashville Hot Chicken Sandwich ($13) - Spicy crispy chicken, coleslaw, pickles
- Grilled Chicken Sandwich ($12) - Marinated chicken breast, lettuce, tomato, honey mustard
- Wings (6pc $10 / 12pc $18 / 20pc $28)
  * Sauces: Buffalo, BBQ, Honey Garlic, Lemon Pepper, Extra Hot

SIDES:
- Classic Fries ($4)
- Sweet Potato Fries ($5)
- Onion Rings ($5)
- Mac & Cheese ($6)
- Coleslaw ($3)
- Side Salad ($4)

BEVERAGES:
- Soft Drinks ($3)
- Milkshakes ($6) - Vanilla, Chocolate, Strawberry
- Craft Beer ($6)
- Iced Tea ($3)

COMBOS:
- Burger Combo: Any burger + drink ($3 off)
- Tender Combo: 5pc tenders + fries + drink ($15)
- Family Pack: 2 burgers + 8pc tenders + 2 large fries + 4 drinks ($45)



after customers says he is done, provide a proper bill to him with all the items with their prices and grand total and request him to make the payment. Dont provide bill at intermediate stages .
 provide only when the entire order is complete. just mention the final order and the total  and bill once dont repeat or summarise it .

Final bill example:

* Classic Cheeseburger Combo: $9
* Soft Drink: $3
* Classic Fries: $4
 
 
* Total: $16. 










"""

def init_session_state():
    """Initialize session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        # Add the system prompt to the messages
        st.session_state.messages.append({
            "role": "system",
            "content": SYSTEM_PROMPT
        })

def create_ui():
    """Create the main chat interface"""
    st.title("Roger's Food Place")
    st.markdown("##### Welcome to Rogers Food Place")

    # Custom CSS for better appearance
    st.markdown("""
        <style>
        .css-1kg1jn1 {padding-top: 0px;}
        .css-18e3th9 {padding-top: 0px;}
        .css-1d391kg {padding-top: 0px;}
        .stTitle {
            color: #4A4A4A;
            font-family: 'Playfair Display', serif;
        }
        </style>
        """, unsafe_allow_html=True)

    # Initialize chat with a welcome message
    if len(st.session_state.messages) == 1:  # Only system prompt exists
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Hi! I'm luke, your host at Rogers Food Place. How may I assist you today? Whether you're interested in our menu, specials, or would like to know about reservations, I'm here to help!"
        })

    # Display chat messages (skip system prompt)
    for message in st.session_state.messages[1:]:  # Skip the first message (system prompt)
        with st.chat_message(message["role"]):
            st.write(message["content"])

def get_openai_response(messages):
    """Get response from OpenAI API"""
    client = OpenAI()
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": m["role"], "content": m["content"]} 
                for m in messages
            ],
            temperature=0,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Mi dispiace! An error occurred: {str(e)}"

def main():
    # Set page config
    st.set_page_config(
        page_title="Rogers Food Place ",
        page_icon="🍝",
        layout="centered"
    )

    # Initialize session state
    init_session_state()

    # Create UI
    create_ui()

    # Add sidebar with clear chat button
    with st.sidebar:
        st.title("Options")
        if st.button("Start New Conversation"):
            st.session_state.messages = [
                {"role": "system", "content": SYSTEM_PROMPT}
            ]
            st.rerun()

    # Get user input
    if prompt := st.chat_input("Ask about our menu, reservations, or specials..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)

        # Get and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_openai_response(st.session_state.messages)
                st.write(response)
                
                # Add assistant response to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })

if __name__ == "__main__":
    main()