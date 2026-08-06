+++  
draft = false  
toc = true  
math = false  
isCJKLanguage = true  
author = "최은광"  
title = "[26년 8월] 2강 | Python으로 첫 게임 만들기"  
date = 2026-08-06  
expiryDate = 2099-12-31  
languages = "한국어"  
layout = "single-multilinguial"  
+++

몽골학교와 함께하는 생성형 AI 활용 교육 | AI와 함께 만드는 나만의 게임 | 26년 8월

<!--more-->

# 0. 수업 개요

## 0.1. 오늘의 목표

#   

이번 수업에서는 AI에게 프로그램 전체를 맡기는 것에서 한 단계 더 나아가, **AI가 작성한 Python 코드를 직접 읽고 수정하는 방법**을 배운다.

학생은 다음 내용을 학습한다.

1. Python이 무엇인지 이해한다.
    
2. AI를 이용하여 간단한 Python 게임 코드를 생성한다.
    
3. Replit에서 Python 프로그램을 실행한다.
    
4. 변수, 입력, 조건문, 반복문의 역할을 게임 안에서 이해한다.
    
5. 코드의 일부 숫자와 문장을 직접 수정한다.
    
6. AI에게 새로운 게임 기능을 추가하도록 요청한다.
    
7. 수정 전후의 코드를 비교하고 어떤 부분이 달라졌는지 확인한다.
    

## 0.2. 오늘의 결과물

#   

- Python 숫자 맞히기 게임
    
- 난이도 또는 게임 규칙을 한 가지 이상 직접 변경한 게임
    
- AI를 이용하여 새로운 기능을 한 가지 이상 추가한 게임
    

## 0.3. 수업 시간

#   

- 총 수업 시간 : 120분
    
- 지난 수업 복습 및 Python 소개 : 약 15분
    
- 강사 게임 제작 시연 : 약 25분
    
- Python 코드 읽기 : 약 25분
    
- 학생 따라 만들기 및 직접 수정 : 약 35분
    
- 선택형 게임 확장 실습 : 약 15분
    
- 결과 공유 및 정리 : 약 5분
    

# 1. 지난 수업 복습

## 1.1. 지난 시간에 한 일

#   

지난 수업에서는 자연어로 원하는 앱을 설명하고 AI가 앱을 만드는 과정을 살펴보았다.

기본 흐름은 다음과 같았다.

1. 만들고 싶은 것을 AI에게 설명한다.
    
2. AI가 코드를 만든다.
    
3. 프로그램을 실행한다.
    
4. 원하는 부분을 수정해 달라고 요청한다.
    
5. 다시 실행하여 결과를 확인한다.
    

오늘도 이 흐름을 사용한다.

그러나 한 가지 새로운 단계를 추가한다.

> **AI가 만든 Python 코드를 직접 읽어 본다.**

## 1.2. 오늘의 핵심 질문

#   

> 게임 속 점수, 정답, 플레이어의 입력은 코드 어디에 있을까?

오늘은 게임의 화면만 보는 것이 아니라 게임을 움직이는 **코드의 구조**를 찾아본다.

# 2. Python이란 무엇인가?

## 2.1. Python

#   

Python은 프로그램, 데이터 분석, 인공지능, 자동화 등 여러 분야에서 사용되는 프로그래밍 언어이다.

Python의 특징:

- 비교적 읽기 쉬운 문법
    
- 짧은 코드로 프로그램 제작 가능
    
- AI 개발에서 널리 사용
    
- 게임과 간단한 프로그램 제작 가능
    

## 2.2. 오늘 Python을 배우는 방법

#   

오늘은 Python 문법을 먼저 외우지 않는다.

다음 순서로 학습한다.

> 게임 실행 → 코드 보기 → 기능 찾기 → 코드 수정 → 다시 실행

즉, 필요한 Python 개념을 게임 안에서 하나씩 발견한다.

# 3. 수업에서 사용할 도구

## 3.1. Google AI Studio

#   

