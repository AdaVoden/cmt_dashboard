<%namespace name="features", file="features.mako"/>
<%page args="weather_features,
date,
utc,
lst,
telescope,
dome"/>
<%inherit file="base.mako" />

<%block name="title">
    <title>The 16" Telescope at the RAO</title>
</%block>
<section class="time">
    <div>
        <b>Date:</b> ${date} <b>UT:</b> ${utc}
        <b>LST:</b> ${lst}
    </div>

</section>
<main>
    ${features.all_features(weather_features)}
    ${features.telescope_widget(telescope, size=2)}
    ${features.dome_widget(dome, size=2)}

</main>
