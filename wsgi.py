from application import create_app

# Gets an initialized application
app = create_app()


if __name__ == '__main__':
    # Run on port 5000 by default
    app.run('0.0.0.0')


