1. Main 페이지
day1과 Totla corpus를 조금 위로 올릴수도 있을것같네요. 확실한건 아니지만 day1 위에 지역명이라던지 현재 date를 추가 할 수도 있을것 같아요. 

//지역명의 추가는 html + css 이해가 없으시면 불가능 할 듯 합니다.
	(해당 부분 : main.html > div footer 수정 후 css 추가 필요)
//main.css > .footer > .top > 88px을 증가시키시면 위로 올라갑니다.

2. Encyclopedia of emotion 페이지
텍스트 내용, 슬라이딩 스피드, 아이콘 크기

//enclopedia.html > <div id = "corey"> , <div id = "enclo"> 안의 내용안의 내용 수정하시면 텍스트 내용이 바뀝니다. <div class = "highlight"></div>안의 내용은 underscore부분

//scroll.js > setTimeout안의 숫자 : 0.3초(1000 : 1초) or scrollTop : 해당 초마다 올라가는 pixel

//enclopedia.css > img > width, height 바꾸기


3. (joy, anger, sadness, surprise) 페이지: corpus와 author&title 사이 간격, 슬라이딩 스피드, 아이콘 크기 조정


//emotion.css > .comments > margin-top 조정

//슬라이딩 스피드는 위와 동일(모든 페이지 통일)

//emotion.css > img > width, height %로 바꾸기

