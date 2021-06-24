@app.route('/routes/new', methods=["GET", "POST"])
def create_new_route():
    """Create a new route, including adding and re-arranging checkpoints."""

@app.route('/route')
def display_route():
    """Show route on map and with step-by-step directions, and weather information for the route. This uses the GET method to store all route information in the query string."""

@app.route('/route/save')
def save_route():
    """Save a route into the database. Page can only be accessed by registered and logged-in users."""

@app.route('/routes/<id>')
def display_saved_route():
    """Build the query string from a saved route and redirect to '/route'. This can be accessed by any user, or by a guest who is not logged in."""

@app.route('/routes/<id>/edit')
def edit_saved_route():
    """The user who created a route can edit their route here. Any other user (or guest) can create a new route using this one as a strating point."""

