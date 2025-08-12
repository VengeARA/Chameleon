import streamlit as st
import random
import pandas as pd

# Categories dictionary
categories = {
    "Snacks at the Movies": [
        "Popcorn", "Nachos", "Hot Dog", "Pretzel", "Candy", "Chocolate Bar", "Gummy Bears", "Ice Cream",
        "Soda", "Milkshake", "Slushie", "Caramel Corn", "Churros", "French Fries", "Onion Rings", "Peanuts",
        "Trail Mix", "Cupcake", "Brownie", "Pizza Slice", "Soft Drink", "Water Bottle", "Cheese Sticks", "Corn Dog", "Fruit Cup"
    ],
    "Cold Drinks for Summer": [
        "Lemonade", "Iced Tea", "Smoothie", "Milkshake", "Cold Coffee", "Coconut Water", "Iced Latte", "Frappe",
        "Slushie", "Iced Matcha", "Fruit Punch", "Mint Mojito", "Ice Water", "Soda", "Root Beer", "Iced Chocolate",
        "Bubble Tea", "Iced Americano", "Orange Juice", "Apple Juice", "Ginger Ale", "Cola", "Sports Drink", "Sparkling Water", "Shirley Temple"
    ],
    "Winter Destinations": [
        "Australia", "Chicago", "Paris", "New York", "London", "Dubai", "Toronto", "Rome", "Barcelona", "Tokyo",
        "Moscow", "Istanbul", "Beijing", "Los Angeles", "Miami", "Berlin", "Singapore", "Amsterdam", "Seoul", "Cairo",
        "Bangkok", "Delhi", "Hong Kong", "Madrid", "Sydney"
    ],
    "Things You See in an Airport": [
        "Check-in Counter", "Security Check", "Boarding Gate", "Duty-Free Shop", "Information Desk",
        "Flight Monitor", "Luggage Carousel", "Customs", "Passport Control", "Waiting Lounge",
        "Airplane", "Runway", "Jet Bridge", "Pilot", "Flight Attendant",
        "Baggage Cart", "Trolley", "Snack Kiosk", "Airport Taxi", "VIP Lounge",
        "Lost and Found", "Ticket Counter", "Announcement Speaker", "Escalator", "Elevator"
    ],
    "Board Games in a Cafe": [
        "Chess", "Exploding Kittens", "Monopoly", "Scrabble", "Clue",
        "Catan", "Ticket to Ride", "Risk", "Scotland Yard", "Carcassonne",
        "UNO Show 'em No Mercy", "Connect Four", "Battleship", "Pictureqa", "Marvel Guess in 10",
        "Exploding Kittens", "Forest Run", "Cards", "Jenga", "Pictionary",
        "Phase 10", "Blokus", "The Game of Life", "Codenames", "Sequence"
    ]
}

# Initialize session state variables
if "step" not in st.session_state:
    st.session_state.step = "welcome"

if "num_players" not in st.session_state:
    st.session_state.num_players = 0

if "category_name" not in st.session_state:
    st.session_state.category_name = None

if "chosen_16" not in st.session_state:
    st.session_state.chosen_16 = []

if "secret_word" not in st.session_state:
    st.session_state.secret_word = None

if "chameleon_player" not in st.session_state:
    st.session_state.chameleon_player = None

if "current_player" not in st.session_state:
    st.session_state.current_player = 1

if "show_word" not in st.session_state:
    st.session_state.show_word = False  # controls if player can see their word

def reset_game():
    st.session_state.step = "welcome"
    st.session_state.num_players = 0
    st.session_state.category_name = None
    st.session_state.chosen_16 = []
    st.session_state.secret_word = None
    st.session_state.chameleon_player = None
    st.session_state.current_player = 1
    st.session_state.show_word = False

# Title
st.markdown('# Welcome to the <span style="color:green">Chameleon</span> Game!', unsafe_allow_html=True)

# Game flow logic
if st.session_state.step == "welcome":
    st.write("Press Start to begin the game.")
    if st.button("Start Game"):
        st.session_state.step = "select_players"

elif st.session_state.step == "select_players":
    num = st.number_input("Enter number of players (3-10):", min_value=3, max_value=10, step=1)
    if st.button("Confirm Players"):
        st.session_state.num_players = num
        # Pick category and words
        st.session_state.category_name, words = random.choice(list(categories.items()))
        st.session_state.chosen_16 = random.sample(words, 16)
        st.session_state.secret_word = random.choice(st.session_state.chosen_16)
        st.session_state.chameleon_player = random.randint(1, st.session_state.num_players)
        st.session_state.step = "show_words"

elif st.session_state.step == "show_words":
    st.subheader(f"Category: {st.session_state.category_name}")
    st.write("Here are your 16 words (4x4 table). Take a good look — no one knows who the imposter is yet!")
    # Display 4x4 table
    df = pd.DataFrame([st.session_state.chosen_16[i:i+4] for i in range(0, 16, 4)])
    st.table(df)
    if st.button("Proceed to Player Turns"):
        st.session_state.step = "player_turn"

elif st.session_state.step == "player_turn":
    player = st.session_state.current_player

    if not st.session_state.show_word:
        # Step 1: Ready screen
        st.subheader(f"Player {player}'s turn")
        st.write(f"Pass the device to Player {player}.")
        st.write("When you're ready to see your word, press **Show Word**.")
        if st.button("Show Word"):
            st.session_state.show_word = True
        st.stop()

    # Step 2: Show word or imposter
    st.subheader(f"Player {player}'s turn")
    if player == st.session_state.chameleon_player:
        st.markdown("## You are the **<span style='color:red'>IMPOSTER</span>!** Try to blend in...", unsafe_allow_html=True)
    else:
        st.markdown(f"## Your secret word is: **{st.session_state.secret_word}**")

    if player < st.session_state.num_players:
        if st.button("Next Player"):
            st.session_state.current_player += 1
            st.session_state.show_word = False
            st.experimental_rerun()
    else:
        if st.button("See Final Screen"):
            st.session_state.step = "final_screen"
            st.experimental_rerun()

elif st.session_state.step == "final_screen":
    st.subheader(f"Category: {st.session_state.category_name}")
    df = pd.DataFrame([st.session_state.chosen_16[i:i+4] for i in range(0, 16, 4)])
    st.table(df)
    st.write("""
    **All players have received their word.**  
    Find and vote out the imposter.  
    If the imposter guesses the correct word, they win.  
    If they fail, the players win.  
    Remember, your goal is not to give hints about the word, but to prove you're safe.
    """)
    if st.button("Play Again"):
        reset_game()
        st.experimental_rerun()
