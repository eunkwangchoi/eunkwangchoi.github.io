+++  
draft = false  
toc = true  
math = false  
isCJKLanguage = false  
author = "Eunkwang Choi"  
title = "[August 2026] Session 2 | Build Your First Game with Python"  
date = 2026-08-06  
expiryDate = 2099-12-31  
languages = "English"  
layout = "single-multilinguial"  
+++

Generative AI Education with Mongolian School | Build Your Own Game with AI | August 2026

<!--more-->

# 0. Course Overview

## 0.1. Today's Objectives

#   

In this session, we will go one step beyond asking AI to build an entire program for us. We will learn how to **read and modify Python code written by AI**.

Students will learn to:

1. Understand what Python is.
    
2. Use AI to generate code for a simple Python game.
    
3. Run a Python program in Replit.
    
4. Understand the roles of variables, input, conditional statements, and loops within a game.
    
5. Directly modify numbers and text in the code.
    
6. Ask AI to add new game features.
    
7. Compare the code before and after modification and identify what changed.
    

## 0.2. Today's Outcomes

#   

- A Python number guessing game
    
- A modified version with at least one changed difficulty setting or game rule
    
- A game with at least one new feature added using AI
    

## 0.3. Class Duration

#   

- Total class duration: 120 minutes
    
- Review of the previous session and introduction to Python: approximately 15 minutes
    
- Instructor game-building demonstration: approximately 25 minutes
    
- Reading Python code: approximately 25 minutes
    
- Guided building and direct modification: approximately 35 minutes
    
- Optional game extension activity: approximately 15 minutes
    
- Sharing results and wrap-up: approximately 5 minutes
    

# 1. Review of the Previous Session

## 1.1. What We Did Last Time

#   

In the previous session, we described the app we wanted in natural language and observed AI building the application.

The basic process was:

1. Describe what you want to build to AI.
    
2. AI generates code.
    
3. Run the program.
    
4. Ask AI to modify the parts you want to change.
    
5. Run it again and check the result.
    

We will use the same process today.

However, we will add one new step.

> **Read the Python code created by AI.**

## 1.2. Today's Key Question

#   

> Where are the score, correct answer, and player input stored in the code?

Today, we will not only look at the game screen. We will examine the **code structure** that makes the game work.

# 2. What Is Python?

## 2.1. Python

#   

Python is a programming language used in many fields, including software development, data analysis, artificial intelligence, and automation.

Characteristics of Python:

- Relatively easy-to-read syntax
    
- Programs can be created with relatively short code
    
- Widely used in AI development
    
- Suitable for games and simple applications
    

## 2.2. How We Will Learn Python Today

#   

We will not begin by memorizing Python syntax.

Instead, we will learn in this order:

> Run the game → Look at the code → Find the function → Modify the code → Run it again

In other words, we will discover the Python concepts we need inside an actual game.

# 3. Tools Used in This Session

## 3.1. Google AI Studio

#   

