<%namespace name="base", file="widget_base.mako"/>

<%def name="weather(weather_feature, name, size, plot)">
    <%base:card title="${name}">
        <section class="weather_status">
            <h3>Current</h3>
            <%self:status value="${weather_feature.current}" unit="${weather_feature.unit}"></%self:status>
            <h3>Today</h3>
            ${named_data(name="Max", value=weather_feature.maximum, unit=weather_feature.unit)}
            ${named_data(name="Min", value=weather_feature.minimum, unit=weather_feature.unit)}
        </section>
        <section class="weather_plot">
            <%base:bokeh_plot target="${plot}" ></%base:bokeh_plot>
        </section>
    </%base:card>
</%def>

<%def name="telescope(telescope)">
    <%base:card id="telescope" title="Telescope">
        ${status(value=telescope.state.name)}
        <div id="horizontal">
            % for coord, value in {"RA" : telescope.ra.hms, "DEC" : telescope.dec.dms, "HA": telescope.hour_angle.hms}.items():
                ${named_data(name=coord, value=value)}
            % endfor
        </div>
        <div id="vertical">
            % for coord, value in {"ALT": telescope.altitude.dms, "AZ": telescope.azimuth.dms}.items():
                ${named_data(name=coord, value=value)}
            % endfor
        </div>
    </%base:card>
</%def>

<%def name="dome(dome)">
    <%base:card id="dome" title="Dome">
        ${status(value=dome.state.name)}
        ${named_data(name="AZ", value=dome.azimuth.dms)}
    </%base:card>
    <%base:card id="shutter" title="Shutter">
        ${status(value=dome.shutterstate.name)}
    </%base:card>
</%def>

<%def name="wind_rose()">
    <%base:card id="wind_rose_container" title="Wind Direction and Speed">
        ${base.bokeh_plot("wind_rose")}
    </%base:card>

</%def>

<%def name="time(name, value)">
    <span id="${name}">
        <h3>${name}</h3>
        <time>${value}</time>
    </span>
</%def>

<%def name="status(value, unit=None)">
    <span class="status">
        % if unit:
            <h2>${value} ${unit}</h2>
        % else:
            <h2>${value} </h2>
        % endif
    </span>
</%def>

<%def name="named_data(name, value=None, unit=None)">
    <span class="data">
        <h3>${name}</h3>
        % if value and unit:
            <h4> ${value} ${unit} </h4>
        % elif value:
            <h4> ${value} </h4>
        % endif
    </span>
</%def>
