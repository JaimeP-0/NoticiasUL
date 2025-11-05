class Noticia:
    def __init__(self, titulo, contenido):
        self.titulo = titulo
        self.contenido = contenido

class NoticiaFactory:
    @staticmethod
    def crear(tipo):
        if tipo == "importante":
            return Noticia("Noticia Importante", "Contenido relevante para todos los estudiantes.")
        elif tipo == "evento":
            return Noticia("Evento Universitario", "Este viernes se celebrará el Día del Estudiante.")
        else:
            return Noticia("Noticia General", "Información general de la universidad.")
