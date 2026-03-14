import importlib
import random
import sys
import os

# ensure the project root is on sys.path so tests can import top-level modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st

from logic_utils import check_guess, update_score, parse_guess, get_range_for_difficulty


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _message = check_guess(40, 50)
    assert outcome == "Too Low"

def test_string_secret_hint_direction():
    # The secret may sometimes be stored as a string.  This test exercises a
    # pathological case where lexicographic comparison would give the wrong
    # hint ("2" > "100" is True).  We expect numeric behavior.
    outcome, _message = check_guess(2, "100")
    assert outcome == "Too Low"