[https://aistudio.google.com](https://aistudio.google.com/)

In Google AI Studio, we will:

- Generate Python code
    
- Ask for code explanations
    
- Modify code
    
- Analyze errors
    
- Ask AI to explain what changed
    

Google AI Studio's Code Execution feature can generate and execute Python code.

However, **Replit will be used as the main environment in which the player enters input and actually plays the game.**

## 3.2. Replit

#   

[https://replit.com](https://replit.com/)

In Replit, we will:

- View Python files
    
- Paste code
    
- Directly modify code
    
- Run programs
    
- Play games through the Console
    
- Check error messages
    

A Python program can be started using the `Run` button in Replit, and the result can be checked in the Console.

# 4. Instructor Demonstration I — Ask AI to Build a Game

## 4.1. Today's Game

#   

**Number Guessing Game**

The computer randomly selects one number between 1 and 100.

The player must guess the number.

Game rules:

- If the guess is lower than the answer, display `Too low!`
    
- If the guess is higher than the answer, display `Too high!`
    
- If the guess is correct, display `Correct!`
    
- Continue until the player finds the correct answer
    

## 4.2. First Prompt

#   

Use the following prompt in Google AI Studio.

```
Create a very simple number guessing game in Python for beginner students.

Rules:
- Choose a random number from 1 to 100.
- Ask the player to enter a number.
- If the guess is too low, print "Too low!"
- If the guess is too high, print "Too high!"
- If the answer is correct, print "Correct!"
- Keep asking until the player gets the correct answer.

Requirements:
- Keep the Python code simple.
- Add short comments.
- Do not use classes.
- Explain the important parts after the code.
```

## 4.3. First, Read the Code Created by AI

#   

The basic structure will usually look similar to this:

```
import random

answer = random.randint(1, 100)

while True:
    guess = int(input("Guess a number from 1 to 100: "))

    if guess < answer:
        print("Too low!")
    elif guess > answer:
        print("Too high!")
    else:
        print("Correct!")
        break
```

Do not try to memorize the code immediately.

First, find which line performs each function.

# 5. Discovering Python Inside the Game

## 5.1. `import`

#   

```
import random
```

This makes Python's `random` functionality available.

In this game, it is used so that the computer can select a number randomly.

## 5.2. Variables

#   

```
answer = random.randint(1, 100)
```

The number selected by the computer is stored under the name `answer`.

A variable is like a box that stores a value.

Other examples:

```
score = 100
lives = 3
player_name = "Alex"
```

### Find It

#   

Which part is the variable in the following code?

```
score = 50
```

- `score`
    
- `50`
    

What is the difference between their roles?

## 5.3. `input()`

#   

```
guess = int(input("Guess a number: "))
```

`input()` receives information from the player.

In this game, it is used when the player enters a number.

## 5.4. `if`

#   

```
if guess < answer:
    print("Too low!")
```

`if` checks whether a condition is true.

Games constantly need to make decisions such as:

- Did the enemy hit the player?
    
- Is the score higher than 100?
    
- Is the player's health zero?
    
- Did the player choose the correct answer?
    

## 5.5. `elif` and `else`

#   

```
elif guess > answer:
    print("Too high!")
else:
    print("Correct!")
```

These allow the program to choose among several possible situations.

## 5.6. `while`

#   

```
while True:
```

This makes the game repeat.

It is the reason the program keeps asking for a number instead of ending after a single guess.

## 5.7. `break`

#   

```
break
```

This ends the repetition.

It is used here to stop the game after the player finds the correct answer.

# 6. Run the Game in Replit

## 6.1. Prepare a Python Project

#   

1. Log in to Replit.
    
2. Open a new Python project or a project capable of running Python.
    
3. Find the Python file.
    
4. The main file will generally be named `main.py`.
    
5. Delete the existing sample code if necessary.
    
6. Paste the Python code provided by the instructor.
    

## 6.2. Run the Game

#   

1. Select the `Run` button at the top.
    
2. Check the Console.
    
3. Confirm that a message similar to the following appears.
    

```
Guess a number from 1 to 100:
```

4. Enter a number.
    
5. Check whether `Too low!`, `Too high!`, or `Correct!` appears.
    
6. Continue until you find the correct answer.
    

# 7. Modify the Code Yourself

## 7.1. Mission 1 — Change the Number Range

#   

Current code:

```
answer = random.randint(1, 100)
```

Change it directly to:

```
answer = random.randint(1, 20)
```

or:

```
answer = random.randint(1, 1000)
```

### Think About It

#   

Does a smaller range make the game easier?

Does a larger range make the game harder?

## 7.2. Mission 2 — Change the Messages

#   

Current code:

```
print("Too low!")
```

Change it to any message you want.

For example:

```
print("Go higher!")
```

You can also ask AI to translate the message into Mongolian and insert the translated text.

## 7.3. Mission 3 — Add a Game Title

#   

Add the following code near the beginning:

```
print("====================")
print("NUMBER GUESSING GAME")
print("====================")
```

Then change the title yourself.

## 7.4. Mission 4 — Ask for the Player's Name

#   

Ask AI:

```
Add a player name at the beginning of the game.

Ask the player for their name and use the name when they win.

Keep the code simple.
Show only the changed parts first.
```

Expected code:

```
player_name = input("What is your name? ")
```

At the end:

```
print("Correct!", player_name)
```

# 8. Instructor Demonstration II — Add Game Features

## 8.1. Add a Limited Number of Attempts

#   

The current game allows unlimited guesses.

Ask AI:

```
Modify the game so the player has only 10 attempts.

Show the number of attempts left after every guess.

Keep the code simple for beginners.
Explain what new variables and conditions you added.
```

## 8.2. What to Find in the Modified Code

#   

Find:

- The variable that stores the number of attempts
    
- The code that decreases the number after each guess
    
- The condition that checks whether the attempts reached zero
    
- The code that displays Game Over
    

## 8.3. Compare Before and After

#   

Answer the following questions:

1. What is the name of the new variable?
    
2. On which line does the number decrease?
    
3. Where is the game-ending condition?
    
4. Which parts of the original code remained unchanged?
    

# 9. Student Feature Challenge

## 9.1. Level 1 — Easy Changes

#   

Choose one.

### Change the Number Range

```
Change the number range from 1-100 to 1-50.
```

### Change the Number of Attempts

```
Give the player only 5 attempts.
```

### Change the Game Messages

```
Make the game messages more funny.
Use simple English.
```

### Mongolian Interface

```
Translate all game messages into Mongolian.
Keep the Python code itself unchanged.
```

## 9.2. Level 2 — New Features

#   

### Score System

```
Add a score system.

Start with 100 points.
Subtract 10 points for every wrong guess.
Show the final score when the player wins.
Keep the code beginner-friendly.
```

### Hint System

```
Add a hint after 3 wrong guesses.

Tell the player whether the answer is odd or even.
Keep the code simple.
```

### Replay

```
Add a replay function.

After the game ends, ask:
"Play again? y/n"

If the player enters y, start a new game.
```

## 9.3. Level 3 — Free Extension

#   

Students who finish early may try:

- Easy / Normal / Hard difficulty
    
- High score
    
- Random bonus points
    
- A time-limit concept
    
- `Hot` when close to the answer and `Cold` when far away
    
- A secret cheat code
    
- Two-player competition
    

# 10. Turn It into a Different Game

## 10.1. Games That Use the Same Python Concepts

#   

The basic structures learned in the number guessing game can be used to create many other games.

### Rock Paper Scissors

Concepts needed:

- `input()`
    
- `random`
    
- `if`
    
- variables
    

### Dice Game

Concepts needed:

- `random`
    
- variables
    
- conditional statements
    
- score
    

### Quiz Game

Concepts needed:

- `input()`
    
- variables
    
- conditional statements
    
- score
    

### Simple RPG Battle

Concepts needed:

- HP variable
    
- Attack variable
    
- `random`
    
- conditional statements
    
- loops
    

### Choose Your Own Adventure

Concepts needed:

- User input
    
- Conditional statements
    
- Multiple choices
    

# 11. Optional Mini Projects

## 11.1. Project A — Rock Paper Scissors

#   

Use the following prompt:

```
Create a simple Rock Paper Scissors game in Python for beginners.

Requirements:
- The player enters rock, paper, or scissors.
- The computer chooses randomly.
- Show both choices.
- Tell the player whether they win, lose, or draw.
- Keep the code simple.
- Add comments.
```

## 11.2. Project B — Dice Battle

#   

```
Create a simple dice battle game in Python.

Rules:
- The player and computer each roll one dice.
- Use random numbers from 1 to 6.
- The higher number wins.
- Show both dice results.
- Keep the code simple for beginners.
```

## 11.3. Project C — Quiz Game

#   

```
Create a simple 5-question quiz game in Python.

Requirements:
- Ask one question at a time.
- Use input().
- Give 1 point for every correct answer.
- Show the final score.
- Keep the code simple for beginners.
```

## 11.4. Project D — Simple RPG Battle

#   

```
Create a very simple text-based RPG battle game in Python.

Rules:
- Player HP starts at 100.
- Monster HP starts at 80.
- The player can choose Attack or Heal.
- Attack damage should be random.
- Healing amount should be random.
- The monster attacks after the player's turn.
- The game ends when either HP becomes 0.

Requirements:
- Keep the code simple for beginner students.
- Do not use classes.
- Add comments.
```

# 12. Ask AI to Explain the Code

## 12.1. When English Is Difficult

#   

Use:

```
Explain this Python code using very simple English.

Explain only:
- variables
- input
- if
- while
- random
```

## 12.2. When a Mongolian Explanation Is Needed

#   

```
Explain this Python code in Mongolian for a beginner student.

Do not change the code.
Explain each important part with a short example.
```

## 12.3. When AI Generates Code That Is Too Difficult

#   

Ask:

```
This code is too difficult.

Rewrite it for a beginner Python student.

Requirements:
- Do not use classes.
- Do not use advanced functions.
- Use simple variables, if statements, and loops.
- Keep it under 60 lines if possible.
```

# 13. When an Error Occurs

## 13.1. Read the Error Message

#   

If a Python program has a problem, an error message will appear in the Console.

Do not immediately delete the error message.

Check which line caused the problem.

## 13.2. Show the Error to AI

#   

Use:

```
I am a beginner learning Python.

Here is my code:

[Paste the code here]

Here is the error:

[Paste the error message here]

Explain the problem in simple English and show me only the part I need to fix.
```

## 13.3. Error-Correction Principle

#   

Even if AI provides an entirely new version of the code, do not immediately replace everything.

Whenever possible:

1. Find the line containing the error.
    
2. Ask AI what caused the problem.
    
3. Identify only the part that needs to be changed.
    
4. Modify it yourself.
    
5. Run the program again.
    

# 14. Python Concepts You Must Understand Today

#   

|Python|What It Does in a Game|
|---|---|
|Variable|Stores values such as score, health, and answers|
|`input()`|Receives player input|
|`print()`|Displays game messages|
|`if`|Checks a condition|
|`elif`|Adds another condition|
|`else`|Handles the remaining case|
|`while`|Repeats the game|
|`break`|Ends a loop|
|`random`|Makes the computer behave randomly|

# 15. Code-Reading Quiz

## 15.1.

#   

```
lives = 3
```

What does `3` represent?

## 15.2.

#   

```
if player_hp <= 0:
    print("Game Over")
```

When will `Game Over` appear?

## 15.3.

#   

```
score = score + 10
```

What happens to the score when this line runs?

## 15.4.

#   

```
enemy = random.randint(1, 3)
```

Which values can be stored in `enemy`?

## 15.5.

#   

```
while True:
```

Why is this useful in a game?

# 16. Class Wrap-Up

## 16.1. Completion Checklist

#   

Before finishing the session, check:

- I generated Python game code.
    
- I ran a Python program in Replit.
    
- I found at least one variable.
    
- I identified where `input()` is used.
    
- I found an `if` conditional statement.
    
- I found a loop.
    
- I directly modified a number or sentence in the code.
    
- I ran the game again after modifying it.
    
- I asked AI to add at least one new feature.
    
- I checked which part of the code changed.
    

## 16.2. Today's Key Idea

#   

Vibe Coding does not mean giving all coding work to AI.

Good Vibe Coding repeatedly follows this process:

> Build → Run → Read the code → Modify → Run again

Students do not need to memorize every Python syntax rule.

However, in the game they are creating, they should be able to identify:

- Where is a value stored?
    
- Where does the program receive player input?
    
- Where does the game make decisions?
    
- Which part repeats?
    
- What changes when a number in the code changes?
    

# 17. Preview of the Next Session

#   

In the next session, we will move beyond text-based games and build a **Python game with moving graphics**.

Planned topics:

- Game window
    
- Player character
    
- `x`, `y` coordinates
    
- Keyboard input
    
- Character movement
    
- Obstacles
    
- Collision
    
- Score
    
- Lives
    
- Game Over
    

Basic project for the next session:

> **Dodge the Falling Obstacles**

Think about one of the following:

1. What would you like your player character to be?
    
2. What would you like to avoid or collect?
    
3. How should the player earn points?