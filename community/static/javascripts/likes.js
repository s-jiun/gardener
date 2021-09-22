const requestLike = new XMLHttpRequest();

const onClickLike = (id) => {
  console.log("아이디", id);
  const url = "like_ajax/";
  requestLike.open("POST", url, true);
  requestLike.setRequestHeader(
    "Content-Type",
    "application/x-www-form-urlencoded"
  );
  requestLike.send(JSON.stringify({ id: id }));
};

const likeHandleResponse = () => {
  if (requestLike.status < 400) {
    const { id, like_count } = JSON.parse(requestLike.response);
    const element1 = document.querySelector(`.post-id-${id} .heart`);
    const element2 = document.querySelector(`.post-id-${id} .like_num`);
    const heart = element1.innerHTML;
    console.log(heart);
    if (
      heart ==
      `<img class="me-1" src="/static/images/heart_line.svg" alt="하트">`
    ) {
      element1.innerHTML = `<img class='me-1' src='/static/images/heart_fill.svg' alt='하트'>`;
      element2.innerHTML = ` ${like_count}`;
    } else {
      element1.innerHTML = `<img class="me-1" src="/static/images/heart_line.svg" alt="하트">`;
      element2.innerHTML = ` ${like_count}`;
    }
  }
};

requestLike.onreadystatechange = () => {
  if (requestLike.readyState === XMLHttpRequest.DONE) {
    likeHandleResponse();
  }
};
