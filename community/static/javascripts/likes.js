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
        console.log(heart)
        console.log(element2.innerHTML)
        if (heart=='❤️'){
            element1.innerHTML='🤍'
            element2.innerHTML = `좋아요 ${like_count}`
        }else if(heart=='🤍'){
            element1.innerHTML='❤️'
            element2.innerHTML = `좋아요 ${like_count}`
        }
    }
}

requestLike.onreadystatechange = () => {
    if(requestLike.readyState === XMLHttpRequest.DONE){
        likeHandleResponse();
    }
};