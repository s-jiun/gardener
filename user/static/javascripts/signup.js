const requestCheckEmail = new XMLHttpRequest();
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
    const element = document.getElementById("id_message");
    const button = document.getElementById("sign_up");
    if (return_code === 0) {
      element.innerHTML = `
      이미 사용중인 아이디입니다.
      `;
      element.style.color = "red";
      button.disabled = true;
    } else {
      element.innerHTML = `
      사용 가능한 아이디입니다. 
      `;
      element.style.color = "blue";
      button.disabled = false;
    }
  }
};

requestCheckId.onreadystatechange = () => {
  if (requestCheckId.readyState === XMLHttpRequest.DONE) {
    checkIdHandleResponse();
  }
};

const checkEmail = () => {
  user_email = document.getElementById("id_email").value;
  const url = "/checkEmail/";
  requestCheckEmail.open("POST", url, true);
  requestCheckEmail.setRequestHeader(
    "Content-Type",
    "application/x-www-form-urlencoded"
  );
  requestCheckEmail.send(JSON.stringify({ user_email: user_email }));
};

const checkEmailHandleResponse = () => {
  if (requestCheckEmail.status < 400) {
    const { return_code } = JSON.parse(requestCheckEmail.response);
    const element = document.getElementById("email_message");
    const button = document.getElementById("sign_up");
    if (return_code === 0) {
      element.innerHTML = `
      이미 사용중인 이메일입니다.
      `;
      element.style.color = "red";
      button.disabled = true;
    } else {
      element.innerHTML = `
      사용 가능한 이메일입니다. 
      `;
      element.style.color = "blue";
      button.disabled = false;
    }
  }
};

requestCheckEmail.onreadystatechange = () => {
  if (requestCheckEmail.readyState === XMLHttpRequest.DONE) {
    checkEmailHandleResponse();
  }
};