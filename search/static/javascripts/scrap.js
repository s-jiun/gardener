const requestScrap = new XMLHttpRequest();
    
const onClickScrap = (Id) => {
    const url = 'scrap_ajax/';
    requestScrap.open('POST', url, true);
    requestScrap.setRequestHeader(
        'Content-Type',
        'application/x-www-form-urlencoded'
    );
    requestScrap.send(JSON.stringify({Id: Id}));
};

const ScrapHandleResponse = () => {
    if (requestScrap.status < 400) {
        const {id, type} = JSON.parse(requestScrap.response);    // {'id': 1, 'type': 'like'}
        const element = document.querySelector(`#plantDetailModal-${id} .post__${type}`);
        if (element.innerHTML === '<i class="fas fa-bookmark"></i>') {
            element.classList.replace(`post__${type}`, 'post__scrap')
            element.innerHTML = '<i class="far fa-bookmark"></i>';
        }
        else {
            element.classList.replace(`post__${type}`, 'post__del_scrap')
            element.innerHTML ='<i class="fas fa-bookmark"></i>'
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
    const search_box = document.getElementById("search_option")
    if (text == '경험자') {
        search_box.innerHTML = ""
        search_box.innerHTML +=`<a href='?type=managelevel&q=초보자' class='btn mx-1'>초보자</a>`
        search_box.innerHTML +=`<a href='?type=managelevel&q=경험자' class='btn mx-1'>경험자</a>`
        search_box.innerHTML +=`<a href='?type=managelevel&q=전문가' class='btn mx-1'>전문가</a>`
    }
    else {
        search_box.innerHTML = ""
        search_box.innerHTML += `
        <input class="plant-input" type="text" name ='q' value="{{q}}" placeholder="검색어를 입력하세요" />
        <button class="plant-input-1" type="submit">검색</button>
        `
    }
}