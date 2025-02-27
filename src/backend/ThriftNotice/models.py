from django.db import models

# Create your models here.

class ThriftStores(models.Model):
    shopid              = models.BigAutoField   (db_column='ShopID', primary_key=True)                      # Field name made lowercase.
    shopname            = models.CharField      (db_column='ShopName')                                      # Field name made lowercase.
    formattedaddress    = models.TextField      (db_column='FormattedAddress', blank=True, null=True)       # Field name made lowercase.
    latitude            = models.FloatField     (db_column='Latitude', blank=True, null=True)               # Field name made lowercase.
    longitude           = models.FloatField     (db_column='Longitude', blank=True, null=True)              # Field name made lowercase.
    shortdescription    = models.TextField      (db_column='ShortDescription', blank=True, null=True)       # Field name made lowercase.
    pricerange          = models.TextField      (db_column='PriceRange', blank=True, null=True)             # Field name made lowercase.
    specialty           = models.TextField      (db_column='Specialty', blank=True, null=True)              # Field name made lowercase.
    isestablishedstore  = models.BinaryField    (db_column='IsEstablishedStore', blank=True, null=True)     # Field name made lowercase.
    popupstarttime      = models.DateTimeField  (db_column='PopUpStartTime', blank=True, null=True)         # Field name made lowercase.
    hasfittingrooms     = models.BooleanField   (db_column='HasFittingRooms', blank=True, null=True)        # Field name made lowercase.
    parkingavailability = models.TextField      (db_column='ParkingAvailability', blank=True, null=True)    # Field name made lowercase.
    ispopupevent        = models.BooleanField   (db_column='IsPopUpEvent', blank=True, null=True)           # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'thrift_stores'
        db_table_comment = 'A Relation Containing Information Of Each Thrift Shop'

    def __str__(self):
        return self.title