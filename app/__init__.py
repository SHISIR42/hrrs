from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os

db = SQLAlchemy()

def create_app():
    load_dotenv()

    app = Flask(__name__)
    from config import Config
    app.config.from_object(Config)
    from app.routes.compliance_api import compliance_api
    app.register_blueprint(compliance_api)

    CORS(app)
    db.init_app(app)


    # Register Blueprints

    from app.routes.employee_routes import employee_bp
    app.register_blueprint(employee_bp, url_prefix="/employees")
    from app.routes.department_routes import department_bp
    app.register_blueprint(department_bp, url_prefix="/departments")
    from app.routes.dbs_api import dbs_api
    from app.routes.dbs_web import web_dbs_bp
    from app.routes.home_office_api import home_office_api
    from app.routes.bank_api import bank_api
    from app.routes.credit_agency_api import credit_agency_api
    from app.routes.bank_web import bank_web_bp
    app.register_blueprint(dbs_api)
    app.register_blueprint(web_dbs_bp)
    app.register_blueprint(home_office_api)
    app.register_blueprint(bank_api)
    app.register_blueprint(credit_agency_api)
    app.register_blueprint(bank_web_bp)

    # Dashboard route
    from flask import render_template

    @app.route('/dashboard')
    def dashboard():
        return render_template('loding.html')

    @app.route('/dashboard/main')
    def dashboard_main():
        return render_template('dashboard.html')

    return app
   
