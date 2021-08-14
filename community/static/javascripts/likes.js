const requestLike = new XMLHttpRequest();

const onClickLike = (id) => {
    const url = 'like_ajax/';
    requestLike.open('POST', url, true);
    requestLike.setRequestHeader(
        'Content-Type',
        'application/x-www-form-urlencoded'
    );
    requestLike.send(JSON.stringify({id: id}));
};

const likeHandleResponse = () => {
    if(requestLike.status < 400){
        const {id, like_count} = JSON.parse(requestLike.response);
        const element1 = document.querySelector(`.post-id-${id} .heart`);
        const element2 = document.querySelector(`.post-id-${id} .like_num`);
        const heart = element1.innerHTML;
        if (heart=='<i class="fas fa-heart"></i>'){
            element1.innerHTML=`<i class="far fa-heart"></i>`
            element2.innerHTML = `좋아요 ${like_count}`
        }else if(heart=='<i class="far fa-heart"></i>'){
            element1.innerHTML=`<i class="fas fa-heart"></i>`
            element2.innerHTML = `좋아요 ${like_count}`
        }
    }
}

requestLike.onreadystatechange = () => {
    if(requestLike.readyState === XMLHttpRequest.DONE){
        likeHandleResponse();
    }
};