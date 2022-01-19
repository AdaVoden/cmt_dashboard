<%namespace name="features", file="features.mako"/>
<%page args="weather_features,
observatory_time,
telescope,
dome,
plots"/>
<!DOCTYPE html>
<html>
    <%include file="head.mako"/>
    <body>
        <header class="card">
            <section id="title-block">
                <h1>Clark-Milone Telescope</h1>
            </section>
            <section id="time-block">
                    %for name, time in observatory_time.times.items():
                        ${features.time(name, time)}
                    %endfor
            </section>
        </header>
        <main>
            <section>
                ${features.telescope_widget(telescope, size=2)}
                ${features.dome_widget(dome, size=2)}
            </section>
            <section>
                ${features.all_weather(weather_features)}
                ${features.bokeh_plot_divs(plots)}
            </section>
        </main>
    </body>
</html>
