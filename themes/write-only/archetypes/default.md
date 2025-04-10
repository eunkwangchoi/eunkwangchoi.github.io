+++
draft = true
toc = false
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


<script src="https://cdn.fastcomments.com/js/embed-v2.min.js"></script>
  <div id="fastcomments-widget"></div>
  <script>
	FastCommentsUI(document.getElementById('fastcomments-widget'), {
	  tenantId: 'kYpW2ra3fpa'
	});
</script>


art list
	Categories
		영화, 음악, 미술, 건축, 문학, 사진, 디자인
	Formats
		전시, 공연, 음반

tech list
	Adobe
		Behance
		Adobe CC
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

ref list
	Philosophers
		Arendt, Hannah
		Rorty, Richard
		Aquinas, Thomas
	Historians
		Gombrich, Ernst
	Clerics
		Nouwen, Henry
	Artists
		Warhol, Andy
		Rodriguez, Sixto
		Bosch, Hieronymus
		Fitzgerald, Scott
		Koons, Jeff
		Lichtenstein, Roy
		Matisse, Henri
		Basquiat, Jean-Michel
		Opie, Julian
		村上 春樹
		村上 隆
		세븐틴

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
