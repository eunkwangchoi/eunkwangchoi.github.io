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
<center><a href="https://ko.wikipedia.org/wiki/%EC%84%9C%EC%B9%AD_%ED%8F%AC_%EC%8A%88%EA%B0%80%EB%A7%A8" target="_blank" rel="noopener noreferrer">Searching for Sugarman (2012)</a></center>


art list
	Categories
		영화, 음악, 미술, 건축, 문학, 사진, 디자인
	Formats
		전시, 공연

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
