<%page args="sky_brightness" />
<%inherit file="base.mako" />

<%block name="title">
    <title>Sky Quality Meter</title>
</%block>

<script language="JavaScript" type="text/javascript">
 var t = 60;
 var i = t;
 image = "SQM.jpg"; //name of the image
 function Start() {
     UpdateStatus();
     if (i == t) {
         UpdateImage();
         i = 0;
     }
     i = i + 1;
     setTimeout("Start()", 1000);
 }

 function UpdateImage() {
     document.images["plot"].src = image + "?rand=" + Math.random();
 }

 function UpdateStatus() {
     var oRequest = new XMLHttpRequest();
     var sURL = "http://136.159.57.168/AICWebInterface/SQM1.status";

     oRequest.open("GET", sURL, false);
     oRequest.setRequestHeader("User-Agent", navigator.userAgent);
     oRequest.send(null);

     document.getElementById("SQMStatus").innerHTML = oRequest.responseText;
 }
</script>
<h1><font color="red">The Sky Quality Meter at the RAO</font></h1>
<img src="bob.jpg" name="plot" />
<p>
    <font id="SQMStatus">Sky Brightness: ${sky_brightness} square arc second</font>
</p>
