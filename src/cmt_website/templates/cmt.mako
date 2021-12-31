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
<article class="time">
        <b>Date:</b> ${date} <b>UTC:</b> ${utc}
        <b>LST:</b> ${lst}
</article>
<main>
    <section>
        ${features.all_weather(weather_features)}
    </section>
    <section>
        ${features.telescope_widget(telescope, size=2)}
        ${features.dome_widget(dome, size=2)}
    </section>
    <section>
    </section>
</main>
