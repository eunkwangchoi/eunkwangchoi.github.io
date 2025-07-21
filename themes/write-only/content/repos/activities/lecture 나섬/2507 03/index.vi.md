+++
draft = false
toc = true
math = false
isCJKLanguage = false
author = "최은광"
title = "[Tháng 7 năm 2025] Bài 2 | Nhập môn Kỹ thuật Viết lệnh (Prompt Engineering)"
date = 2025-07-11
expiryDate = 2099-12-31
languages = "Tiếng Việt"
layout = "single-multilinguial"
+++

Chương trình giáo dục AI tạo sinh phối hợp cùng Trường Thanh thiếu niên châu Á NASEOM
Thư viện Thông tin Gwangjin | Tháng 7 năm 2025

<!--more--> 

# 0. Trước Khi Vào Bài Học

#

- Tạo tài khoản AI video : Runway https://runwayml.com, Bing (Microsoft) https://www.bing.com/create
- Mô hình AI tạo ảnh mới : Mage.Space https://www.mage.space


# 1.  Prompt là gì?

#

- Kiểm tra kết quả buổi học trước
- Ba phong cách prompt : 달리(Dall·E), 미드저니(MidJourney), 스테이블 디퓨전(Stable Diffusion)

|Tên mô hình|Ví dụ Prompt|Cách nói hiệu quả|Gợi ý thêm (Negative Prompt)|
|---|---|---|---|
|**DALL·E**|`A cute cat sitting on a sofa, photorealistic`<br>귀여운 고양이가 소파에 앉아 있는 모습, 사진처럼|**문장처럼 부드럽게 말하기**👉 AI가 문장을 잘 이해해서 자연스럽게 그림을 그림|❌ 없음(싫은 건 따로 말 못 함)|
|**MidJourney**|`cute cat, sofa, photorealistic, 4k, soft lighting`<br>귀여운 고양이, 소파, 4K 화질, 부드러운 조명|**중요한 단어만 나열하기**👉 예쁜 그림을 잘 그리지만, 문장은 못 알아들음|⚠️ 거의 없음(간단한 표현으로 조절 가능)|
|**Stable Diffusion**|`a cute cat on a sofa, digital painting, ultra detailed`<br>소파 위에 귀여운 고양이, 디지털 그림 스타일, 아주 자세하게|**단어 + 스타일 + 조명까지 넣기**👉 그림 스타일과 느낌을 내가 정할 수 있음|✅ 있음!**싫은 건 미리 말하기**예: `blurry, ugly, extra limbs`→ 흐릿한 거, 못생긴 거, 다리 이상한 거 ❌|

#

- Phân biệt phong cách prompt
- Đoán mô hình phù hợp với prompt

# 2. Prompt Tốt vs Prompt Kém

#

## 2.1. Prompt Kém

#

`dog`

#

* Quá ngắn và không rõ ràng
* Không nói rõ con chó như thế nào, ở đâu, phong cách gì
* Kết quả chỉ là hình ảnh chó đơn giản

## 2.2. Prompt Tốt

#

`a cute golden retriever puppy wearing a red scarf, sitting in a green park, cartoon style`

* 4W1H + Phong cách
* Là con gì → Chó Golden Retriever
* Như thế nào → Dễ thương, đeo khăn đỏ
* Ở đâu → Trong công viên
* Phong cách → Phong cách hoạt hình


# 3. Thực hành Viết Prompt

#

Viết prompt bằng AI văn bản (có dịch)

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


# 4. Viết Storyboard để tạo video
