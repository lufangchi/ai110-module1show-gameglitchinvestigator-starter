#FIX: Refactored functions logic into logic_utils.py using Copilot Agent mode

#FIX: Discuss the range and attempt logic with the Copilot Agent and update the code to be more reasonable for the player  
def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty.

    This mirrors the behavior originally defined in :mod:`app`.
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 100
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None

#FIX: Identify the guess checking logic with Copilot Agent Ask mode, improve the code with in line chat
def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    Returns:
        tuple[str, str]: (outcome, hint_message)

    The hint message is designed to tell the player which direction to move their next guess.
    If the guess is higher than the secret, the hint says to go LOWER, and vice versa.
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    # Determine direction hints correctly.
    try:
        if guess > secret:
            return "Too High", "📉 Go LOWER!"
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        # Support glitchy behavior where secret may be a string.  Numeric
        # comparison of mixed types raises TypeError, and a naive lexicographic
        # comparison can give the wrong hint (e.g. "2" > "100").  Convert to
        # ints when possible, otherwise fall back to string comparison.
        try:
            g_num = int(guess)
            s_num = int(secret)
        except Exception:
            g_num = None
            s_num = None

        if g_num is not None and s_num is not None:
            if g_num == s_num:
                return "Win", "🎉 Correct!"
            if g_num > s_num:
                return "Too High", "📉 Go LOWER!"
            return "Too Low", "📈 Go HIGHER!"
        # last resort: compare as strings
        g = str(guess)
        s = str(secret)
        if g == s:
            return "Win", "🎉 Correct!"
        if g > s:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"

#FIX: Redifine the scoring logic with Copilot Agent Ask mode, setting the max score to 100, deducting over attemps.
def update_score(current_score: int, outcome: str, attempt_number: int, max_attempts: int):
    """
    Update score based on game outcome and attempt number.
    
    Scoring rules:
    - Initial score: 100
    - End score: 0
    - Correct on attempt 1: 100 points
    - Correct on attempt n (n > 1): 100 - (n-1) * 100/(max_attempts-1) points
    - Wrong guess: no change to score
    """
    if outcome == "Win":
        # Convert attempt_number to actual attempt (accounts for counter starting at 1)
        actual_attempt = attempt_number - 1
        
        if actual_attempt == 1:
            return 100
        else:
            # Deduct points: 100/max_attempts per attempt starting from attempt 2
            points_per_attempt = 100 / max_attempts
            score = 100 - (actual_attempt - 1) * points_per_attempt
            # Ensure score doesn't go below 0
            return max(int(score), 0)
    
    # For wrong guesses, score doesn't change
    return current_score
