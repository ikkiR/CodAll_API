from flask import Blueprint

def regitrar_rotas(app):    
    from .usuarios import usuarios_bp
    app.register_blueprint(usuarios_bp)
