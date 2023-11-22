
function getThisUrl(tourl){
    currentUrl=window.location.href
    listStr=currentUrl.split("/");
    baseUrl=listStr[0]+"//"+listStr[2]+"/";
    if(tourl!==""){
        thisUrl=baseUrl+tourl;
        return thisUrl;
    }else{
        return baseUrl;
    }
}



