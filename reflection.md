# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

Looks overall reasonalble functionalities, reach maximum guess attempt since the hints are backwards

- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

the hints were backwards vs. should give the forwards directional hints
the score does not change monotonically vs. make sense to decrease as attempt time increase
the new game button does not work vs. new game could be initiated by clicking new game instead of refreshing page every time
easy mode suppose to handle 1 to 20 but could input 1 to 100 vs should accept only guess between 1 to 20

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

In this case, I mainly explored Github Copilot as the AI tool.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

One correct suggestion was moving functions to logic_utils.py and updating imports in app.py; I verified by running pytest and interact with streamlit app multiple times to make sure it functions well.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

One incorrect suggestion was a unit test for the "new game" button using Streamlit session state in pytest, which failed with AttributeError due to session state not working outside Streamlit; I verified by running the test and removed it.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

running pytest, mannually testing the app for correct behaviors

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.

One test I ran was pytest -q, which showed initial failures in score and range tests, then all passed after fixes, confirming the code worked.

- Did AI help you design or understand any tests? How?

Yes, AI designed tests like the hint regression test and explained failures, helping me verify and iterate on fixes.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.

The secret number kept changing because Streamlit reruns the script on every interaction, regenerating the secret without storing it persistentl

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Streamlit "reruns" mean the app re-executes from top to bottom on each user action, like a page refresh; session state is a dictionary that persists data across reruns, allowing the app to remember values like scores or secrets.

- What change did you make that finally gave the game a stable secret number?

if "secret" not in st.session_state: st.session_state.secret = random.randint(low, high) to initialize the secret only once, making it stable.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.

One habit I want to reuse is applying "ask and planning" mode when identifying bugs to gather context, then switching to "agent" mode for actionable fixes, ensuring an iterative process with clear mental steps.

- What is one thing you would do differently next time you work with AI on a coding task?

 I'd verify AI suggestions with more edge-case testing before full implementation to avoid overlooking assumptions.

- In one or two sentences, describe how this project changed the way you think about AI generated code.

AI generated code could be understood and managed more properly by mastering the tools!
