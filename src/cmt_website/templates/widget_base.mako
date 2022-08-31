<%def name="card(title, id='')">
    <!-- Base card function, creates a two section card, with a header and a body then adds
         the content that it was called with. Used as a tag. -->
    <article class="card shadow" id="${id}">
        <section class="title"> <h2>${title}</h2></section>
        <section class="content">
            ${caller.body()}
        </section>
    </article>
</%def>

<%def name="bokeh_plot(target)">
    <!-- Takes a bokeh plot target name, pulls javascript from it and then displays it on screen -->
    <div id="${target}">
    </div>

    <script>
     fetch('/plot/${target}')
         .then(function(response) {return response.json(); })
         .then(function(item) {return Bokeh.embed.embed_item(item);})
    </script>
</%def>
