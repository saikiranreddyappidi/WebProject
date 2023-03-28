# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ApporvedFiles(models.Model):
    slno = models.AutoField(primary_key=True)
    regno = models.CharField(max_length=45)
    file_name = models.CharField(max_length=45)
    file_type = models.CharField(max_length=45)
    file_link = models.CharField(max_length=350)
    subject = models.CharField(max_length=45)
    stu_comment = models.TextField(blank=True, null=True)
    apporved_by = models.CharField(max_length=45)
    fac_comment = models.TextField(blank=True, null=True)
    datetime = models.DateTimeField()
    enable = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'apporved_files'


class AssignedCookies(models.Model):
    id = models.BigAutoField(primary_key=True)
    reg = models.CharField(max_length=45)
    cookies = models.CharField(max_length=100)
    datetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'assigned_cookies'


class AssignedOtp(models.Model):
    sl_no = models.AutoField(primary_key=True)
    reg = models.CharField(max_length=45)
    otp = models.CharField(max_length=45)
    ip = models.CharField(max_length=45)
    datetime = models.DateTimeField()
    cookie = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'assigned_otp'


class AssignedSections(models.Model):
    slno = models.AutoField(primary_key=True)
    fac_id = models.CharField(max_length=45)
    sec = models.CharField(max_length=45)
    subject = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'assigned_sections'


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


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DeclinedFiles(models.Model):
    slno = models.AutoField(primary_key=True)
    regno = models.CharField(max_length=45)
    file_name = models.CharField(max_length=45)
    file_type = models.CharField(max_length=45)
    file_link = models.CharField(max_length=350)
    subject = models.CharField(max_length=45)
    stu_comment = models.TextField(blank=True, null=True)
    declined_by = models.CharField(max_length=45)
    fac_comment = models.TextField(blank=True, null=True)
    datetime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'declined_files'


class Digital(models.Model):
    sl_no = models.AutoField(db_column='Sl_No', primary_key=True)  # Field name made lowercase.
    reg_no = models.CharField(db_column='Reg_no', max_length=45)  # Field name made lowercase.
    intime = models.DateTimeField(db_column='Intime')  # Field name made lowercase.
    outtime = models.DateTimeField(db_column='Outtime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'digital'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

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


class Faculty(models.Model):
    sl_no = models.AutoField(primary_key=True)
    name = models.CharField(db_column='Name', max_length=45)  # Field name made lowercase.
    faculty_id = models.CharField(max_length=45)
    faculty_pswd = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'faculty'
        unique_together = (('sl_no', 'faculty_id'),)


class HtmlContent(models.Model):
    slno = models.AutoField(primary_key=True)
    regno = models.CharField(max_length=12)
    content = models.TextField(blank=True, null=True)
    lastmodified = models.DateTimeField()
    visibility = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'html_content'
        unique_together = (('slno', 'regno'),)


class LinksProvided(models.Model):
    sl_no = models.AutoField(primary_key=True)
    faculty_id = models.CharField(max_length=45)
    file_name = models.CharField(max_length=45)
    drive_links = models.CharField(max_length=100)
    branch = models.CharField(max_length=45)
    file_type = models.CharField(max_length=45)
    datetime = models.DateTimeField(blank=True, null=True)
    facultyname = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'links_provided'


class PdfsMembers(models.Model):
    id = models.BigAutoField(primary_key=True)
    regstration = models.CharField(max_length=255)
    sec = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'pdfs_members'


class StudentInfo(models.Model):
    sl_no = models.AutoField(db_column='Sl_No', primary_key=True)  # Field name made lowercase.
    reg_no = models.CharField(db_column='Reg_No', max_length=45)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=45)  # Field name made lowercase.
    password = models.CharField(db_column='PassWord', max_length=45)  # Field name made lowercase.
    email = models.CharField(max_length=45)
    photo_link = models.CharField(max_length=300, blank=True, null=True)
    ip = models.CharField(db_column='IP', max_length=45, blank=True, null=True)  # Field name made lowercase.
    sec = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student_info'
        unique_together = (('sl_no', 'reg_no'),)


class Userlinks(models.Model):
    slno = models.AutoField(primary_key=True)
    reg = models.CharField(max_length=45)
    sec = models.IntegerField(blank=True, null=True)
    filename = models.CharField(max_length=45)
    file_type = models.CharField(max_length=45)
    link = models.CharField(max_length=350)
    datetime = models.DateTimeField()
    subject = models.CharField(max_length=45)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'userlinks'
