const requestFollowing = new XMLHttpRequest()

const onClickFollowing = (user_id) => {
    const url = '/following_ajax/';
    requestFollowing.open('POST', url, true);
    requestFollowing.setRequestHeader(
        'Content-Type',
        'application/x-www-form-urlencoded',
    );
    requestFollowing.send(JSON.stringify({user_id:user_id}))
}

const followingHandleResponse = () => {
    if (requestFollowing.status < 400) {
        const {user_id} = JSON.parse(requestFollowing.response);
        const element = document.querySelector('.follow-wrapper')
        const follower_count = document.querySelector('.follower-count')
        const count = Number(follower_count.innerHTML) + 1
        follower_count.innerHTML = `${count}`
        console.log(element)
        element.innerHTML = `
        <div class="follow">
            <button class="follow-btn" onclick="onClickDeleteFollow(${user_id})">팔로우 취소</button>
        </div>
        `

    }

}

requestFollowing.onreadystatechange = () => {
if (requestFollowing.readyState === XMLHttpRequest.DONE) {
    followingHandleResponse();
    }
}

const requestDeleteFollow = new XMLHttpRequest()

const onClickDeleteFollow = (user_id) => {
    const url = '/other_delete_ajax/';
    requestDeleteFollow.open('POST', url, true);
    requestDeleteFollow.setRequestHeader(
        'Content-Type',
        'application/x-www-form-urlencoded',
    );
    requestDeleteFollow.send(JSON.stringify({user_id:user_id}))
}

const followHandleResponse = () => {
    if (requestDeleteFollow.status < 400) {
        const {user_id} = JSON.parse(requestDeleteFollow.response);
        const element = document.querySelector(`.follow-wrapper`)
        const follower_count = document.querySelector('.follower-count')
        const count = Number(follower_count.innerHTML) - 1
        follower_count.innerHTML = `${count}`
        console.log(element)
        element.innerHTML = `    
        <div class='following'>
            <button class="follow-btn" onclick="onClickFollowing(${user_id})">팔로우</button>
        </div>`
    }

}
requestDeleteFollow.onreadystatechange = () => {
if (requestDeleteFollow.readyState === XMLHttpRequest.DONE) {
    followHandleResponse();
    }
}