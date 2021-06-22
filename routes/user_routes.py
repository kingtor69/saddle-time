from app import CURR_USER, CURR_ROUTE, CURR_CHECKPOINT_LIST, GUEST, loginSession, logoutSession

@app.route('/users/signup', methods=["GET", "POST"])
def signup_new_user():
    """Sign up new users. Enter into database"""

@app.route('/users/<user_id>/preferences', methods=["GET", "POST"])
def edit_user_preferences():
    """Edit user preferences such as default route type, metric or imperial units, &c. Will also edit other aspects of a user profile such as bio, favorite bike, &c."""

@app.route('/users/<user_id>/delete', methods=["POST"])
def delete_user():
    """Permanently deletes a user from the database."""

@app.route('/login')
def login():
    """logs a user in"""

@app.route('/logout')
def logout():
    """logs a user out"""

