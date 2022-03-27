const requestCheckId = new XMLHttpRequest();

const checkId = () => {
  user_id = document.getElementById("id_userid").value;
  console.log(user_id);
  const url = "/checkId/";
  requestCheckId.open("POST", url, true);
  requestCheckId.setRequestHeader(
    "Content-Type",
    "application/x-www-form-urlencoded"
  );
  requestCheckId.send(JSON.stringify({ user_id: user_id }));
};

const checkIdHandleResponse = () => {
  if (requestCheckId.status < 400) {
    const { return_code } = JSON.parse(requestCheckId.response);
    const element = document.getElementById("user_id");
    const button = document.getElementById("sign_up");
    if (return_code === 0) {
      element.innerHTML = `
        아이디 : 이미 사용중인 아이디입니다.
      `;
      button.disabled = true;
    } else {
      element.innerHTML = `
        아이디 : 사용 가능한 아이디입니다. 
      `;
      button.disabled = false;
    }
  }
};

requestCheckId.onreadystatechange = () => {
  if (requestCheckId.readyState === XMLHttpRequest.DONE) {
    checkIdHandleResponse();
  }
};

const checkPassword = () => {
  var reg = "^(?=.*[A-Za-z])(?=.*d)[A-Za-zd]{8,}$";
  var txt = "aaaa";
  if (!reg.test(txt)) {
    alert("비밀번호 정규식 규칙 위반!!");
    return false;
  }

  user_id = document.getElementById("id_userid").value;
  console.log(user_id);
  const url = "/checkId/";
  requestCheckId.open("POST", url, true);
  requestCheckId.setRequestHeader(
    "Content-Type",
    "application/x-www-form-urlencoded"
  );
  requestCheckId.send(JSON.stringify({ user_id: user_id }));
};
