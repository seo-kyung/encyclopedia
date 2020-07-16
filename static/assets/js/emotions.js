$(document).ready(function () {
  //UI 상수
  var write = document.getElementById("write");
  var close = document.getElementById("close");
  var save = document.getElementById("save");
  var deletes = document.getElementById("delete");
  var pop_Layer = document.getElementsByClassName("pop-up");

  //pop-up 데이터 상수
  var pageTitle = document.title;
  var author = document.getElementsByName("author")[0];
  var title = document.getElementsByName("title")[0];
  var corpus = document.getElementsByName("corpus")[0];
  var count = document.getElementsByClassName("counts")[0];

  //팝업창 보이기
  write.onclick = function () {
    pop_Layer[0].style.display = "block";
  };

  //삭제창
  var isClicked = false;
  var delete_icon = document.getElementById("deleteImg");

  deletes.addEventListener("click", function () {
    if (isClicked) {
      //삭제 모드 취소
      isClicked = false;
      //img change
      delete_icon.src = "/static/assets/img/delete_icon.png";
      //스크롤 다시 시작
      doScroll();
      autoScroll();
      //이벤트 제거
      clearDeleteMode();
    } else {
      //삭제 모드
      isClicked = true;
      //img change
      delete_icon.src = "/static/assets/img/delete_save_icon.png";
      //스크롤 멈춤
      stopScroll();
      //삭제 화면
      deleteMode();
    }
  });

  //textarea 내용 지우고 팝업창 닫기
  function clear() {
    author.value = "";
    title.value = "";
    corpus.value = "";
    corpus.style.borderColor = "black";
    pop_Layer[0].style.display = "none";
  }

  // var mySwiper = new Swiper(".swiper-container", {
  //   direction: "vertical",
  //   slidesPerView: "auto",
  //   speed: 1200,
  //   autoplay: {
  //     delay: 1000,
  //     disableOnInteraction: false,
  //   }
  // });

  var contentsList = document.getElementsByClassName("contents");

  function deleteContents() {
    console.log(this.dataset.timestamp);
    $.ajax({
      url: "/entry",
      method: "delete",
      data: {
        timestamp: this.dataset.timestamp,
      },
      success: function () {
        location.reload();
      },
    });
  }

  function mouseoverEvent() {
    this.style.opacity = 0.13;
    this.style.cursor = "pointer";
  }

  //attach eventlistener
  function deleteMode() {
    for (var i = 0; i < contentsList.length; i++) {
      //hover effect
      contentsList[i].onmouseout = function () {
        this.style.opacity = 1;
        this.style.cursor = "default";
      };
      contentsList[i].addEventListener("mouseover", mouseoverEvent);
      contentsList[i].addEventListener("click", deleteContents);
    }
  }

  //remove eventlistener
  function clearDeleteMode() {
    for (var i = 0; i < contentsList.length; i++) {
      contentsList[i].removeEventListener("mouseover", mouseoverEvent);
      contentsList[i].removeEventListener("click", deleteContents);
    }
  }

  var target = document.getElementsByClassName("hiddenScroll")[0];
  var isScroll = true;

  var myTimer;
  var autoScroll = function () {
    target.scrollTop += 1;
    myTimer = setTimeout(autoScroll, 50);
  };

  //스크롤 재시작
  var doScroll = function () {
    isScroll = true;
    //스크롤 위로 올리기
    target.scrollTop = 0;
  };
  //스크롤 멈춤
  var stopScroll = function () {
    isScroll = false;
    clearTimeout(myTimer);
  };

  autoScroll();
});
