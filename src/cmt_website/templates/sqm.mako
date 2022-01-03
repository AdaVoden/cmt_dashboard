<%page args="sky_brightness" />
<%inherit file="base.mako" />

<%block name="title">
    <title>Sky Quality Meter</title>
</%block>
<h1><font color="red">The Sky Quality Meter at the RAO</font></h1>
<img src="static/sqm.jpg" name="plot" />
<p>
    <font id="SQMStatus">Sky Brightness: ${sky_brightness} square arc second</font>
</p>
