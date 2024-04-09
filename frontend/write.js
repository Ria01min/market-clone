const form = document.getElementById("write-form");

const hadleSubmitForm = async (event) => {
  event.preventDefault();
  //업로드한 시간을 넣어주기 위함
  const body = new FormData(form);
  //세계시간 기준으로
  body.append("insertAt", new Date().getTime());
  //try catch구문은 try 안에 있는 로직을 한 번 시도해보다가  error(e)가 발생하면 catch 로직이 실행되는 문법
  try {
    //서버로 보냄
    const res = await fetch("/items", {
      method: "POST",
      body: body, //업로드한 시간을 넣어주기 위함 (그냥 body, 이렇게 써도 무방함)
    });
    //서버로부터 오는 응답
    const data = await res.json();
    if (data == "200") window.location.pathname = "/"; //서버 업로드에 성공하면 페이지를 메인페이지로 전환
  } catch (e) {
    console.error(e);
  }
};

form.addEventListener("submit", hadleSubmitForm);
