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
                <section id="status-block">
                    ${widget_card.dome(status.dome)}
                    ${widget_card.telescope(status.telescope)}
                </section>
                <section id="wind_rose">
                    ${widget_card.wind_rose()}
                </sections>
            </section id="right-content">
            <section> <!-- Righthand side, weather graphs -->
                % for name, feature, plot in (zip(weather_features.keys(), weather_features.values(), plots)):
                    ${widget_card.weather(feature, name, 1, plot)}
                % endfor
            </section>
        </main>
    </body>
</html>
