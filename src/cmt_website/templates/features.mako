<%def name="all_features(weather_features)">
    % for name, feature in weather_features.items():
        ${feature_widget(feature, name, 1)}
    % endfor
</%def>

<%def name="feature_widget(weather_feature, name, size)">
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

<%def name="telescope_widget(telescope, size, name='Clark-Milone Telescope')">
    <article class="telescope, block-${size}">
        <h2 class="widget-header"> ${name} </h2>
        <span class="widget-status"> <b>Status</b> ${telescope.state.name} </span>
        % for coord, value in {"RA" : telescope.ra.hms, "DEC" : telescope.dec.hms, "HA": telescope.hour_angle.hms, "Altitude": telescope.altitude.dms, "Azimuth": telescope.azimuth.dms}.items():
            <span class="widget-value" > <b>${coord}</b> ${value} </span>
        % endfor
    </article>
</%def>

<%def name="dome_widget(dome, size)">
    <article class="dome, block-${size}">
        <h2 class="widget-header" > Dome </h2>
        <span class="widget_status" > <b>Status</b> ${dome.state.name} </span>
        <span class="widget-value"> <b>Position</b> ${dome.azimuth.dms}</span>
    </article>
    <article class="shutter, block-${size}">
        <h2 class="widget-header" > Shutter </h2>
        <span class="widget_status" > <b>Status</b> ${dome.shutterstate.name} </span>
    </article>
</%def>