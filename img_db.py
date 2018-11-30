from pymodm import connect
from pymodm import MongoModel, fields

connect("mongodb://bme_user:GODUKE10@ds121624.mlab.com:21624/bme590final")


class DB_Image_Meta(MongoModel):
    """MongoDB database object for image metadata

    Attributes:
        img_file_path (str): Unique string containing file path
        user (str): Username of user who uploaded image
        processing_times (list): List of floats containing processing times
                                 for each processing type
        processing_types (list): List of chars with processing types performed
    """
    img_file_path = fields.CharField(primary_key=True)
    user = fields.CharField()
    processing_times = fields.ListField(field=fields.FloatField())
    processing_types = fields.ListField(field=fields.CharField())
    original_height = fields.IntegerField()
    original_width = fields.IntegerField()
    processed_height = fields.ListField(field=fields.IntegerField())
    processed_width = fields.ListField(field=fields.IntegerField())
    upload_timestamp = fields.DateTimeField()

