const requestOtherFollowing = new XMLHttpRequest();

const onClickListFollowing = (user_id) => {
  const url = "/following_ajax/";
  requestOtherFollowing.open("POST", url, true);
  requestOtherFollowing.setRequestHeader(
    "Content-Type",
    "application/x-www-form-urlencoded"
  );
  requestOtherFollowing.send(JSON.stringify({ user_id: user_id }));
};

const otherFollowingHandleResponse = () => {
  if (requestOtherFollowing.status < 400) {
    const { user_id, user_name, user_point, user_image_url, user_userid } =
      JSON.parse(requestOtherFollowing.response);
    const element = document.querySelector(`.postcard-${user_id}`);
    console.log(element);
    const element2 = document.querySelector(`.following-count`);
    element2.innerHTML = Number(element2.innerHTML) + 1
    element.innerHTML = `    
    <a onclick="onClickListDeleteFollow(${user_id})" >팔로우 취소</a>
    `;
  }
};

requestOtherFollowing.onreadystatechange = () => {
  if (requestOtherFollowing.readyState === XMLHttpRequest.DONE) {
    otherFollowingHandleResponse();
  }
};

const requestOtherDeleteFollow = new XMLHttpRequest();

const onClickListDeleteFollow = (user_id) => {
  const url = "/other_delete_ajax/";
  requestOtherDeleteFollow.open("POST", url, true);
  requestOtherDeleteFollow.setRequestHeader(
    "Content-Type",
    "application/x-www-form-urlencoded"
  );
  requestOtherDeleteFollow.send(JSON.stringify({ user_id: user_id }));
};

const otherFollowHandleResponse = () => {
  if (requestOtherDeleteFollow.status < 400) {
    const { user_id, user_name, user_point, user_image_url, user_userid } =
      JSON.parse(requestOtherDeleteFollow.response);
    const element = document.querySelector(`.postcard-${user_id}`);
    const element2 = document.querySelector(`.following-count`);
    element2.innerHTML = Number(element2.innerHTML) - 1
    element.innerHTML = `    
    <a onclick="onClickListFollowing(${user_id})">팔로우</a>
    `;
  }
};
requestOtherDeleteFollow.onreadystatechange = () => {
  if (requestOtherDeleteFollow.readyState === XMLHttpRequest.DONE) {
    otherFollowHandleResponse();
  }
};
