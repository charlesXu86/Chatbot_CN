//m-3-id-1 上下滚动
(function(){
	var marquee = document.getElementById('m-3-id-1');
	var offset=0;
	var scrollheight =marquee.offsetHeight;
	var firstNode = marquee.children[0].cloneNode(true);
	marquee.appendChild(firstNode);
	setInterval(function(){
		if(offset == scrollheight){
			offset = 0;
		}
		marquee.style.marginTop = "-"+offset+"px";
		offset += 2;
	},20);
})();

//图片无缝滚动
var speed=10; 
var tab=document.getElementById("m-5-id-1"); 
var tab1=document.getElementById("m-5-id-2"); 
var tab2=document.getElementById("m-5-id-3"); 
tab2.innerHTML=tab1.innerHTML; 
function Marquee(){ 
if(tab2.offsetWidth-tab.scrollLeft<=0) 
tab.scrollLeft-=tab1.offsetWidth 
else{ 
tab.scrollLeft++; 
} 
} 
var MyMar=setInterval(Marquee,speed); 
tab.onmouseover=function() {clearInterval(MyMar)}; 
tab.onmouseout=function() {MyMar=setInterval(Marquee,speed)}; 


//字母滚动
var screen1 = document.getElementById("screen1");
var screen1_1 = document.getElementById("screen1_1");
var screen1_2 = document.getElementById("screen1_2");
var speed=4;    //滚动速度值，值越大速度越慢
var nnn=200/screen1_1.offsetHeight;
for(i=0;i<nnn;i++){screen1_1.innerHTML+="<br />"+ screen1_1.innerHTML}
screen1_2.innerHTML = screen1_1.innerHTML    //克隆screen1_2为screen1_1
function Marquee1(){
    if(screen1_2.offsetTop-screen1.scrollTop<=0)    //当滚动至screen1_1与screen1_2交界时
        screen1.scrollTop-=screen1_1.offsetHeight    //screen1跳到最顶端
    else{
        screen1.scrollTop++     //如果是横向的 将 所有的 height top 改成 width left
    }
}
var MyMar = setInterval(Marquee1,speed);        //设置定时器
screen1.onmouseover = function(){clearInterval(MyMar)}    //鼠标经过时清除定时器达到滚动停止的目的
screen1.onmouseout = function(){MyMar = setInterval(Marquee1,speed)}    //鼠标移开时重设定时器


//局部刷新  
var XMLHttpReq; 
//创建XMLHttpRequest对象 
function createXMLHttpRequest() { 
if(window.XMLHttpRequest) { //Mozilla 浏览器 
XMLHttpReq = new XMLHttpRequest(); 
} 
else if (window.ActiveXObject) { // IE浏览器 
try { 
XMLHttpReq = new ActiveXObject("Msxml2.XMLHTTP"); 
} catch (e) { 
try { 
XMLHttpReq = new ActiveXObject("Microsoft.XMLHTTP"); 
} catch (e) {} 
} 
} 
} 
//发送请求函数 
function sendRequest() { 
createXMLHttpRequest(); 
var url = "data1.php?_dc="+new Date().getTime();
XMLHttpReq.open("GET", url, true); 
XMLHttpReq.onreadystatechange = processResponse;//指定响应函数 
XMLHttpReq.send(null); // 发送请求 
} 
// 处理返回信息函数 
function processResponse() { 
if (XMLHttpReq.readyState == 4) { // 判断对象状态 
if (XMLHttpReq.status == 200) { // 信息已经成功返回，开始处理信息 
DisplayHot(); 
setTimeout("sendRequest()",2000); //设置自动刷新时间，这里是毫秒，即2秒//RemoveRow(); 
} else { //页面不正常 
//window.alert("您所请求的页面有异常。"); 
} 
} 
} 
function DisplayHot()
{
var theDate = XMLHttpReq.responseText ;//如果出现编码问题,可以在服务端escape一下,然后在这里使用unescape( responseText )

gxsj1.innerHTML = theDate ;
}







//获取当前时间带跳动
function showLocale(objD){
	var str,colorhead,colorfoot;
	var yy = objD.getYear();
	if(yy<1900) yy = yy+1900;
	var MM = objD.getMonth()+1;
	if(MM<10) MM = '0' + MM;
	var dd = objD.getDate();
	if(dd<10) dd = '0' + dd;
	var hh = objD.getHours();
	if(hh<10) hh = '0' + hh;
	var mm = objD.getMinutes();
	if(mm<10) mm = '0' + mm;
	var ss = objD.getSeconds();
	if(ss<10) ss = '0' + ss;
	var ww = objD.getDay();
	if  ( ww==0 )  colorhead="";
	//if  ( ww > 0 && ww < 6 )  colorhead="";
	//if  ( ww==6 )  colorhead="";
	//if  (ww==0)  ww="星期日";
	//if  (ww==1)  ww="星期一";
	//if  (ww==2)  ww="星期二";
	//if  (ww==3)  ww="星期三";
	//if  (ww==4)  ww="星期四";
	//if  (ww==5)  ww="星期五";
	//if  (ww==6)  ww="星期六";
	colorfoot=""
	str = colorhead + yy + "-" + MM + "-" + dd + " " + hh + ":" + mm + ":" + ss + "  " + colorfoot;
	return(str);
}

function tick(){
	var today;
	today = new Date();
	document.getElementById("localtime").innerHTML = showLocale(today);
	window.setTimeout("tick()", 1000);
}

tick();




//自动增加数字
window.onload = function() {
    // 数字到达 100 后还原为 1
    var max = 11000000,
        o = document.getElementById('zdzj1');
        var chrome = /chrome/i.test(navigator.userAgent);
                         
    // 获取保存的数据
    if(chrome) {
        data_num = sessionStorage.getItem("num") || "";
    }
    else {
        data_num = document.cookie.replace(
        /(?:(?:^|.*;\s*)num\s*\=\s*((?:[^;](?!;))*[^;]?).*)|.*/,
        "$1");
    }
    var num_now = parseInt(data_num) || 0;
                         
    o.innerHTML = num_now + 1;
                         
    // 每 0.1 秒更新一次数字，并保存数据
    setInterval(function() {
        num_now = num_now >= max ? 2685 : num_now + 1;
        o.innerHTML = num_now;
        if(chrome) {
            sessionStorage.setItem("num", num_now);
        }
        else {
            document.cookie = "num=" + num_now + ";path=/;";
        }
    }, 100);
};
