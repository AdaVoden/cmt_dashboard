<%def name="all_weather(weather_features)">
    % for name, feature in weather_features.items():
        ${weather_widget(feature, name, 1)}
    % endfor
</%def>

<%def name="weather_widget(weather_feature, name, size)">
    <article class="weather_feature, block-${size}">
        <h2 class="widget-header"> ${name} </h2>
        <span class="widget-value"> ${weather_feature.current} ${weather_feature.unit} </span>
        <div class="widget-historical">
            <span>
                <b>Min</b>
                <span class="widget-value" > ${weather_feature.minimum} ${weather_feature.unit} </span>
            </span>

            <span>
                <b>Max</b>
                <span class="widget-value" > ${weather_feature.maximum} ${weather_feature.unit} </span>
            </span>

        </div>
    </article>
</%def>

<%def name="telescope_card(telescope)">
    <%self:card id="telescope" title="Telescope">
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

    </%self:card>
</%def>

<%def name="dome_shutter_card(dome)">
    <%self:card id="dome" title="Dome">
        ${status(value=dome.state.name)}
        ${named_data(name="AZ", value=dome.azimuth.dms)}
    </%self:card>
    <%self:card id="shutter" title="Shutter">
        ${status(value=dome.shutterstate.name)}
    </%self:card>
</%def>

<%def name="card(title, id='')">
    <article class="card shadow" id="${id}">
        <section class="title"> <h2>${title}</h2></section>
        <section class="body">
            ${caller.body()}
        </section>
    </article>
</%def>

<%def name="status_block(status)">
    <section class="status-block">
        ${dome_shutter_card(status.dome)}
        ${telescope_card(status.telescope)}
    </section>
</%def>

<%def name="bokeh_plot_divs(targets, size=2)">
    % for target in targets:
        <article class="plot">
            <div id="${target}">
            </div>
        </article>
        <script>
         fetch('/plot/${target}')
             .then(function(response) {return response.json(); })
             .then(function(item) {return Bokeh.embed.embed_item(item);})
        </script>
    % endfor
</%def>

<%def name="time(name, value)">
    <div id="${name}">
        <h3>${name}</h3>
        <time>${value}</time>
    </div>
</%def>

<%def name="status(value)">
    <div class="status">
        <h2>${value}</h2>
    </div>
</%def>

<%def name="named_data(name, value=None)">
    <div class="data">
        <h3>${name}</h2>
        % if value:
            <span class="value" > ${value} </span>
        % endif
    </div>
</%def>
