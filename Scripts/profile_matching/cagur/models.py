from django.db import models

# Create your models here.

class Cagur(models.Model):
    nama = models.CharField(max_length=255)
    telp = models.CharField(max_length=255)
    pendidikan = models.CharField(max_length=255)
    ipk = models.CharField(max_length=255)
    pengalaman_mengajar = models.CharField(max_length=255)
    umur = models.CharField(max_length=255)
    psikotes = models.CharField(max_length=255)
    sertifikasi_keahlian = models.CharField(max_length=255)

    class Meta:
        db_table = 'cagur'

class Kriteria(models.Model):
    JENIS_CHOICES = [
        ('Core Factor', 'Core Factor'),
        ('Secondary Factor', 'Secondary Factor'),
    ]
    nama = models.CharField(max_length=255)
    jenis = models.CharField(max_length=20, choices=JENIS_CHOICES)

    class Meta:
        db_table = 'kriteria'

class SubKriteria(models.Model):
    kriteria = models.ForeignKey(Kriteria, on_delete=models.CASCADE, related_name='sub_kriteria')
    desc = models.CharField(max_length=255)
    nilai = models.SmallIntegerField()
    selected = models.BooleanField()

    class Meta:
        db_table = 'sub_kriteria'

class Gap(models.Model):
    gap = models.IntegerField()
    bobot_nilai = models.DecimalField(max_digits=8, decimal_places=1)
    keterangan = models.CharField(max_length=255)

    class Meta:
        db_table = 'gap'

class IdealProfil(models.Model):
    kriteria = models.ForeignKey(Kriteria, on_delete=models.CASCADE)
    sub_kriteria = models.ForeignKey(SubKriteria, on_delete=models.CASCADE)
    nilai_ideal = models.PositiveIntegerField()

    class Meta:
        db_table = 'ideal_profil'
        unique_together = ('kriteria', 'sub_kriteria')

class NilaiProfil(models.Model):
    cagur = models.ForeignKey(Cagur, on_delete=models.CASCADE)
    kriteria = models.ForeignKey(Kriteria, on_delete=models.CASCADE)
    sub_kriteria = models.ForeignKey(SubKriteria, on_delete=models.CASCADE)
    nilai_profil = models.PositiveIntegerField()

    class Meta:
        db_table = 'nilai_profil'
        unique_together = ('cagur', 'kriteria', 'sub_kriteria')

class PerhitunganGap(models.Model):
    cagur = models.ForeignKey(NilaiProfil, on_delete=models.CASCADE)
    sub_kriteria = models.ForeignKey(SubKriteria, on_delete=models.CASCADE)
    ideal_profil = models.IntegerField()
    gap = models.IntegerField()
    bobot_gap = models.DecimalField(max_digits=8, decimal_places=1)

    class Meta:
        db_table = 'perhitungan_gap'
        unique_together = ('cagur', 'sub_kriteria')

class PerhitunganAkhir(models.Model):
    cagur = models.ForeignKey(NilaiProfil, on_delete=models.CASCADE)
    sub_kriteria = models.ForeignKey(SubKriteria, on_delete=models.CASCADE)
    jumlah_nilai = models.DecimalField(max_digits=8, decimal_places=1)
    rata_rata = models.DecimalField(max_digits=8, decimal_places=4)
    total_rata_rata = models.DecimalField(max_digits=8, decimal_places=4)

    class Meta:
        db_table = 'perhitungan_akhir'
        unique_together = ('cagur', 'sub_kriteria')

class Ranking(models.Model):
    cagur = models.OneToOneField(NilaiProfil, on_delete=models.CASCADE, primary_key=True)
    total_nilai = models.DecimalField(max_digits=8, decimal_places=4)
    rank = models.SmallIntegerField(null=True, blank=True)

    class Meta:
        db_table = 'ranking'
