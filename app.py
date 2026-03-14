import random
import streamlit as st

from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
)

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# Check if difficulty has changed and reset game if it has
if "current_difficulty" not in st.session_state:
    st.session_state.current_difficulty = difficulty
elif st.session_state.current_difficulty != difficulty:
    # Difficulty changed, reset the game
    st.session_state.current_difficulty = difficulty
    st.session_state.attempts = 1
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.secret = random.randint(low, high)

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("Make a guess")

#st.info(
    #f"Guess a number between {low} and {high}. "
    #f"Attempts left: {attempt_limit - len(st.session_state.history)}"
#)

#with st.expander("Developer Debug Info"):
    #st.write("Secret:", st.session_state.secret)
    #st.write("Attempts:", st.session_state.attempts)
    #st.write("Score:", st.session_state.score)
    #st.write("Difficulty:", difficulty)
    #st.write("History:", st.session_state.history)

guess_key = f"guess_input_{difficulty}"

# Ensure the text input has a known session state key before creating the widget.
if guess_key not in st.session_state:
    st.session_state[guess_key] = ""

# When a new game is started, we set a flag so that on the next rerun the input is cleared
# before the widget is instantiated (avoids Streamlit API errors).
if st.session_state.get("reset_guess_input", False):
    st.session_state[guess_key] = ""
    st.session_state["reset_guess_input"] = False

raw_guess = st.text_input(
    "Enter your guess:",
    key=guess_key,
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

#FIX: identify the new game generation logic with Copilot Agent Ask mode, improve the code with in line chat to reset the game state and generate a new secret when the player clicks "New Game"
if new_game:
    # Reset all game state so the player can start fresh without needing a browser refresh.
    st.session_state.attempts = 1
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []

    # Keep the new secret aligned with the currently selected difficulty range.
    st.session_state.secret = random.randint(low, high)

    # Set a flag so the input is cleared before the widget is created on the next run.
    st.session_state["reset_guess_input"] = True

    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

# FIX: update the reamining attempts logic to be more intuitive for the player
if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        if st.session_state.attempts % 2 == 0:
            secret = str(st.session_state.secret)
        else:
            secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
            max_attempts=attempt_limit,
        )

        with st.expander("Updated Debug Info"):
            st.write("Secret:", st.session_state.secret)
            st.write("Next Attempt:", st.session_state.attempts)
            #st.write("Score:", st.session_state.score)
            st.write("Outcome:", outcome)
            st.write("History:", st.session_state.history)

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts > attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )
    st.divider()
st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - len(st.session_state.history)}"
)

st.caption("Built by an AI that claims this code is production-ready.")
