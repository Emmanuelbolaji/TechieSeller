from market import app


if __name__ == '__main__':
    """
    Entry point for running the Flask application.
    Ensures that the app only runs if the script is executed directly, 
    not when imported as a module.
    """
    app.run(debug=False)
