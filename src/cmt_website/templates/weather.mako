<%namespace name="features" file="features.mako"/>
<%page args="weather_data"/>
<%inherit file="base.mako" />
<%block name="title">
    <title>RAO Weather</title>
</%block>
<div style="text-align: center">
    <h1><font color="green">RAO Weather</font></h1>
</div>
<div style="text-align: left">
    <table
        style="width: 50%; text-align: left"
        border="0"
        cellpadding="2"
        cellspacing="2"
    >
        <tbody>
            <tr>
                <td />
                <td style="vertical-align: bottom; text-align: left">
                    <h1>Current Conditions</h1>
                </td>
                <td />
                <td style="vertical-align: top; text-align: center">
                    <a href="http://136.159.57.152" target="new">
                        <img
                            width="150"
                            height="100"
                            src="http://136.159.57.152/netcam.jpg"
                        />
                    </a>
                </td>
            </tr>
        </tbody>
    </table>
</div>
${features.all_features(weather_data.features)}
<a href="http://cleardarksky.com/c/RothneyALkey.html" target="new">
    <img src="http://cleardarksky.com/csk/getcsk.php?id=RothneyAL" />
</a>
<br /><br />
<table
    style="width: 50%; text-align: left"
    border="0"
    cellpadding="2"
    cellspacing="2"
>
    <tbody>
        <tr>
            <td><h1>Weather Forecast</h1></td>
            <td>
                <a
                    href="http://weatheroffice.ec.gc.ca/city/pages/ab-52_metric_e.html"
                    target="new"
                >Enviroment Canada</a
                                  >
            </td>
            <td>
                <a
                    href="http://theweathernetwork.com/weather/cities/can/pages/CAAB0049.html"
                    target="new"
                >The Weather Network</a
                                    >
            </td>
        </tr>
    </tbody>
</table>
<table
    style="width: 50%; text-align: left"
    border="0"
    cellpadding="2"
    cellspacing="2"
>
    <tbody>
        <tr>
            <td><h1>Weather Satelite Images</h1></td>
            <td>
                <a
                    href="http://weatheroffice.ec.gc.ca/satellite/animateweb_e.html?imagetype=satellite&imagename=goes_wcan_1070_m_..................jpg&nbimages=1&clf=1"
                    target="new"
                >IR</a
                   >
            </td>
            <td>
                <a
                    href="http://weatheroffice.ec.gc.ca/satellite/animateweb_e.html?imagetype=satellite&imagename=goes_wcan_visible_m_..................jpg&nbimages=1&clf=1"
                    target="new"
                >Visible</a
                        >
            </td>
            <td>
                <a
                    href="http://weatheroffice.ec.gc.ca/satellite/animateweb_e.html?imagetype=satellite&imagename=goes_wcan_vvi_m_..................jpg&nbimages=1&clf=1"
                    target="new"
                >IR + Visible</a
                             >
            </td>
        </tr>
    </tbody>