[https://aistudio.google.com](https://aistudio.google.com/)

Google AI Studio에서는 다음 작업을 한다.

- Python 코드 생성
    
- 코드 설명
    
- 코드 수정
    
- 오류 분석
    
- 변경된 부분 설명
    

Google AI Studio의 Code execution 기능은 Python 코드를 생성하고 실행할 수 있다.

다만 이번 수업에서 **플레이어가 직접 입력하며 게임을 플레이하는 최종 실행 환경은 Replit을 사용한다.**

## 3.2. Replit

#   

[https://replit.com](https://replit.com/)

Replit에서는 다음 작업을 한다.

- Python 파일 확인
    
- 코드 붙여넣기
    
- 코드 직접 수정
    
- 프로그램 실행
    
- Console에서 게임 플레이
    
- 오류 메시지 확인
    

Replit 상단의 `Run` 버튼으로 프로그램을 실행할 수 있으며, 실행 결과는 Console에서 확인할 수 있다.

# 4. 강사 시연 Ⅰ — AI에게 게임을 만들어 달라고 하기

## 4.1. 오늘 만들 게임

#   

**Number Guessing Game**

컴퓨터가 1부터 100까지 숫자 하나를 무작위로 선택한다.

플레이어는 숫자를 맞혀야 한다.

게임 규칙:

- 정답보다 작은 숫자를 입력하면 `Too low!`
    
- 정답보다 큰 숫자를 입력하면 `Too high!`
    
- 정답을 입력하면 `Correct!`
    
- 정답을 맞힐 때까지 반복
    

## 4.2. 첫 번째 프롬프트

#   

Google AI Studio에서 다음 프롬프트를 사용한다.

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

## 4.3. AI가 만든 코드를 먼저 읽어 보기

#   

예상되는 기본 구조는 다음과 같다.

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

코드를 바로 외우지 않는다.

먼저 어떤 줄이 어떤 기능을 하는지 찾아본다.

# 5. 게임 안에서 Python 발견하기

## 5.1. `import`

#   

```
import random
```

`random`이라는 기능을 Python에서 사용할 수 있도록 불러온다.

이번 게임에서는 컴퓨터가 임의의 숫자를 선택하기 위해 사용한다.

## 5.2. 변수

#   

```
answer = random.randint(1, 100)
```

`answer`라는 이름에 컴퓨터가 고른 숫자를 저장한다.

변수는 값을 담아 두는 상자와 비슷하다.

다른 예:

```
score = 100
lives = 3
player_name = "Alex"
```

### 찾아보기

#   

다음 중 변수는 무엇인가?

```
score = 50
```

- `score`
    
- `50`
    

둘의 역할은 어떻게 다른가?

## 5.3. `input()`

#   

```
guess = int(input("Guess a number: "))
```

`input()`은 플레이어에게 값을 입력받는다.

게임에서는 플레이어가 숫자를 입력할 때 사용한다.

## 5.4. `if`

#   

```
if guess < answer:
    print("Too low!")
```

`if`는 어떤 조건이 맞는지 판단한다.

게임에서는 다음과 같은 판단이 계속 필요하다.

- 적에게 맞았는가?
    
- 점수가 100점을 넘었는가?
    
- 플레이어의 체력이 0인가?
    
- 정답을 맞혔는가?
    

## 5.5. `elif`와 `else`

#   

```
elif guess > answer:
    print("Too high!")
else:
    print("Correct!")
```

여러 상황 중 하나를 선택한다.

## 5.6. `while`

#   

```
while True:
```

게임을 계속 반복하게 한다.

숫자를 한 번 입력하고 프로그램이 바로 끝나는 것이 아니라 정답을 맞힐 때까지 다시 질문하는 이유이다.

## 5.7. `break`

#   

```
break
```

반복을 끝낸다.

정답을 맞히면 게임을 종료할 때 사용한다.

# 6. Replit에서 직접 실행하기

## 6.1. Python 프로젝트 준비

#   

1. Replit에 로그인한다.
    
2. 새 Python 프로젝트 또는 Python을 실행할 수 있는 프로젝트를 연다.
    
3. Python 파일을 확인한다.
    
4. 기본 파일은 일반적으로 `main.py`로 사용한다.
    
5. 기존 예제 코드가 있다면 삭제한다.
    
6. 강사가 제공한 Python 코드를 붙여넣는다.
    

## 6.2. 실행

#   

1. 상단의 `Run` 버튼을 누른다.
    
2. Console 창을 확인한다.
    
3. 다음과 같은 문장이 나타나는지 확인한다.
    

```
Guess a number from 1 to 100:
```

4. 숫자를 입력한다.
    
5. `Too low!`, `Too high!`, `Correct!` 중 어떤 결과가 나타나는지 확인한다.
    
6. 정답을 맞힐 때까지 게임을 계속한다.
    

# 7. 코드를 직접 바꾸어 보기

## 7.1. 미션 1 — 숫자의 범위 변경

#   

현재 코드:

```
answer = random.randint(1, 100)
```

다음과 같이 직접 변경한다.

```
answer = random.randint(1, 20)
```

또는

```
answer = random.randint(1, 1000)
```

### 확인할 것

#   

숫자의 범위가 작아지면 게임은 쉬워지는가?

범위가 커지면 게임은 어려워지는가?

## 7.2. 미션 2 — 안내 문장 변경

#   

현재 코드:

```
print("Too low!")
```

학생이 원하는 문장으로 수정한다.

예:

```
print("Go higher!")
```

또는 몽골어 문장을 AI에게 번역하여 넣을 수 있다.

## 7.3. 미션 3 — 게임 제목 추가

#   

게임 시작 부분에 다음과 같은 코드를 추가한다.

```
print("====================")
print("NUMBER GUESSING GAME")
print("====================")
```

직접 제목을 바꿔 본다.

## 7.4. 미션 4 — 플레이어 이름 받기

#   

AI에게 다음과 같이 요청한다.

```
Add a player name at the beginning of the game.

Ask the player for their name and use the name when they win.

Keep the code simple.
Show only the changed parts first.
```

예상되는 코드:

```
player_name = input("What is your name? ")
```

게임 종료 시:

```
print("Correct!", player_name)
```

# 8. 강사 시연 Ⅱ — 게임 기능 추가하기

## 8.1. 시도 횟수 만들기

#   

현재 게임은 무제한으로 숫자를 입력할 수 있다.

AI에게 다음과 같이 요청한다.

```
Modify the game so the player has only 10 attempts.

Show the number of attempts left after every guess.

Keep the code simple for beginners.
Explain what new variables and conditions you added.
```

## 8.2. 수정된 코드에서 찾을 것

#   

새로운 코드가 나오면 다음 요소를 찾는다.

- 시도 횟수를 저장하는 변수
    
- 한 번 입력할 때마다 횟수를 줄이는 코드
    
- 횟수가 0이 되었는지 확인하는 조건
    
- 게임 오버를 출력하는 코드
    

## 8.3. 변경 전과 변경 후 비교

#   

학생은 다음 질문에 답한다.

1. 새로 생긴 변수의 이름은 무엇인가?
    
2. 어떤 줄에서 숫자가 감소하는가?
    
3. 게임 종료 조건은 어디에 있는가?
    
4. 기존 코드 중 그대로 남은 부분은 무엇인가?
    

# 9. 학생 기능 추가 챌린지

## 9.1. Level 1 — 쉬운 변경

#   

다음 중 하나를 선택한다.

### 숫자 범위 변경

```
Change the number range from 1-100 to 1-50.
```

### 시도 횟수 변경

```
Give the player only 5 attempts.
```

### 게임 메시지 변경

```
Make the game messages more funny.
Use simple English.
```

### 몽골어 인터페이스

```
Translate all game messages into Mongolian.
Keep the Python code itself unchanged.
```

## 9.2. Level 2 — 새로운 기능

#   

### 점수 시스템

```
Add a score system.

Start with 100 points.
Subtract 10 points for every wrong guess.
Show the final score when the player wins.
Keep the code beginner-friendly.
```

### 힌트 시스템

```
Add a hint after 3 wrong guesses.

Tell the player whether the answer is odd or even.
Keep the code simple.
```

### 다시 시작

```
Add a replay function.

After the game ends, ask:
"Play again? y/n"

If the player enters y, start a new game.
```

## 9.3. Level 3 — 자유 확장

#   

빠르게 완성한 학생은 다음 기능에 도전한다.

- Easy / Normal / Hard 난이도
    
- 최고 점수
    
- 랜덤 보너스 점수
    
- 제한 시간 개념 추가
    
- 숫자에 가까울수록 `Hot`, 멀수록 `Cold`
    
- 비밀 치트 코드
    
- 플레이어 2명 대결
    

# 10. 새로운 게임으로 바꾸기

## 10.1. 같은 Python 개념으로 만들 수 있는 게임

#   

숫자 맞히기 게임에서 배운 기본 구조만으로도 다양한 게임을 만들 수 있다.

### Rock Paper Scissors

필요한 개념:

- `input()`
    
- `random`
    
- `if`
    
- 변수
    

### Dice Game

필요한 개념:

- `random`
    
- 변수
    
- 조건문
    
- 점수
    

### Quiz Game

필요한 개념:

- `input()`
    
- 변수
    
- 조건문
    
- 점수
    

### Simple RPG Battle

필요한 개념:

- HP 변수
    
- 공격력 변수
    
- `random`
    
- 조건문
    
- 반복문
    

### Choose Your Own Adventure

필요한 개념:

- 사용자 입력
    
- 조건문
    
- 여러 선택지
    

# 11. 선택형 미니 프로젝트

## 11.1. 프로젝트 A — 가위바위보

#   

AI에게 다음 프롬프트를 사용한다.

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

## 11.2. 프로젝트 B — 주사위 대결

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

## 11.3. 프로젝트 C — 퀴즈 게임

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

## 11.4. 프로젝트 D — 간단한 RPG 전투

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

# 12. AI에게 코드를 설명하게 하기

## 12.1. 영어가 어려울 때

#   

다음 프롬프트를 사용한다.

```
Explain this Python code using very simple English.

Explain only:
- variables
- input
- if
- while
- random
```

## 12.2. 몽골어 설명이 필요할 때

#   

```
Explain this Python code in Mongolian for a beginner student.

Do not change the code.
Explain each important part with a short example.
```

## 12.3. 어려운 코드가 생성되었을 때

#   

AI가 지나치게 복잡한 코드를 만들면 다음과 같이 요청한다.

```
This code is too difficult.

Rewrite it for a beginner Python student.

Requirements:
- Do not use classes.
- Do not use advanced functions.
- Use simple variables, if statements, and loops.
- Keep it under 60 lines if possible.
```

# 13. 오류가 발생했을 때

## 13.1. 오류 메시지를 읽는다

#   

Python 프로그램에 문제가 생기면 Console에 오류 메시지가 나타난다.

오류 메시지를 바로 삭제하지 않는다.

어느 줄에서 문제가 발생했는지 확인한다.

## 13.2. AI에게 오류를 보여 준다

#   

다음 프롬프트를 사용한다.

```
I am a beginner learning Python.

Here is my code:

[코드 붙여넣기]

Here is the error:

[오류 메시지 붙여넣기]

Explain the problem in simple English and show me only the part I need to fix.
```

## 13.3. 오류 수정 원칙

#   

AI가 새로운 전체 코드를 제시하더라도 바로 전부 교체하지 않는다.

가능하면 다음 순서로 해결한다.

1. 오류가 난 줄을 찾는다.
    
2. AI에게 원인을 묻는다.
    
3. 수정해야 하는 부분만 확인한다.
    
4. 학생이 직접 수정한다.
    
5. 다시 실행한다.
    

# 14. 오늘 반드시 이해할 Python 개념

#   

|Python|게임에서 하는 일|
|---|---|
|변수|점수, 체력, 정답 등의 값을 저장|
|`input()`|플레이어의 입력을 받음|
|`print()`|게임 메시지를 보여 줌|
|`if`|조건을 판단|
|`elif`|다른 조건을 추가|
|`else`|나머지 경우를 처리|
|`while`|게임을 반복|
|`break`|반복을 종료|
|`random`|컴퓨터가 무작위 행동을 하게 함|

# 15. 오늘의 코드 읽기 퀴즈

## 15.1.

#   

```
lives = 3
```

`3`은 무엇을 의미할까?

## 15.2.

#   

```
if player_hp <= 0:
    print("Game Over")
```

언제 `Game Over`가 나타날까?

## 15.3.

#   

```
score = score + 10
```

이 코드가 실행되면 점수는 어떻게 변할까?

## 15.4.

#   

```
enemy = random.randint(1, 3)
```

`enemy`에는 어떤 값이 들어갈 수 있을까?

## 15.5.

#   

```
while True:
```

이 코드가 게임에서 필요한 이유는 무엇일까?

# 16. 수업 마무리

## 16.1. 완료 확인

#   

수업을 마치기 전에 다음을 확인한다.

- Python 게임 코드를 생성했다.
    
- Replit에서 Python 프로그램을 실행했다.
    
- 변수 하나 이상을 찾았다.
    
- `input()`이 어디에 사용되는지 확인했다.
    
- `if` 조건문을 찾았다.
    
- 반복문을 찾았다.
    
- 코드의 숫자 또는 문장을 직접 수정했다.
    
- 수정 후 게임을 다시 실행했다.
    
- AI에게 기능을 한 가지 이상 추가하도록 요청했다.
    
- 변경된 코드가 어디인지 확인했다.
    

## 16.2. 오늘의 핵심

#   

Vibe Coding은 AI에게 코드를 모두 맡기는 것이 아니다.

좋은 Vibe Coding을 위해서는 다음 과정을 반복한다.

> 만들기 → 실행하기 → 코드 보기 → 수정하기 → 다시 실행하기

학생이 모든 Python 문법을 암기할 필요는 없다.

하지만 자신이 만들고 있는 게임에서 다음은 찾을 수 있어야 한다.

- 어떤 값이 어디에 저장되는가?
    
- 플레이어의 입력은 어디에서 받는가?
    
- 게임은 어디에서 판단하는가?
    
- 어떤 코드가 반복되는가?
    
- 숫자를 바꾸면 무엇이 달라지는가?
    

# 17. 다음 수업 예고

#   

다음 시간에는 텍스트 화면을 넘어 **그래픽이 움직이는 Python 게임**으로 확장한다.

예정 내용:

- 게임 화면
    
- 플레이어 캐릭터
    
- `x`, `y` 좌표
    
- 키보드 입력
    
- 캐릭터 이동
    
- 장애물
    
- 충돌
    
- 점수
    
- 생명
    
- Game Over
    

다음 시간의 기본 프로젝트:

> **떨어지는 장애물 피하기 게임**

학생은 다음 중 하나를 생각해 온다.

1. 플레이어 캐릭터를 무엇으로 만들고 싶은가?
    
2. 무엇을 피하거나 잡고 싶은가?
    
3. 어떤 방법으로 점수를 얻고 싶은가?