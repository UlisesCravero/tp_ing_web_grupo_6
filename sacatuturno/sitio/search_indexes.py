from haystack import indexes
from sitio.models import ServicioPrestado


class ServicioPrestadoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    nombre = indexes.CharField(model_attr='nombre')
    descripcion = indexes.CharField(model_attr='descripcion')
    ciudad = indexes.CharField(model_attr='ciudad')
 
    def get_model(self):
        return ServicioPrestado

    def index_queryset(self, using=None):
        return self.get_model().objects.filter()