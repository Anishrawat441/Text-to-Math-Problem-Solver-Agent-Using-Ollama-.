# Task 3: Session State for Application
## 1.Build a simple Streamlit app.
## 2.Use st.session_state to:
## . Maintain conversation history
## . Store previous questions & answers
## 3. Ensure math context is preserved across interactions. 


import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.tools import tool


## Creating UI

st.title("Math Problem Solver")


# Initialize LLM

model = ChatOllama(
    model="gemma3:latest",
    temperature=0
)

# Calculator Tool

@tool
def calculator(expression: str) -> str:
    """Calculate a mathematical expression."""

    try:
        expression = expression.replace("^", "**")

        result = eval(
            expression,
            {"__builtins__": {}},
            {}
        )

        return str(result)

    except Exception as e:
        return f"Error: {e}"

# Session State

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! I am your Math Assistant. "
                "Ask me a question."
            )
        }
    ]
# Display Conversation History

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])

# User Input

question = st.chat_input(
    "Ask your question..."
)


if question:
    # Store User Question

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    # Display User Question

    with st.chat_message("user"):
        st.write(question)


    # Create Context from Previous Messages

    conversation_history = ""

    for message in st.session_state.messages:

        conversation_history += (
            f"{message['role']}: "
            f"{message['content']}\n"
        )


   
    # Generate Response

    with st.spinner("Solving..."):

        prompt = f"""
You are a helpful mathematical assistant.

Use the previous conversation to understand the
mathematical context.

Previous conversation:
{conversation_history}

Current question:
{question}

Solve the problem clearly and show the important steps.
Give the final answer at the end.
"""

        response = model.invoke(prompt)

        answer = response.content


## Store answer

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })


    # Display Assistant Answer

    with st.chat_message("assistant"):
        st.write(answer)