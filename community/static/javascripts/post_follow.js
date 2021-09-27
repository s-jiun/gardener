const requestOtherFollowing = new XMLHttpRequest();

const onClickOtherFollowing = (user_id) => {
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
    const element = document.querySelector(`#follow-wrapper`);
    console.log(element);
    element.innerHTML = `    
    <button type="button" class="btn btn-outline-success" onclick="onClickOtherDeleteFollow(${user_id})" id="post-follow-button">팔로우 취소</button>
    `;
  }
};

requestOtherFollowing.onreadystatechange = () => {
  if (requestOtherFollowing.readyState === XMLHttpRequest.DONE) {
    otherFollowingHandleResponse();
  }
};

const requestOtherDeleteFollow = new XMLHttpRequest();

const onClickOtherDeleteFollow = (user_id) => {
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
    const element = document.querySelector(`#follow-wrapper`);
    element.innerHTML = `    
    <button type="button" class="btn btn-outline-success" onclick="onClickOtherFollowing(${user_id})" id="post-follow-button">팔로우</button> 
    `;
  }
};
requestOtherDeleteFollow.onreadystatechange = () => {
  if (requestOtherDeleteFollow.readyState === XMLHttpRequest.DONE) {
    otherFollowHandleResponse();
  }
};
