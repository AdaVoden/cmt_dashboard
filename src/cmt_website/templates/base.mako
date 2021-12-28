<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width,initial-scale=1" />
        <%block name="title"/>
    </head>
    <body>

        <center>
            <br />
            <img src="static/CMT_banner.jpg" />
        </center>

            <center>
                <img src="static/gal.gif" />
            </center>
            <p>
                <a href="cmt">
                    <img src="static/16inchdome_icon.jpg" /><br />
                    <i> <font size="-1">Follow the Telescope</font></i>
                </a>
            </p>
            <p>
                <a href="weather">
                    <img src="static/1620_icon.jpg" />
                    <br />
                    <i>
                        <font size="-1"> Weather </font>
                    </i>
                </a>
            </p>
            <p>
                <a href="current_image">
                    <img src="static/M42_icon.jpg" />
                    <br />
                    <i>
                        <font size="-1">Most Recent Color Image</font>
                    </i>
                </a>

            </p>
            <p>
                <a href="sqm">
                    <img src="static/raincld.gif" />
                    <br />
                    <i>
                        <font size="-1">Sky Quality Meter</font>
                    </i>
                </a>

            </p>
            <p>
                <a
                    href="http://www.google.com/calendar/embed?src=ahr2blr3de7fb6qvbji11ubbvg%40group.calendar.google.com "
                ><img src="static/BMoon001LW_thumbnailnew.jpg" /><br />
                    <i>
                        <font size="-1">Schedule</font>
                    </i>
                </a>
            </p>

            ${self.body(**pageargs)}
    </body>
</html>
