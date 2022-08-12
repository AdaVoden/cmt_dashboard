<%namespace name="features", file="features.mako"/>
<%page args="weather_features,
observatory_time,
status,
plots"/>
<!DOCTYPE html>
<html>
    <%include file="head.mako"/>
    <body>
        <header class="shadow">
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
                ${features.status_block(status)}
            </section>
            <section>
                ${features.all_weather(weather_features)}
                ${features.bokeh_plot_divs(plots)}
            </section>
        </main>
    </body>
</html>
