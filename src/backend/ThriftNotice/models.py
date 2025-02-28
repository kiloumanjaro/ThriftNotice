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
    popupstarttime      = models.TimeField      (db_column='PopUpStartTime', blank=True, null=True)         # Field name made lowercase.
    hasfittingrooms     = models.BooleanField   (db_column='HasFittingRooms', blank=True, null=True)        # Field name made lowercase.
    parkingavailability = models.TextField      (db_column='ParkingAvailability', blank=True, null=True)    # Field name made lowercase.
    review              = models.TextField      (db_column='Review', blank=True, null=True)                 # Field name made lowercase.

    class Meta:
        db_table = 'thrift_stores'
        db_table_comment = 'A Relation Containing Information Of Each Thrift Shop'

class Users(models.Model):
    userid              = models.BigAutoField   (db_column='userid', primary_key=True)                      # Field name made lowercase.
    username            = models.TextField      (db_column='username', blank=True, null=True)               # Field name made lowercase.
    clothing            = models.TextField      (db_column='clothing', blank=True, null=True)               # Field name made lowercase.
    budget              = models.TextField      (db_column='budget', blank=True, null=True)                 # Field name made lowercase.
    shoppingenvironment = models.TextField      (db_column='shoppingenvironment', blank=True, null=True)    # Field name made lowercase.
    organization        = models.TextField      (db_column='organization', blank=True, null=True)           # Field name made lowercase.
    interest            = models.TextField      (db_column='interest', blank=True, null=True)               # Field name made lowercase.

    class Meta:
        db_table = 'users_pref'
        db_table_comment = 'A Relation Containing Information Of Users Preferences'

class FavoriteShop(models.Model):
    userid = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='userid', primary_key=True)  
    shopid = models.ForeignKey(ThriftStores, on_delete=models.CASCADE, db_column='shopid')

    class Meta:
        db_table = 'favorite_shops'
        db_table_comment = 'A table storing favorite shops for each user.'
        unique_together = ('userid', 'shopid')  # Ensures a user can't favorite the same shop twice