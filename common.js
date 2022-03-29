function post(addr, param, header, callback) {
  var a = new ajaxcallforgeneral(),
    str = [];
  if (header['Content-Type'] == 'application/json') {
    str = JSON.stringify(param);
  } else {
    for (var el in param) str.push(el + '=' + encodeURIComponent(param[el]));
    str = str.join('&');
  }
  a.post(addr, str, header);
  a.ajaxcallback = callback;
}
function get(addr,param,header,callback){
	var a=new ajaxcallforgeneral(),
		str=[];
	for(var el in param){
		str.push(el+"="+param[el]);
	}
	str=str.join("&");
	a.jAjax(addr+"?"+str, header);
	a.ajaxcallback=callback;
};
function ajaxcallforgeneral() {
  this.xmlHttp;
  var j = this;
  var HTTP = {};
  var ADDR;
  var PARAM;
  var HEADER;
  this.jAjax = function (address, header) {
    j.xmlHttp = new XMLHttpRequest();
    j.xmlHttp.onreadystatechange = on_ReadyStateChange;
    j.xmlHttp.onerror = onError;
    j.xmlHttp.open('GET', address, true);
    if (header) {
      Object.keys(header).forEach((key) => {
        var val = header[key];
        j.xmlHttp.setRequestHeader(key, val);
      });
    }
    j.xmlHttp.send(null);
  };
  this.post = function (addr, prm, header) {
    // dateListId1.innerHTML = "";

    j.xmlHttp = new XMLHttpRequest();
    j.xmlHttp.onreadystatechange = on_ReadyStateChange;
    j.xmlHttp.onerror = onError;
    j.xmlHttp.open('POST', addr, true);

    //header :: cors에 결정적
    //j.xmlHttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
    if (header) {
      if (header['Content-Type'])
        Object.keys(header).forEach((key) => {
          var val = header[key];
          j.xmlHttp.setRequestHeader(key, val);
        });
      else
        j.xmlHttp.setRequestHeader(
          'Content-Type',
          'application/x-www-form-urlencoded'
        );
    } else {
      j.xmlHttp.setRequestHeader(
        'Content-Type',
        'application/x-www-form-urlencoded'
      );
    }

    ADDR = addr;
    PARAM = prm;
    HEADER = JSON.stringify(header);

    //console.log(prm);
    j.xmlHttp.send(prm);
  };
  this.file = function (addr, prm) {
    j.xmlHttp = new XMLHttpRequest();
    j.xmlHttp.onreadystatechange = on_ReadyStateChange;
    j.xmlHttp.open('POST', addr, true);
    j.xmlHttp.send(prm);
  };
  function onError() {
    /* dateListId1.innerHTML += "address :: " + ADDR + "\r\n";
		dateListId1.innerHTML += "header :: " + HEADER + "\r\n";
		dateListId1.innerHTML += "param :: " + PARAM + "\r\n"; */
  }
  function on_ReadyStateChange() {
    /* dateListId1.innerHTML += "<div>" + j.xmlHttp.readyState + " :: " + j.xmlHttp.status + "</div>\r\n"; */

    if (j.xmlHttp.readyState == 4) {
      if (j.xmlHttp.status == 200) {
        var data = j.xmlHttp.responseText;
        j.ajaxcallback(data);
      } else {
        // dateListId1.innerHTML += "<div>" + j.xmlHttp.readyState + " :: " + j.xmlHttp.status + "</div>\r\n";
      }
    }
  }
}
Array.prototype.trav = function (fnc) {
  for (var i = 0, lng = this.length; i < lng; i++) {
    var a = fnc(this[i], i);
    if (a) break;
  }
};
String.prototype.gt = function (num) {
  //get tail
  return this.substring(this.length - num, this.length);
};
String.prototype.gh = function (num) {
  //get head
  return this.substring(0, num);
};
String.prototype.ct = function (num) {
  //get tail
  return this.substring(0, this.length - num);
};
String.prototype.ch = function (num) {
  //cut head
  return this.substring(num, this.length);
};
