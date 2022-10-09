from aplicacion.config.mysqlconnection import connectToMySQL #siempre importar la conección con la base de datos
from flask import flash
from aplicacion import app

class Receta:

    base_datos="esquema_recetas_primer_intento"

    def __init__(self, data):
        self.id=data['id']
        self.titulo = data['titulo']
        self.descripcion = data['descripcion']
        self.instrucciones = data['instrucciones']
        self.fecha = data['fecha']
        self.duracion = data['duracion']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.usuario_id = data['usuario_id']

    #insertar una receta:
    @classmethod
    def crear_receta(cls,data):
        consulta= "INSERT INTO recetas (titulo, descripcion, instrucciones, fecha, duracion, created_at, updated_at, usuario_id) VALUES (%(titulo)s, %(descripcion)s, %(instrucciones)s, %(fecha)s, %(duracion)s, NOW(), NOW(), %(usuario_id)s);" 
        resultado = connectToMySQL(cls.base_datos).query_db(consulta,data)
        return resultado
    
    #leer UNA SOLA receta:
    @classmethod
    def leer_receta(cls, data):
        # ACA LO HICE DISTINTO PORQUE EN LA DEMOSTRACION NO PUSIERON QUIEN HIZO LA RECETA
        consulta= """SELECT recetas.id, recetas.titulo, recetas.descripcion, recetas.instrucciones, recetas.fecha, recetas.duracion, recetas.created_at, recetas.updated_at, concat(usuarios.nombre," ", usuarios.apellido ) AS usuario_id  FROM recetas JOIN usuarios ON recetas.usuario_id = usuarios.id WHERE recetas.id = %(id)s;"""
        resultado= connectToMySQL (cls.base_datos).query_db(consulta,data)
        return cls(resultado[0])

    #EDITAR UNA RECETA
    @classmethod
    def editar_receta(cls, data):
        consulta="""UPDATE recetas SET titulo = %(titulo)s, descripcion = %(descripcion)s, instrucciones = %(instrucciones)s, fecha = %(fecha)s, duracion = %(duracion)s, updated_at = NOW() WHERE id = %(id)s; """
        resultado= connectToMySQL (cls.base_datos).query_db(consulta,data)
        return resultado
    
    #MOSTRAR TODAS LAS RECETAS CON SUS USUARIOS
    @classmethod
    def todas_las_recetas(cls):
        consulta = "SELECT * FROM recetas JOIN usuarios ON recetas.usuario_id = usuarios.id"
        resultado= connectToMySQL (cls.base_datos).query_db(consulta)
        # print(resultado, "ESTO ES LO QUE TENGO QUE LEER")
        return resultado
    
    #Eliminar receta
    @classmethod
    def eliminar_receta(cls,data):
        consulta = "DELETE FROM recetas WHERE id=%(id)s;"
        resultado= connectToMySQL (cls.base_datos).query_db(consulta,data)
        return resultado

    @staticmethod
    def validacion_receta(formulario_receta):
        is_valid = True # asumimos que esto es true
        if len(formulario_receta['titulo']) < 3:
            flash("El título debe contar con al menos 3 caracteres")
            is_valid = False
        if len(formulario_receta['descripcion']) < 3:
            flash("La descripcion debe contar con al menos 3 caracteres")
            is_valid = False
        if len(formulario_receta['instrucciones']) < 3:
            flash("Las instrucciones deben contar con al menos 3 caracteres")
            is_valid = False
        if len(formulario_receta['fecha']) < 10:
            flash("Selecciona una fecha")
            is_valid = False
        #ESTE INPUT DEL FORMULARIO NO LO PUDE VALIDAR
        # if not  formulario_receta['duracion'] == "1" or formulario_receta['duracion'] == "0":
        #     flash("Selecciona una duración")
        #     is_valid = False
        return is_valid