from app import app,db
from .models import Autos
from flask import request


@app.route('/')
def index():
    return {"Msj":"Bienvenido a la Pagina de Autos"}

@app.route('/autos',methods=['POST','GET'])
def handle_autos():
    if request.method=='POST':
        if request.is_json:
            data=request.get_json()
            new_auto=Autos(nombre=data['nombre'],detalle=data['detalle'],imagen=data['imagen'],precio=data['precio'],estado=data['estado'])
            db.session.add(new_auto)
            db.session.commit()

            return {"message": f"Auto {new_auto.nombre} has been created successfully "}
        
        else:
            return {"error":"The request payload is not in Json format"}
        
    elif request.method =='GET':
        autos=Autos.query.filter_by(estado=True).all()#Select * From Autos
        results = [
            {
            "nombre":auto.nombre,
            "detalle":auto.detalle,
            "precio":auto.precio,
            "imagen":auto.imagen,
            "estado":auto.estado
            } for auto in autos]
        
        return {"Count":len(autos),"Autos":results,"message":"success"}
    
@app.route('/auto/<auto_id>',methods=['GET','PUT','DELETE']) 
def handle_auto(auto_id):
    auto=Autos.query.get_or_404(auto_id)
    if request.method == 'GET':
        response = {
            "nombre":auto.nombre,
            "detalle":auto.detalle,
            "precio":auto.precio,
            "imagen":auto.imagen,
            "estado":auto.estado
        }
        return {"message":"success","auto":response}
    
    elif request.method=='PUT':
        data = request.get_json()
        auto.nombre=data["nombre"]
        auto.detalle=data["detalle"]
        auto.precio=data["precio"]
        auto.imagen=data["imagen"]
        auto.estado=data["estado"]

        db.session.add(auto)
        db.session.commit()

        return {"message":f"Auto {auto.nombre} successfully updated"}
    
    elif request.method=='DELETE':
        db.session.delete(auto)
        db.session.commit()

        return {"message":f"Auto {auto.nombre} successfully deleted"}

    
