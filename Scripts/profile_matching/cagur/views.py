from django.shortcuts import render, redirect
from django.db.models import Sum
from .models import (
    Cagur, Gap, Kriteria, NilaiProfil, 
    PerhitunganAkhir, PerhitunganGap, 
    Ranking, SubKriteria
)

def dashboard(request):
    try:
        # Ambil data gap
        gaps = Gap.objects.all()

        # Ambil 5 peringkat teratas
        rank = Ranking.objects.order_by('rank')[:5]
        top1, top2, top3, top4, top5 = rank[0], rank[1], rank[2], rank[3], rank[4]

        # Kelola kriteria
        kriteria1 = Kriteria.objects.first()
        kriteria = Kriteria.objects.exclude(id=kriteria1.id)
        kriteria_ids = list(kriteria.values_list('id', flat=True))

        # Kelola sub kriteria
        sub_kriteria1 = SubKriteria.objects.filter(id_k=kriteria1.id)
        sub_kriteria = SubKriteria.objects.filter(id_k__in=kriteria_ids)

        context = {
            'gaps': gaps,
            'top1': top1, 'top2': top2, 'top3': top3, 'top4': top4, 'top5': top5,
            'kriteria1': kriteria1,
            'kriteria': kriteria,
            'sub_kriteria1': sub_kriteria1,
            'sub_kriteria': sub_kriteria
        }
        return render(request, 'dashboard.html', context)
    except Exception as e:
        # Tangani kesalahan jika terjadi
        return render(request, 'error.html', {'error': str(e)})

def ideal_profil(request):
    # Placeholder untuk implementasi IdealProfilController
    return render(request, 'ideal_profil.html')

def result(request):
    try:
        # Ambil data yang diperlukan untuk halaman hasil
        cagurs = Cagur.objects.all()
        
        # Gunakan pagination jika tersedia di Django
        nilai_profils = NilaiProfil.objects.all()[:12]
        sub_kriteria = SubKriteria.objects.filter(selected=True)

        perhitungan_gaps = PerhitunganGap.objects.all()[:12]
        perhitungan_akhirs = PerhitunganAkhir.objects.all()[:4]
        rankings = Ranking.objects.select_related('cagur').order_by('rank')[:5]

        context = {
            'cagurs': cagurs,
            'nilai_profils': nilai_profils,
            'sub_kriteria': sub_kriteria,
            'perhitungan_gaps': perhitungan_gaps,
            'perhitungan_akhirs': perhitungan_akhirs,
            'rankings': rankings
        }
        return render(request, 'result.html', context)
    except Exception as e:
        return render(request, 'error.html', {'error': str(e)})

def store_result(request):
    try:
        # Ambil cagur yang belum memiliki perhitungan akhir
        cagurs = Cagur.objects.exclude(perhitunganakhir_isnull=False)

        for cagur in cagurs:
            cagur_id = cagur.id

            # Ambil sub kriteria core dan secondary
            sub_kriteria_core = SubKriteria.objects.filter(
                selected=True, 
                kriteria__jenis='Core Factor'
            ).first()

            sub_kriteria_secondary = SubKriteria.objects.filter(
                selected=True, 
                kriteria__jenis='Secondary Factor'
            ).first()

            # Hitung perhitungan core dan secondary
            # ... (kode perhitungan tetap sama)

        return redirect('result')
    except Exception as e:
        # Tangani kesalahan jika terjadi
        return render(request, 'error.html', {'error': str(e)})

def store_rank(request):
    try:
        # Ambil cagur yang belum memiliki ranking
        cagurs = Cagur.objects.exclude(ranking__isnull=False)

        for cagur in cagurs:
            # Hitung total nilai
            total_nilai = PerhitunganAkhir.objects.filter(
                id_cagur=cagur.id
            ).aggregate(total_rata_rata=Sum('total_rata_rata'))['total_rata_rata'] or 0

            # Buat ranking
            ranking = Ranking.objects.create(
                id_cagur=cagur.id,
                total_nilai=total_nilai
            )

        # Urutkan dan berikan peringkat
        all_rankings = Ranking.objects.order_by('-total_nilai')
        for rank, ranking_item in enumerate(all_rankings, start=1):
            Ranking.objects.filter(id=ranking_item.id).update(rank=rank)

        return redirect('result')
    except Exception as e:
        # Tangani kesalahan jika terjadi
        return render(request, 'error.html', {'error': str(e)})