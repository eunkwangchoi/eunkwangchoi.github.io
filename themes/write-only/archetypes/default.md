+++
draft = true
math = false
isCJKLanguage = true

layout = ""
weight = 0

aliases = ""
slug = ""
url = ""

author = "Eunkwang Ryan Choi"
contributor = ""

title = '{{ replace .File.ContentBaseName "-" " " | title }}'
description = ""

date = '{{ .Date }}'
expiryDate = 2099-12-31

arts = [ "" ]
techs = [ "" ]
refs = [ "" ]
etcs = [ "" ]

languages = ""

locs = [ "" ]
+++


{{< youtube ZJthWmvUzzc >}}
![cat](../../images/insta-201102.jpg)

<a href="https://munjang.or.kr/board.es?mid=a20204000000&bid=0011&act=view&ord=B&list_no=101979&nPage=2&c_page=" target="_blank" rel="noopener noreferrer">원문: 문장웹진</a>

<div style="text-align: center;">
    <a href="https://talk.naver.com/W448DX" target="_blank" rel="noopener noreferrer">네이버 톡톡</a>
</div>


art list
	Categories
		영화, 음악, 미술, 건축, 문학, 사진, 디자인
	Formats
		전시, 공연, 음반

tech list
	Generative AI
		MidJourney
	Google
		Google Search
	Sound Tech
		Dolby
		Soundscape
	Literature & Latte
		Scrivener
	Microsoft
		Onedrive
		MS (Office) 365


etc list
	Activities
		독서, 여행, 명상, 취미, 불사
	Works
		집필, 작업
	Companions
		야옹이, 아내


hugo mod clean --all
Remove-Item -Recurse -Force resources, public
hugo --cleanDestinationDir