</table>
<h1>Weather Data Plots</h1>
<div style="text-align: left">
    <h3>Temperature</h3>
    <table
        style="width: 100%; text-align: left"
        border="1"
        cellpadding="2"
        cellspacing="2"
    >
        <tbody>
            <tr>
                <td style="vertical-align: top; text-align: center">
                    <a href="onedaytemp.jpg" target="new"
                    ><img
                         alt="24 Hour temperature"
                         src="onedaytemp_thumb.jpg"
                         style="border: 2px solid; width: 120px; height: 93px" /></a
                                                                                 ><br />
                    24 Hour Period<br />
                </td>
                <td style="vertical-align: top; text-align: center">
                    <a href="sevendaytemp.jpg" target="new"
                    ><img
                         alt=""
                         src="sevendaytemp_thumb.jpg"
                         style="border: 2px solid; width: 120px; height: 93px" /></a
                                                                                 ><br />
                    7 Day Period<br />
                </td>
                <td style="vertical-align: top; text-align: center">
                    <a href="thirtydaytemp.jpg" target="new"
                    ><img
                         alt=""
                         src="thirtydaytemp_thumb.jpg"
                         style="border: 2px solid; width: 120px; height: 93px" /></a
                                                                                 ><br />
                    30 Day Period<br />
                </td>
            </tr>
        </tbody>
    </table>
    <br />
    <h3>Pressure</h3>
    <br />
    <table
        style="width: 100%; text-align: left"
        border="1"
        cellpadding="2"
        cellspacing="2"
    >
        <tbody>
            <tr>
                <td style="vertical-align: top; text-align: center">
                    <span style="text-decoration: underline">
                        <a href="onedaypressure.jpg" target="new">
                            <img
                                alt=""
                                src="onedaypressure_thumb.jpg"
                                style="border: 2px solid; width: 120px; height: 93px"
                            />
                        </a>
                    </span>
                    <br />
                    24 Hour Period
                    <br />
                </td>
                <td style="vertical-align: top; text-align: center">
                    <a href="sevendaypressure.jpg" target="new"
                    ><img
                         alt=""
                         src="sevendaypressure_thumb.jpg"
                         style="border: 2px solid; width: 120px; height: 93px" /></a
                                                                                 ><br />
                    7 Day Period<br />
                </td>
                <td style="vertical-align: top; text-align: center">
                    <a href="thirtydaypressure.jpg" target="new"
                    ><img
                         alt=""
                         src="thirtydaypressure_thumb.jpg"
                         style="border: 2px solid; width: 120px; height: 93px" /></a
                                                                                 ><br />
                    30 Day Period<br />
                </td>
            </tr>
        </tbody>
    </table>
    <br />
    <h3>Relative Humidity</h3>
    <br />
    <table
        style="width: 100%; text-align: left"
        border="1"
        cellpadding="2"
        cellspacing="2"
    >
        <tbody>
            <tr>
                <td style="vertical-align: top; text-align: center">
                    <a href="onedayhumidity.jpg" target="new"
                    ><img
                         alt=""
                         src="onedayhumidity_thumb.jpg"
                         style="border: 2px solid; width: 120px; height: 93px" /></a
                                                                                 ><br />
                    24 Hour Period<br />
                </td>
                <td style="vertical-align: top; text-align: center">
                    <a href="sevendayhumidity.jpg" target="new"
                    ><img
                         alt=""
                         src="sevendayhumidity_thumb.jpg"
                         style="border: 2px solid; width: 120px; height: 93px" /></a
                                                                                 ><br />
                    7 Day Period<br />
                </td>
                <td style="vertical-align: top; text-align: center">
                    <a href="thirtydayhumidity.jpg" target="new"
                    ><img
                         alt=""
                         src="thirtydayhumidity_thumb.jpg"
                         style="border: 2px solid; width: 120px; height: 93px" /></a
                                                                                 ><br />
                    30 Day Period<br />
                </td>
            </tr>
        </tbody>
    </table>
    <br />
    <h3>Wind Speed</h3>
    <br />
    <table
        style="width: 100%; text-align: left"
        border="1"
        cellpadding="2"
        cellspacing="2"
    >
        <tbody>
            <tr>
                <td style="vertical-align: top; text-align: center">
                    <a href="onedaywspeed.jpg" target="new"
                    ><img
                         alt=""
                         src="onedaywspeed_thumb.jpg"
                         style="border: 2px solid; width: 120px; height: 93px" /></a
                                                                                 ><br />
                    24 Hour Period<br />
                </td>
                <td style="vertical-align: top; text-align: center">
                    <a href="sevendaywspeed.jpg" target="new"
                    ><img
                         alt=""
                         src="sevendaywspeed_thumb.jpg"
                         style="border: 2px solid; width: 120px; height: 93px" /></a
                                                                                 ><br />
                    7 Day Period<br />
                </td>
                <td style="vertical-align: top; text-align: center">
                    <a href="thirtydaywspeed.jpg" target="new"
                    ><img
                         alt=""
                         src="thirtydaywspeed_thumb.jpg"
                         style="border: 2px solid; width: 120px; height: 93px" /></a
                                                                                 ><br />
                    30 Day Period<br />
                </td>
            </tr>
        </tbody>
    </table>
    <br />
    <h3>Wind Direction</h3>
    <br />
    <table
        style="width: 100%; text-align: left"
        border="1"
        cellpadding="2"
        cellspacing="2"
    >
        <tbody>
            <tr>
                <td style="vertical-align: top; text-align: center">
                    <a href="onedaywdirection.jpg" target="new"
                    ><img
                         alt=""
                         src="onedaywdirection_thumb.jpg"
                         style="border: 2px solid; width: 120px; height: 93px" /></a
                                                                                 ><br />
                    24 Hour Period<br />
                </td>
                <td style="vertical-align: top; text-align: center">
                    <a href="sevendaywdirection.jpg" target="new"
                    ><img
                         alt=""
                         src="sevendaywdirection_thumb.jpg"
                         style="border: 2px solid; width: 120px; height: 93px" /></a
                                                                                 ><br />
                    7 Day Period<br />
                </td>
                <td style="vertical-align: top; text-align: center">
                    <a href="thirtydaywdirection.jpg" target="new"
                    ><img
                         alt=""
                         src="thirtydaywdirection_thumb.jpg"
                         style="border: 2px solid; width: 120px; height: 93px" /></a
                                                                                 ><br />
                    30 Day Period<br />
                </td>
            </tr>
        </tbody>
    </table>
    <br />
</div>
