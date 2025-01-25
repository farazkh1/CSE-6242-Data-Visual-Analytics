""" routes.py - Flask route definitions

Flask requires routes to be defined to know what data to provide for a given
URL. The routes provided are relative to the base hostname of the website, and
must begin with a slash."""
from flaskapp import app
from flask import render_template, request
from wrangling_scripts.Q5 import data_wrangling, username


# The following two lines define two routes for the Flask app, one for just
# '/', which is the default route for a host, and one for '/index', which is
# a common name for the main page of a site.
#
# Both of these routes provide the exact same data - that is, whatever is
# produced by calling `index()` below.
@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def index():
    """Renders the index.html template"""
    filter_class = request.args.get("class", "")
    header, table, dropdown_options = data_wrangling(filter_class)
    # Renders the template (see the index.html template file for details). The
    # additional defines at the end (table, header, username) are the variables
    # handed to Jinja while it is processing the template.
    return render_template(
        'index.html',
        table=table,
        header=header,
        username=username(),
        option_list=dropdown_options,
        filter_class=filter_class,
    )
