<%namespace name="widget_card", file="widget_card.mako"/>

<%page args="weather_features,
observatory_time,
status,
plots"/>
<!DOCTYPE html>
<html>
    <%include file="head.mako"/>
    <body>
        <header class="shadow"> <!-- Top of screen header -->
            <section id="title-block">
                <h1>Clark-Milone Telescope</h1>
            </section>
            <section id="time-block"> <!-- For showing relevant and needed times -->
                %for name, time in observatory_time.times.items():
                    ${widget_card.time(name, time)}
                %endfor
            </section>
        </header>
        <main>
            <section id="left-content"> <!-- Lefthand side, status and wind rose -->
                <article id="status-block">
                    ${widget_card.dome(status.dome)}
                    ${widget_card.telescope(status.telescope)}
                </article>
                    ${widget_card.wind_rose()}
            </section>
            <section id="right-content"> <!-- Righthand side, weather graphs -->
                % for name, feature, plot in (zip(weather_features.keys(), weather_features.values(), plots)):
                    ${widget_card.weather(feature, name, plot)}
                % endfor
            </section>
        </main>
    </body>
</html>
