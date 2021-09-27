const requestFollowerDelete = new XMLHttpRequest();

const onClickFollowerDelete = (user_id) => {
  const url = "/follower_delete_ajax/";
  requestFollowerDelete.open("POST", url, true);
  requestFollowerDelete.setRequestHeader(
    "Content-Type",
    "application/x-www-form-urlencoded"
  );
  requestFollowerDelete.send(JSON.stringify({ user_id: user_id }));
};

const followerDeleteHandleResponse = () => {
  if (requestFollowerDelete.status < 400) {
    const { user_id,  user_name, user_point, user_image_url, user_userid  } = JSON.parse(requestFollowerDelete.response);
    // const element = document.querySelectorAll(`.follow-wraper-${user_id}`);
    // const followingObject = document.querySelector(`.follow-object-${user_id}`)
    // console.log(element);
    // element[0].innerHTML = `
    //     <div class="follow-${user_id}" style="display:inline;">
    //     <button onclick="onClickFollow(${user_id})" style="background: white; border: 1px solid #ACA790; padding:5px; border-radius:10px; font-size:16px;">팔로우</button>
    //     </div>
    //     `;
    // followingObject.remove(followingObject)
    // const is_list_Conatiner1 = document.querySelector(`.following-box #follow-user-box1`)
    // const is_list_Conatiner2 = document.querySelector(`.following-box #follow-user-box2`)
    
    // if ((is_list_Conatiner1 == null) && (is_list_Conatiner2 == null)) {
      //   const listConatiner = document.querySelector('.list-container')
      //   listConatiner.innerHTML += `
      //   <div class="text-center" style="margin-top: 50px; height: 300px;">
      //   <h4> 아직 함께하는 가드너가 없네요
      //   <img src="/static/images/sad.svg" alt="" style="width: 30px; height: 30px;"></h4>
      //   </div>`
      // }
    const follower_object = document.querySelector(`#follower-div-${user_id}`);
    follower_object.remove(follower_object)
    const followers = document.querySelector(`.follower-div`);
    if (followers == null) {
      const follower_box = document.querySelector(`#follower-box`);
      follower_box.innerHTML = `아직 함께하는 팔로워가 없어요.`
    }
      
  }
};

requestFollowerDelete.onreadystatechange = () => {
  if (requestFollowerDelete.readyState === XMLHttpRequest.DONE) {
    followerDeleteHandleResponse();
  }
};

const requestFollowingDelete = new XMLHttpRequest();

const onClickFollowingDelete = (user_id) => {
  const url = "/following_delete_ajax/";
  requestFollowingDelete.open("POST", url, true);
  requestFollowingDelete.setRequestHeader(
    "Content-Type",
    "application/x-www-form-urlencoded"
  );
  requestFollowingDelete.send(JSON.stringify({ user_id: user_id }));
};

const followingDeleteHandleResponse = () => {
  if (requestFollowingDelete.status < 400) {
    const { user_id} = JSON.parse(requestFollowingDelete.response); 
    // const element = document.querySelectorAll(`.follow-wraper-${user_id}`);
    // console.log(element);
    // element[0].innerHTML = `    
    //     <div class='following-${user_id}' style="display:inline;">
    //     <button onclick="onClickFollowing(${user_id})"  style="background: white; border: 1px solid #ACA790; padding:5px; border-radius:10px; font-size:16px;">팔로잉</button>
    //     </div>
    //     `;
    // const listConatiner = document.querySelector('.list-container')
    // const is_list_Conatiner = document.querySelector(`.following-box #follow-user-box1`)
    // const box1 = document.querySelectorAll(`#follow-user-box1`)
    // const box2 = document.querySelectorAll(`#follow-user-box2`)
    // console.log(listConatiner)
    // if (is_list_Conatiner == null)
    //   listConatiner.innerHTML=''
    
    // listConatiner.innerHTML += `
    // <div class="row row-cols-2 row-cols-lg-2 p-3 follow-object-${user_id}" id="follow-user-box1">  
    // <div class="col p-0 mt-2" id="follow-user-img">
    // <img src="${user_image_url}">
    // </div>
    // <div class="col" style="width:80%">
    // <h5 id="follow-name">
    // <img src="/static/images/ID.png" alt="" style="width:20px; height:20px; margin-bottom: 5px;">
    // ID : ${user_userid}</h5>
    // <div class="follow-wraper-${user_id}" style="display:inline; ">
    // <div class="following-${user_id}" style="display:inline;"> 
    // <button onclick="onClickFollowing(${user_id})" style="background: white; border: 1px solid #ACA790; padding:5px; border-radius:10px; font-size:16px;">팔로잉</button>
    // </div>
    // </div>
    // <hr class="m-1">
    // <span> &nbsp; Name : ${user_name}</span><br>
    // <span> &nbsp; Point : ${user_point}</span>
    // </div>
    // </div>
    // `
    const following_object = document.querySelector(`#following-div-${user_id}`);
    following_object.remove(following_object)
    const followings = document.querySelector(`.following-div`);
    if (followings == null) {
      const following_box = document.querySelector(`#following-box`);
      following_box.innerHTML = `아직 함께하는 팔로워가 없어요.`
    }
  }
};
requestFollowingDelete.onreadystatechange = () => {
  if (requestFollowingDelete.readyState === XMLHttpRequest.DONE) {
    followingDeleteHandleResponse();
  }
};

//  not my profile
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
    const { user_id, user_name, user_point, user_image_url, user_userid } = JSON.parse(requestOtherFollowing.response); 
    const element = document.querySelectorAll(`.follow-wraper-${user_id}`);
    console.log(element);
    if (element.length>1){

      element[0].innerHTML = `    
      <div class='follow-${user_id}' style="display:inline;">
      <button class="follow-btn" onclick="onClickOtherDeleteFollow(${user_id})">팔로우 취소</button>
      </div>
      `;
      
      element[1].innerHTML = `    
      <div class='follow-${user_id}' style="display:inline;">
      <button class="follow-btn" onclick="onClickOtherDeleteFollow(${user_id})">팔로우 취소</button>
      </div>
      `;
    }
    else {
      element[0].innerHTML = `    
      <div class='follow-${user_id}' style="display:inline;">
      <button class="follow-btn" onclick="onClickOtherDeleteFollow(${user_id})">팔로우 취소</button>
      </div>
      `;
    }
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
    const { user_id, user_name, user_point, user_image_url, user_userid } = JSON.parse(requestOtherDeleteFollow.response); 
    const element = document.querySelectorAll(`.follow-wraper-${user_id}`);
    console.log(element);
    if (element.length>1){

      element[0].innerHTML = `    
      <div class='following-${user_id}' style="display:inline;">
      <button class="follow-btn" onclick="onClickOtherFollowing(${user_id})">팔로우</button>
      </div>
      `;
      
      element[1].innerHTML = `    
      <div class='following-${user_id}' style="display:inline;">
      <button class="follow-btn" onclick="onClickOtherFollowing(${user_id})">팔로우</button>
      </div>
      `;
    }
    else {
      element[0].innerHTML = `    
      <div class='following-${user_id}' style="display:inline;">
      <button class="follow-btn" onclick="onClickOtherFollowing(${user_id})">팔로우</button>
      </div>
      `;
    }
      
  }
};
requestOtherDeleteFollow.onreadystatechange = () => {
  if (requestOtherDeleteFollow.readyState === XMLHttpRequest.DONE) {
    otherFollowHandleResponse();
  }
};