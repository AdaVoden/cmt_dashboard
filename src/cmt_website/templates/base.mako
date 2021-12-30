<!DOCTYPE html>
<html>
    <%include file="head.mako"/>
  <body>

      <img src="static/CMT_banner.jpg" />
      <img src="static/gal.gif" />
      <%include file="navigation.mako"/>

      ${self.body(**pageargs)}
  </body>
</html>
