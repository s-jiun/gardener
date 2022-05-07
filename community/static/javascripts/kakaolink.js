import * as myAPI from "./secret.js";

function sendLinkCustom(thumbnail, likeNum, commentNum, view, title, postid) {
    if (!Kakao.isInitialized()) {
        Kakao.init(myAPI.KAKAOAPIKEY)
    }
    Kakao.Link.sendCustom({
        templateId: 66239,
        templateArgs: {
            title: title,
            imageUrl: 'https://ourplant.kr' + thumbnail,
            likes: likeNum,
            comments: commentNum,
            watch: view,
            mobileWebUrl: 'community/post/' + postid,
            webUrl: 'community/post/' + postid
        }
    });
}