+++
draft = false
toc = true
math = false
isCJKLanguage = false
author = "최은광"
title = "[2025 оны 7-р сар] Хичээл 2 | Промпт инженерчлэлийн үндэс"
date = 2025-07-11
expiryDate = 2099-12-31
languages = "Монгол"
layout = "single-multilinguial"
+++

Генератив AI ашиглах сургалт — Насом Азийн Залуучуудын Сургуулийн хамт
Гванжин мэдээллийн номын сан | 2025 оны 7-р сар

<!--more--> 

# 0. 수업에 들어가기에 앞서

#

- 영상 AI 계정 만들기 : Runway https://runwayml.com, Bing (Microsoft) https://www.bing.com/create
- 새로운 이미지 AI 모델 : Mage.Space https://www.mage.space


# 1. 프롬프트란 무엇인가?

#

- 지난 시간 결과물 확인
- 세 가지 스타일의 프롬프트 : 달리(Dall·E), 미드저니(MidJourney), 스테이블 디퓨전(Stable Diffusion)

|모델 이름|프롬프트 예시|어떻게 말해야 잘 나올까?|추가 팁 (Negative Prompt)|
|---|---|---|---|
|**DALL·E**|`A cute cat sitting on a sofa, photorealistic`<br>귀여운 고양이가 소파에 앉아 있는 모습, 사진처럼|**문장처럼 부드럽게 말하기**👉 AI가 문장을 잘 이해해서 자연스럽게 그림을 그림|❌ 없음(싫은 건 따로 말 못 함)|
|**MidJourney**|`cute cat, sofa, photorealistic, 4k, soft lighting`<br>귀여운 고양이, 소파, 4K 화질, 부드러운 조명|**중요한 단어만 나열하기**👉 예쁜 그림을 잘 그리지만, 문장은 못 알아들음|⚠️ 거의 없음(간단한 표현으로 조절 가능)|
|**Stable Diffusion**|`a cute cat on a sofa, digital painting, ultra detailed`<br>소파 위에 귀여운 고양이, 디지털 그림 스타일, 아주 자세하게|**단어 + 스타일 + 조명까지 넣기**👉 그림 스타일과 느낌을 내가 정할 수 있음|✅ 있음!**싫은 건 미리 말하기**예: `blurry, ugly, extra limbs`→ 흐릿한 거, 못생긴 거, 다리 이상한 거 ❌|

#

- 프롬프트 스타일 판단해 보기
- 프롬프트 모델 판단해 보기

# 2. 좋은 프롬프트 vs 나쁜 프롬프트

#

## 2.1. 나쁜 프롬프트

#

`dog`

#

- 너무 짧고 모호함
- 어떤 강아지인지, 어떤 상황인지, 어떤 스타일인지 알 수 없음
- 기본적인 강아지 모습만 나옴 (종류, 감정, 배경 등 불분명)

## 2.2. 좋은 프롬프트

#

`a cute golden retriever puppy wearing a red scarf, sitting in a green park, cartoon style`

- 4W1H + 스타일
- 무엇을(어떤 강아지?) → 골든 리트리버    
- 어떻게(어떤 모습?) → 귀엽고 강아지, 스카프 착용    
- 어디에(장소는?) → 공원    
- 어떤 스타일? → 만화 스타일


# 3. 프롬프트 작성 실습

#

텍스트 AI를 이용한 프롬프트 작성 (번역 포함)

## 🎨 3.1. **Style Keywords (스타일/화풍)**

#

> _그림의 전체적인 분위기나 표현 방식_

#

- cartoon style    
- digital painting    
- watercolor    
- 3D render    
- pixel art    
- concept art    
- anime style    
- comic book style    
- photorealistic    
- minimalist    
- line drawing    
- vaporwave    
- fantasy art    
- surrealism    
- isometric view    

## 😊 3.2. **Emotion & Mood Keywords (감정/분위기)**

#

> _장면의 감정, 느낌_

#

- happy    
- sad    
- peaceful    
- dreamy    
- mysterious    
- lonely    
- warm    
- dark    
- cozy    
- scary    
- magical    
- romantic    
- angry    
- energetic    
- futuristic    

## 🌆 3.3. **Background & Setting (배경/장소)**

#

> _어디서 일어나는지_

#

- forest    
- city    
- beach    
- desert    
- mountain    
- space    
- underwater    
- bedroom    
- library    
- amusement park    
- classroom    
- village    
- battlefield    
- moon    
- sky    


## 👤 3.4. **Character Appearance (인물 외형/의상)**

#

> _사람이나 캐릭터의 모습_

#

- young girl / boy    
- old man / woman    
- astronaut    
- robot    
- wizard    
- warrior    
- fairy    
- vampire    
- pirate    
- superhero    
- wearing glasses    
- with a hat    
- long hair    
- in armor    
- wearing hanbok / kimono    

## 🐶 3.5. **Animal Keywords (동물/생물)**

#

> _등장하는 동물_

#

- cat    
- dog    
- rabbit    
- dinosaur    
- tiger    
- penguin    
- owl    
- dragon    
- fox    
- elephant    
- octopus    
- whale    
- bird    
- mouse    
- turtle    

## 🎬 3.6. **Action Verbs (동작/활동)**

#

> _무엇을 하는지_

#

- dancing    
- running    
- flying    
- sleeping    
- reading    
- painting    
- swimming    
- singing    
- jumping    
- playing guitar    
- building    
- looking at stars    
- cooking    
- crying    
- laughing    

## 💡 3.7. **Lighting & Effects (조명/효과)**

#

> _빛과 장면 효과_

#

- soft lighting    
- glowing    
- neon lights    
- cinematic lighting    
- golden hour    
- spotlight    
- foggy    
- dramatic light    
- fireflies    
- backlight    
- moonlight    
- rainbow light    
- under lighting    
- reflections    
- shadowy    

## 👁 3.8. **Perspective & Angle (시점/구도)**

#

> _그림을 보는 위치_

#

- from above    
- top-down view    
- side view    
- close-up    
- wide shot    
- over the shoulder    
- front view    
- behind the character    
- isometric    
- bird's-eye view    
- first person view    

## 🖼 3.9. **Media Type (매체/목적)**

#

> _무엇을 위한 그림인지_

#

- book illustration    
- game concept art    
- movie poster    
- children’s book    
- comic cover    
- trading card    
- magazine cover    
- background for animation    
- character design    
- logo art    

#

## 3.10. 활용 예시 (조합)

#

> `A happy astronaut dancing on the moon at sunset, cartoon style, soft lighting`  
> → 감정 + 인물 + 장소 + 시간 + 스타일 + 조명

#

> `A lonely robot reading a book in an old library, warm light, digital painting`  
> → 감정 + 캐릭터 + 배경 + 조명 + 스타일

#

> `A tiger with glasses flying over a cyberpunk city, concept art, glowing lights`  
> → 동물 + 외형 + 동작 + 배경 + 스타일 + 효과


# 4. 영상 제작을 위한 스토리보드 작성
