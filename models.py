# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class CoreCustomeuser(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    email = models.CharField(unique=True, max_length=254)

    class Meta:
        managed = False
        db_table = 'core_customeuser'


class CoreCustomeuserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    customeuser = models.ForeignKey(CoreCustomeuser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'core_customeuser_groups'
        unique_together = (('customeuser', 'group'),)


class CoreCustomeuserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    customeuser = models.ForeignKey(CoreCustomeuser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'core_customeuser_user_permissions'
        unique_together = (('customeuser', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(CoreCustomeuser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class LikesLikeditem(models.Model):
    id = models.BigAutoField(primary_key=True)
    object_id = models.PositiveBigIntegerField()
    content_type = models.ForeignKey(DjangoContentType, models.DO_NOTHING)
    user = models.ForeignKey(CoreCustomeuser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'likes_likeditem'


class SilkProfile(models.Model):
    name = models.CharField(max_length=300)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    time_taken = models.FloatField(blank=True, null=True)
    file_path = models.CharField(max_length=300)
    line_num = models.IntegerField(blank=True, null=True)
    end_line_num = models.IntegerField(blank=True, null=True)
    func_name = models.CharField(max_length=300)
    exception_raised = models.IntegerField()
    dynamic = models.IntegerField()
    request = models.ForeignKey('SilkRequest', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'silk_profile'


class SilkProfileQueries(models.Model):
    id = models.BigAutoField(primary_key=True)
    profile = models.ForeignKey(SilkProfile, models.DO_NOTHING)
    sqlquery = models.ForeignKey('SilkSqlquery', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'silk_profile_queries'
        unique_together = (('profile', 'sqlquery'),)


class SilkRequest(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    path = models.CharField(max_length=190)
    query_params = models.TextField()
    raw_body = models.TextField()
    body = models.TextField()
    method = models.CharField(max_length=10)
    start_time = models.DateTimeField()
    view_name = models.CharField(max_length=190, blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    time_taken = models.FloatField(blank=True, null=True)
    encoded_headers = models.TextField()
    meta_time = models.FloatField(blank=True, null=True)
    meta_num_queries = models.IntegerField(blank=True, null=True)
    meta_time_spent_queries = models.FloatField(blank=True, null=True)
    pyprofile = models.TextField()
    num_sql_queries = models.IntegerField()
    prof_file = models.CharField(max_length=300)

    class Meta:
        managed = False
        db_table = 'silk_request'


class SilkResponse(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    status_code = models.IntegerField()
    raw_body = models.TextField()
    body = models.TextField()
    encoded_headers = models.TextField()
    request = models.OneToOneField(SilkRequest, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'silk_response'


class SilkSqlquery(models.Model):
    query = models.TextField()
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    time_taken = models.FloatField(blank=True, null=True)
    traceback = models.TextField()
    request = models.ForeignKey(SilkRequest, models.DO_NOTHING, blank=True, null=True)
    identifier = models.IntegerField()
    analysis = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'silk_sqlquery'


class StoreAddress(models.Model):
    id = models.BigAutoField(primary_key=True)
    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    customer = models.ForeignKey(CoreCustomeuser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'store_address'


class StoreCart(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    datetime_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'store_cart'


class StoreCartitem(models.Model):
    id = models.BigAutoField(primary_key=True)
    quantity = models.PositiveSmallIntegerField()
    cart = models.ForeignKey(StoreCart, models.DO_NOTHING)
    product = models.ForeignKey('StoreProduct', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'store_cartitem'


class StoreCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    featured_product = models.ForeignKey('StoreProduct', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'store_category'


class StoreComment(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    body = models.TextField()
    datetime_created = models.DateTimeField()
    status = models.CharField(max_length=2)
    product = models.ForeignKey('StoreProduct', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'store_comment'


class StoreCustomer(models.Model):
    id = models.BigAutoField(primary_key=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(blank=True, null=True)
    user = models.OneToOneField(CoreCustomeuser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'store_customer'


class StoreDiscount(models.Model):
    id = models.BigAutoField(primary_key=True)
    discount = models.FloatField()
    description = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'store_discount'


class StoreOrder(models.Model):
    id = models.BigAutoField(primary_key=True)
    datetime_created = models.DateTimeField()
    status = models.CharField(max_length=1)
    customer = models.ForeignKey(StoreCustomer, models.DO_NOTHING)
    zarinpal_authority = models.CharField(max_length=255)
    zarinpal_data = models.TextField()
    zarinpal_ref_id = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'store_order'


class StoreOrderitem(models.Model):
    id = models.BigAutoField(primary_key=True)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    order = models.ForeignKey(StoreOrder, models.DO_NOTHING)
    product = models.ForeignKey('StoreProduct', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'store_orderitem'


class StoreProduct(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=50)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    description = models.TextField()
    datetime_created = models.DateTimeField()
    datetime_modified = models.DateTimeField()
    category = models.ForeignKey(StoreCategory, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'store_product'


class StoreProductDiscounts(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(StoreProduct, models.DO_NOTHING)
    discount = models.ForeignKey(StoreDiscount, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'store_product_discounts'
        unique_together = (('product', 'discount'),)


class StoreProductimage(models.Model):
    id = models.BigAutoField(primary_key=True)
    image = models.CharField(max_length=100)
    product = models.ForeignKey(StoreProduct, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'store_productimage'


class TagsTag(models.Model):
    id = models.BigAutoField(primary_key=True)
    label = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'tags_tag'


class TagsTaggeditem(models.Model):
    id = models.BigAutoField(primary_key=True)
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(DjangoContentType, models.DO_NOTHING)
    tag = models.ForeignKey(TagsTag, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'tags_taggeditem'
