//HTML에서 id가 signup-form인 폼 엘리먼트를 찾는다.
const form = document.querySelector("#signup-form");

//비밀번호 확인
const checkPassword = () => {
  const formData = new FormData(form);
  const password1 = formData.get("password");
  const password2 = formData.get("password2");

  if (password1 === password2) {
    return true;
  } else return false;
};

//비밀번호를 해싱하는 로직. 사용자가 폼을 제출하면 이 함수가 호출됨.
const handleSubmit = async (event) => {
  event.preventDefault(); //제출 버튼을 누르자마자 페이지가 새로고침 되는 걸 막아줌
  const formData = new FormData(form); //HTML 폼에서 데이터가 오면 FormData객체를 만든다.
  const sha356Password = sha256(formData.get("password")); //객체에서 비밀번호만 추출한 뒤, sha256 해시 함수를 사용해 해싱한다.
  formData.set("password", sha356Password); //해싱된 비번을 폼 데이터에 다시 집어넣기
  const div = document.querySelector("#info");

  if (checkPassword()) {
    //비밀번호 확인
    const res = await fetch("/signup", {
      method: "POST",
      body: formData,
    }); //fetch() 함수를 이용해 서버로 (body에 formdata를 포함해) POST요청을 보낸다.
    const data = await res.json(); //서버에서 온 응답을 JSON형식으로 바꾼다.
    if (data === "200") {
      //회원가입에 성공한 경우
      alert("회원가입에 성공했습니다. 로그인 창으로 이동합니다.");
      window.location.pathname = "/login.html";
    } else {
      //회원가입에 실패한 경우
      div.innerText = "비밀번호가 같지 않습니다.";
      div.style.color = "red";
    }
  }
};
//폼 제출 이벤트에 핸들러를 추가
form.addEventListener("submit", handleSubmit);
