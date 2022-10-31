from django.db import models

Organization = (
    ('JISMONIY', "Jismoniy shaxs"),
    ('YURIDIK', "Yuridik shaxs"),
)
Status = (
    ('YANGI', "Yangi"),
    ('MODERATSIYADA', "Moderatsiyada"),
    ('TASDIQLANGAN', "Tasdiqlangan"),
    ('BEKOR QILINGAN', "Bekor qilingan"),
)


class Sponsor(models.Model):
    organization = models.CharField(max_length=20, choices=Organization, default='JISMONIY')
    full_name = models.CharField(max_length=150, verbose_name="F.I.SH.")
    phone_number = models.CharField(max_length=20, verbose_name="Telefon raqam")
    company_name = models.CharField(max_length=200, verbose_name="Tashkinot nomi", blank=True, null=True)
    payment_amount = models.IntegerField(verbose_name="Homiylik Summasi")
    allocated_amount = models.IntegerField(verbose_name="Sarflagan pullari", default=0)

    add_day = models.DateField(auto_now_add=True, verbose_name="Sana")
    update_day = models.DateTimeField(auto_now = True)
    status = models.CharField(max_length=30, choices=Status, default="YANGI")

    def rest_money(self):
        return self.payment_amount - self.allocated_amount

    def __str__(self):
        return self.full_name


Student_type = (
    ('MAGISTR', 'Magistr'),
    ('BAKALAVR', "Bakalavr"),
)


class Otm(models.Model):
    name = models.TextField(verbose_name="OTM")

    def __str__(self):
        return self.name


class Student(models.Model):
    full_name = models.CharField(max_length=150, verbose_name="F.I.SH.")
    phone_number = models.CharField(max_length=20, verbose_name="Telefon raqam", blank=True, null=True)
    student_type = models.CharField(max_length=20, choices=Student_type, default="BAKALAVR")
    otm = models.ForeignKey(Otm, on_delete=models.SET_NULL, null=True)
    allocated_amount = models.IntegerField(default=0)
    contract_amount = models.IntegerField(verbose_name="Kontrakt miqdori")
    add_day = models.DateField(auto_now_add=True, verbose_name='SANA')
    update_day = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.full_name

    def rest_money(self):
        return self.contract_amount - self.allocated_amount


class Metsenat(models.Model):
    sponsor = models.ForeignKey(Sponsor, on_delete=models.SET_NULL, null=True)
    payment = models.IntegerField(verbose_name="Ajratilgan summa")
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    payment_day = models.DateField(auto_now_add=True)
    update_day = models.DateTimeField(auto_now = True)

    def student_sum(self):
        return self.student.allocated_amount

    def sponsor_sum(self):
        return self.sponsor.payment_amount

    def __str__(self):
        return f"{self.id}  {self.student}   {self.sponsor}  {self.payment}"
