<%page args="temperature,
humidity,
wind_speed,
date,
utc,
lst,
telescope_altitude,
telescope_azimuth,
telescope_ra,
telescope_ha,
telescope_dec,
dome_azimuth,
dome_shutter,
camera_filter,
camera_focus,
camera_temperature,
telescope_status,
dome_status"/>
<%inherit file="base.mako" />

<%block name="title">
    <title>The 16" Telescope at the RAO</title>
</%block>
<table width="900" border="0">
    <tr valign="top">
        <td style="height: 200px; width: 400px">
            <div style="text-align: center">
                <h1><font color="green">The 16" Telescope at the RAO</font></h1>
            </div>
            <div style="text-align: left">
                <b>Date:</b> ${date} <b>UT:</b> ${utc}
                <b>LST:</b> ${lst}<br />
                * Note: If the time is not updating then the telescope is not
                running.
                <h2><font color="green">Weather</font></h2>
                <b>Temperature:</b> ${temperature} C <b>Humidity:</b> ${humidity}% <b>Wind Speed</b> ${wind_speed}
                km/h
                <h2><font color="green">Telescope</font> <i>${telescope_status}</i></h2>
            </div>
            <table
                style="width: 50%; text-align: left"
                border="0"
                cellpadding="0"
                cellspacing="0"
            >
                <tbody>
                    <tr>
                        <td />
                        <td style="vertical-align: center; text-align: center">
                            <a href="telimage.html" target="new"
                            ><img src="../telimage.jpg"
                             /></a>
                        </td>
                    </tr>
                </tbody>
            </table>
            <br /><br />
        </td>
        <td style="height: 200px; width: 400px; text-align: top">
            <br />
            <br />
            <br />
            <br />
            <br />
            <br />
            <br />
            <br />
            <br />
            <br />
            <br />
            <table
                style="width: 50%; text-align: left"
                border="1"
                cellpadding="2"
                cellspacing="2"
            >
                <tbody>
                    <tr>
                        <td></td>
                        <td style="vertical-align: center; text-align: center">
                            <b>Altitude</b>
                        </td>
                        <td></td>
                        <td style="vertical-align: center; text-align: center">
                            <b>Azimuth</b>
                        </td>
                        <td></td>
                        <td style="vertical-align: center; text-align: center">
                            <b>RA</b>
                        </td>
                        <td></td>
                        <td style="vertical-align: center; text-align: center">
                            <b>HA</b>
                        </td>
                        <td></td>
                        <td style="vertical-align: center; text-align: center">
                            <b>DEC</b>
                        </td>
                    </tr>
                    <tr>
                        <td></td>
                        <td style="vertical-align: center; text-align: center">
                            ${telescope_altitude}
                        </td>
                        <td></td>
                        <td style="vertical-align: center; text-align: center">
                            ${telescope_azimuth}
                        </td>
                        <td></td>
                        <td style="vertical-align: center; text-align: center">
                            ${telescope_ra}
                        </td>
                        <td></td>
                        <td style="vertical-align: center; text-align: center">
                            ${telescope_ha}
                        </td>
                        <td></td>
                        <td style="vertical-align: center; text-align: center">
                            ${telescope_dec}
                        </td>
                    </tr>
                </tbody>
            </table>
            <h2><font color="green">Dome</font> <i>${dome_status}</i></h2>
            <table
                style="width: 50%; text-align: left"
                border="1"
                cellpadding="2"
                cellspacing="2"
            >
                <tbody>
                    <tr>
                        <td></td>
                        <td style="vertical-align: center; text-align: center">
                            <b>Azimuth</b>
                        </td>
                        <td></td>
                        <td style="vertical-align: center; text-align: center">
                            <b>Shutter</b>
                        </td>
                    </tr>
                    <tr>
                        <td></td>
                        <td style="vertical-align: center; text-align: center">
                            ${dome_azimuth}
                        </td>
                        <td></td>
                        <td style="vertical-align: center; text-align: center">${dome_shutter}</td>
                    </tr>
                </tbody>
            </table>
            <h2><font color="green">Camera</font></h2>
            <table
                style="width: 50%; text-align: left"
                border="1"
                cellpadding="2"
                cellspacing="2"
            >
                <tbody>
                    <tr>
                        <td></td>
                        <td style="vertical-align: center; text-align: center">
                            <b>Filter</b>
                        </td>
                        <td></td>
                        <td style="vertical-align: center; text-align: center">
                            <b>Focus</b>
                        </td>
                        <td></td>
                        <td style="vertical-align: center; text-align: center">
                            <b>Temperature</b>
                        </td>
                    </tr>
                    <tr>
                        <td></td>
                        <td style="vertical-align: center; text-align: center">
                            ${camera_filter}
                        </td>
                        <td></td>
                        <td style="vertical-align: center; text-align: center">${camera_focus}</td>
                        <td></td>
                        <td style="vertical-align: center; text-align: center">
                            ${camera_temperature} C
                        </td>
                    </tr>
                </tbody>
            </table>
            <br /><br />
        </td>
    </tr>
</table>
