<%namespace name="features", file="features.mako"/>
<%page args="weather_features,
date,
utc,
lst,
telescope,
dome,
plots"/>
<!DOCTYPE html>
<html>
    <%include file="head.mako"/>
    <body>
        <header>
            <h1>Clark-Milone Telescope</h1>
            <article id="time">
                <b>Date:</b> ${date} <b>UTC:</b> ${utc}
                <b>LST:</b> ${lst}
            </article>
        </header>
        <main>
            <section>
                ${features.all_weather(weather_features)}
            </section>
            <section>
                ${features.telescope_widget(telescope, size=2)}
                ${features.dome_widget(dome, size=2)}
            </section>
            <section id="plots">
                ${features.bokeh_plot_divs(plots)}
            </section>
        </main>
    </body>
</html>
