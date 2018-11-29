from pymodm import connect
from pymodm import MongoModel, fields

connect("mongodb://<dbuser>:<dbpassword>@ds121624.mlab.com:21624/bme590final")


class DB_Image_Meta(MongoModel):
    img_url = fields.CharField(primary_key=True)
    user = fields.CharField()
    processing_times = fields.ListField(field=fields.FloatField())
    processing_types = fields.ListField(field=fields.CharField())
