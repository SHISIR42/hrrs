from app import create_app, db



app = create_app()

with app.app_context():
    print("Registered endpoints:")
    for rule in app.url_map.iter_rules():
        print(rule.endpoint, rule.rule)
    db.create_all()

if __name__ == '__main__':
    app.run(port=5000, debug=True)