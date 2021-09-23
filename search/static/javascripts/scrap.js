const requestScrap = new XMLHttpRequest();

const onClickScrap = (Id) => {
  const url = "scrap_ajax/";
  requestScrap.open("POST", url, true);
  requestScrap.setRequestHeader(
    "Content-Type",
    "application/x-www-form-urlencoded"
  );
  requestScrap.send(JSON.stringify({ Id: Id }));
};

const ScrapHandleResponse = () => {
  if (requestScrap.status < 400) {
    const { id, type } = JSON.parse(requestScrap.response);
    const element = document.querySelector(
      `#plantDetailModal-${id} .post__${type}`
    );
    if (type == "del_scrap") {
      element.classList.replace(`post__${type}`, "post__scrap");
      element.innerHTML = `<img class="profile-post-header__img" src="/static/images/mark_line.svg" />`;
    } else {
      element.classList.replace(`post__${type}`, "post__del_scrap");
      element.innerHTML = `<img class="profile-post-header__img" src="/static/images/mark_fill.svg" />`;
    }
  }
};

requestScrap.onreadystatechange = () => {
  if (requestScrap.readyState === XMLHttpRequest.DONE) {
    ScrapHandleResponse();
  }
};

function SelectHandleOnchange(e) {
  const text = e.options[e.selectedIndex].text;
  const search_box = document.getElementById("search_option");
  if (text == "경험자") {
    search_box.innerHTML = "";
    search_box.innerHTML += `<a href='?type=managelevel&q=초보자' class='btn mx-1'>초보자</a>`;
    search_box.innerHTML += `<a href='?type=managelevel&q=경험자' class='btn mx-1'>경험자</a>`;
    search_box.innerHTML += `<a href='?type=managelevel&q=전문가' class='btn mx-1'>전문가</a>`;
  }
}
