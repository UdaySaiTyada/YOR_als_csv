from django.db import models

# Create your models here.
class Properties(models.Model):
    id = models.IntegerField(primary_key=True)
    owner_id = models.IntegerField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    flat_no = models.TextField(blank=True, null=True)
    addressl1 = models.TextField(blank=True, null=True)
    locality = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    zipcode = models.IntegerField(blank=True, null=True)
    sqftsuper = models.IntegerField(blank=True, null=True)
    image = models.IntegerField(blank=True, null=True)
    images = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    sharetype = models.IntegerField(blank=True, null=True)
    baths = models.IntegerField(blank=True, null=True)
    kitchens = models.IntegerField(blank=True, null=True)
    washrooms = models.IntegerField(blank=True, null=True)
    totalrooms = models.IntegerField(blank=True, null=True)
    availrooms = models.IntegerField(blank=True, null=True)
    rent = models.IntegerField(blank=True, null=True)
    owner_rent = models.TextField(blank=True, null=True)
    parkingcharges = models.IntegerField(blank=True, null=True)
    deposite = models.IntegerField(blank=True, null=True)
    maintenance = models.IntegerField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    availfrom = models.TextField(blank=True, null=True)
    availto = models.TextField(blank=True, null=True)
    tenure = models.IntegerField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    cntrestaurants = models.IntegerField(blank=True, null=True)
    cnthospitals = models.IntegerField(blank=True, null=True)
    cntgyms = models.IntegerField(blank=True, null=True)
    cnttheater = models.IntegerField(blank=True, null=True)
    cntmalls = models.IntegerField(blank=True, null=True)
    workdistance = models.IntegerField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    blockname = models.TextField(blank=True, null=True)
    gender = models.IntegerField(blank=True, null=True)
    tag_as = models.TextField(blank=True, null=True)
    commpercentage = models.TextField(blank=True, null=True)
    tds = models.TextField(blank=True, null=True)
    actualosamount = models.TextField(db_column='actualOSAmount', blank=True, null=True)  # Field name made lowercase.
    pendingosamount = models.TextField(db_column='pendingOSAmount', blank=True, null=True)  # Field name made lowercase.
    amountremark = models.TextField(db_column='amountRemark', blank=True, null=True)  # Field name made lowercase.
    minimumguranteeisactive = models.TextField(db_column='minimumGuranteeIsActive', blank=True, null=True)  # Field name made lowercase.
    minimumguranteeamount = models.TextField(db_column='minimumGuranteeAmount', blank=True, null=True)  # Field name made lowercase.
    minimumguranteestart = models.TextField(db_column='minimumGuranteeStart', blank=True, null=True)  # Field name made lowercase.
    minimumguranteeend = models.TextField(db_column='minimumGuranteeEnd', blank=True, null=True)  # Field name made lowercase.
    propertyrules = models.TextField(blank=True, null=True)
    parking_number = models.TextField(blank=True, null=True)
    metatitle = models.TextField(blank=True, null=True)
    metakeyword = models.TextField(blank=True, null=True)
    metadescription = models.TextField(blank=True, null=True)
    assign_to = models.TextField(blank=True, null=True)
    golden = models.IntegerField(blank=True, null=True)
    partner = models.IntegerField(blank=True, null=True)
    showinhomepage = models.IntegerField(blank=True, null=True)
    created_at = models.TextField(blank=True, null=True)
    updated_at = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'properties'



class Users(models.Model):
    id = models.IntegerField(primary_key=True)
    owner_id = models.IntegerField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    flat_no = models.TextField(blank=True, null=True)
    addressl1 = models.TextField(blank=True, null=True)
    locality = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    zipcode = models.IntegerField(blank=True, null=True)
    sqftsuper = models.IntegerField(blank=True, null=True)
    image = models.IntegerField(blank=True, null=True)
    images = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    sharetype = models.IntegerField(blank=True, null=True)
    baths = models.IntegerField(blank=True, null=True)
    kitchens = models.IntegerField(blank=True, null=True)
    washrooms = models.IntegerField(blank=True, null=True)
    totalrooms = models.IntegerField(blank=True, null=True)
    availrooms = models.IntegerField(blank=True, null=True)
    rent = models.IntegerField(blank=True, null=True)
    owner_rent = models.TextField(blank=True, null=True)
    parkingcharges = models.IntegerField(blank=True, null=True)
    deposite = models.IntegerField(blank=True, null=True)
    maintenance = models.IntegerField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    availfrom = models.TextField(blank=True, null=True)
    availto = models.TextField(blank=True, null=True)
    tenure = models.IntegerField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    cntrestaurants = models.IntegerField(blank=True, null=True)
    cnthospitals = models.IntegerField(blank=True, null=True)
    cntgyms = models.IntegerField(blank=True, null=True)
    cnttheater = models.IntegerField(blank=True, null=True)
    cntmalls = models.IntegerField(blank=True, null=True)
    workdistance = models.IntegerField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    blockname = models.TextField(blank=True, null=True)
    gender = models.IntegerField(blank=True, null=True)
    tag_as = models.TextField(blank=True, null=True)
    commpercentage = models.TextField(blank=True, null=True)
    tds = models.TextField(blank=True, null=True)
    actualosamount = models.TextField(db_column='actualOSAmount', blank=True, null=True)  # Field name made lowercase.
    pendingosamount = models.TextField(db_column='pendingOSAmount', blank=True, null=True)  # Field name made lowercase.
    amountremark = models.TextField(db_column='amountRemark', blank=True, null=True)  # Field name made lowercase.
    minimumguranteeisactive = models.TextField(db_column='minimumGuranteeIsActive', blank=True, null=True)  # Field name made lowercase.
    minimumguranteeamount = models.TextField(db_column='minimumGuranteeAmount', blank=True, null=True)  # Field name made lowercase.
    minimumguranteestart = models.TextField(db_column='minimumGuranteeStart', blank=True, null=True)  # Field name made lowercase.
    minimumguranteeend = models.TextField(db_column='minimumGuranteeEnd', blank=True, null=True)  # Field name made lowercase.
    propertyrules = models.TextField(blank=True, null=True)
    parking_number = models.TextField(blank=True, null=True)
    metatitle = models.TextField(blank=True, null=True)
    metakeyword = models.TextField(blank=True, null=True)
    metadescription = models.TextField(blank=True, null=True)
    assign_to = models.TextField(blank=True, null=True)
    golden = models.IntegerField(blank=True, null=True)
    partner = models.IntegerField(blank=True, null=True)
    showinhomepage = models.IntegerField(blank=True, null=True)
    created_at = models.TextField(blank=True, null=True)
    updated_at = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'