// This is the content script that will be injected into web pages

console.log('Script loaded');


async function async_fetcher(method, url, data) {

    const response = await fetch(
        "http://localhost:5000/api/primary" + url,
    {
        method: method,
        mode: `cors`,
        cache: `no-cache`,
        credentials: `same-origin`,
        redirect: `follow`,
        referrerPolicy: `no-referrer`,
        body: data
    }).catch(error => {
        return {data: false}
    });

    try {
        return response.json();
    } catch(err) {
        console.log("%% Big Error:", err);
        return {data: false}
    }

}


function processImageForm() {

    const ele = iMetaImageFile = document.getElementById("iMetaImageFile");

    const formData = new FormData();
    
    formData.append("imagefile", ele.files[0]);
    
    async_fetcher("POST", "/image-search", formData).then(resp => {
        
        if (resp.data == false ) {
            return;
        }

        location.href = `/search?q=${resp.data.answer[0].generated_text}`;

    });

}



function metaphorChecker() {
    
    if (location.href.indexOf(`https://metaphor.systems/search?q=`) != 0) {
        return;
    }


	const bs_css_link = document.createElement(`link`);
	bs_css_link.setAttribute(`rel`, `stylesheet`);
	bs_css_link.setAttribute(`href`, `https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css`);
	bs_css_link.setAttribute(`integrity`, `sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD`);
	bs_css_link.setAttribute(`crossorigin`, `anonymous`);
	document.head.appendChild(bs_css_link);

	const bs_icons_link = document.createElement(`link`);
	bs_icons_link.setAttribute(`rel`, `stylesheet`);
	bs_icons_link.setAttribute(`href`, `https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.3/font/bootstrap-icons.css`);
	document.head.appendChild(bs_icons_link);

    const PageWrapper = document.getElementsByClassName("search__PageWrapper-sc-872kyz-2")[0];

    const imgSearcher = document.createElement("div");
    imgSearcher.setAttribute("class", "m-2 p-2");
    imgSearcher.innerHTML = `<label for="formFile" class="form-label">Search an Image</label>
    <input class="form-control" type="file" id="iMetaImageFile">`;
    
    const whereIsInp = PageWrapper.getElementsByTagName("textarea")[0].parentElement;
    whereIsInp.parentElement.appendChild(imgSearcher);

    const iMetaImageFile = document.getElementById("iMetaImageFile");
    iMetaImageFile.addEventListener("change", processImageForm);

    const theParamList = new URLSearchParams(window.location.search);
    const qry = theParamList.get(`q`);

	if (!qry) {
        return;
    }
    
    const iMetaResult = document.createElement("div");
    iMetaResult.setAttribute("class", "border rounded-3 m-3 p-3");
    iMetaResult.innerHTML = `<div class="spinner-grow text-primary" role="status"></div>`;

    async_fetcher("GET", `/new-search?q=${qry}`, null).then(resp => {

        if (resp.data == false) {
            iMetaResult.parentElement.removeChild(iMetaResult);
        }

        let final_str = ``;

        final_str += `<h3 class="fw-bold">${resp.data.keyword}</h3><br/><br/>`;

        for (var i = 0; i < resp.data.images.length; i++) {
            final_str += `<img src="${resp.data.images[i]}" style="max-width:200px" height="auto" class="img-thumbnail rounded-3 m-auto p-1 border d-inline-block" />`
        }

        final_str += '</br></hr/></br>';

        let cnt = resp.data.content.replaceAll('\n', '<br/>')

        final_str += `<p style="white-space: pre-wrap;">${cnt}</p>`;

        iMetaResult.innerHTML = final_str;

    });

    PageWrapper.appendChild(iMetaResult);

}


setTimeout(metaphorChecker, 3000);

