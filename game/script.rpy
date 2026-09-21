# game/script.rpy

# ==============================================================================
# TRANSFORMS & POSITIONING
# ==============================================================================
transform portrait_left:
    xoffset -200
    yalign 0.62

transform portrait_right:
    xoffset 200
    yalign 0.62

# ==============================================================================
# CHARACTER DEFINITIONS & VARIABLES
# ==============================================================================
define mc = Character("[player_name]", color="#78d6b9")
define tziyon = Character("Tziyon", color="#94a8f3")
define nar = Character(None) # Narrative voice

default player_name = "Kalista"
default bkt = None
default total_questions_solved = 0

# ==============================================================================
# MAIN STORY FLOW
# ==============================================================================
label start:
    show screen main_menu_shortcut_button

    $ bkt = BKTSystem()

    # $ bkt.kcs["KC-01"].update({"pL": 1.0, "fluency": 5, "mastered": True})
    # $ bkt.kcs["KC-02"].update({"pL": 1.0, "fluency": 5, "mastered": True})
    # $ bkt.kcs["KC-03"].update({"pL": 1.0, "fluency": 5, "mastered": True})
    # $ bkt.kcs["KC-04"].update({"pL": 1.0, "fluency": 5, "mastered": True})
    # $ bkt.kcs["KC-05"].update({"pL": 0.15, "fluency": 0, "mastered": False})
    # $ bkt.kcs["KC-06"].update({"pL": 0.10, "fluency": 0, "mastered": False})

    scene bg ruangosis with fade

    # Show the persistent tracker overlay at the top
    show screen bkt_tracker_overlay(bkt)

    show tziyon normal at portrait_left with dissolve
    show mc default at portrait_right with dissolve

    tziyon "Kalista, untuk membuktikan kamu layak jadi Ketua OSIS, kamu harus membuktikan bahwa setiap keputusanmu didasari perhitungan logis."
    tziyon "Setiap rencana program kerja yang kita perdebatkan hari ini harus kamu selesaikan lewat model perhitungan aljabar presisi."

    mc "Bagus. Tunjukkan semua proposal dan permasalahannya. Aku akan buktikan kalau logikaku tidak pernah salah."

    jump story_question_loop

# ==============================================================================
# QUESTION -> STORY -> QUESTION INTERLEAVED LOOP (MAX 10 QUESTIONS)
# ==============================================================================
label story_question_loop:

    # 1. CEK BATAS MAKSIMAL 10 SOAL ATAU MATERI SUDAH MASTERY
    if total_questions_solved >= 10:
        jump story_finale

    $ current_q = bkt.get_next_question()

    if current_q is None:
        jump story_finale

    $ total_questions_solved += 1

    # 2. NARASI NARRATIVE UNTUK TIAP SOAL (1 SAMPAI 10)
    scene bg ruangosis with fade
    show tziyon normal at portrait_left
    show mc default at portrait_right

    if total_questions_solved == 1:
        tziyon "Masalah pertama: Pembagian dana awal kampanye antara divisi Acara dan Humas."
        mc "Gampang. Kita seimbangkan variabel anggarannya dulu."

    elif total_questions_solved == 2:
        tziyon "Oke, tapi bagaimana jika divisi Logistik mendadak minta tambahan dana dengan tarif bertingkat?"
        mc "Tinggal pakai persamaan dua variabel. Perhatikan baik-baik perhitunganku."

    elif total_questions_solved == 3:
        tziyon "Tunggu, divisi Publikasi mengklaim percetakan poster membutuhkan penyesuaian biaya sewa printer."
        mc "Itu cuma masalah penyederhanaan bentuk aljabar dasar. Lihat ini."

    elif total_questions_solved == 4:
        scene bg aula with fade
        show tziyon normal at portrait_left
        show mc default at portrait_right
        tziyon "Kita pindah ke Aula. Lihat tempat duduk ini? Kita harus menghitung kapasitas maksimal penonton Kampanye Monolog."
        mc "Rumus deret dan aljabar kuncinya. Aku hitung kebutuhan kursi dan ruang geraknya."

    elif total_questions_solved == 5:
        tziyon "Bagaimana dengan pembagian shift panitia OSIS agar tidak ada anggota yang lembur?"
        mc "Pertidaksamaan variabel. Aku pastikan semua alokasi waktu panitia adil."

    elif total_questions_solved == 6:
        tziyon "Bagian Humas melapor bahwa persentase jangkauan angket siswa belum memenuhi target kuesioner."
        mc "Aku selesaikan estimasi rasio siswa yang belum mengisi survei sekarang."

    elif total_questions_solved == 7:
        scene bg ruangosis with fade
        show tziyon normal at portrait_left
        show mc default at portrait_right
        tziyon "Kembali ke Ruang OSIS. Sponsor utama minta perhitungan bagi hasil dana pameran seni sekolah."
        mc "Perhitungan komisi dan persen keuntungan sponsor bukan hal yang sulit buatku."

    elif total_questions_solved == 8:
        tziyon "Logistik panggung utama Fest: Listrik dan konsumsi daya vendor sound system berlebih."
        mc "Sistem persamaan ini akan membatasi pemborosan daya tanpa mengurangi kualitas acara."

    elif total_questions_solved == 9:
        tziyon "Hampir selesai. Sekarang hitung perkiraan waktu pemungutan suara online seluruh kelas."
        mc "Kecepatan server per menit dibanding jumlah pemilih. Ini langkah perhitungannya."

    elif total_questions_solved == 10:
        tziyon "Terakhir: Evaluasi total pengeluaran dan rekapitulasi dana sisa operasional OSIS."
        mc "Langkah terakhir ini akan menutup seluruh perdebatan kita, Tziyon!"

    # 3. EKSEKUSI SOAL STEP-BY-STEP
    label execute_steps:
        $ step = bkt.get_current_step()
        $ lowest_pl = min([bkt.kcs[k]["pL"] for k in step["kcs"]])
        
        if lowest_pl < HINT_TRIGGER_THRESHOLD:
            show screen bkt_hint_window(step["hint"])

        menu:
            tziyon "Selesaikan langkah perhitungan [total_questions_solved]/10 berikut:\n[step['state']]"

            "[step['options'][0]]":
                $ user_choice = 0
            "[step['options'][1]]":
                $ user_choice = 1
            "[step['options'][2]]":
                $ user_choice = 2
            "[step['options'][3]]":
                $ user_choice = 3
            "💡 Minta Petunjuk":
                show screen bkt_hint_window(step["hint"])
                jump execute_steps
            "⚡ DEV ONLY - Skip Semua KC (Instant Finale)":
                $ [bkt.kcs[k].update({'pL': 1.0, 'mastered': True}) for k in bkt.kcs]
                jump story_finale

        $ is_correct, is_finished = bkt.submit_answer(user_choice)

        if is_correct:
            show mc smirk at portrait_right
            mc "Tepat sekali. Langkah perhitunganku sudah benar."
        else:
            show tziyon bingung at portrait_left
            tziyon "Masih keliru. Langkah yang tepat seharusnya: [step['options'][step['correct']]]"
            tziyon "Fokus lagi, Kalista. Jangan sampai kecanduan mengambil keputusan tanpa ketelitian."

        if not is_finished:
            jump execute_steps

    jump story_question_loop

# ==============================================================================
# CONCLUSION
# ==============================================================================
label story_finale:
    scene bg aula with fade

    show tziyon normal at portrait_left with dissolve
    show mc smirk at portrait_right with dissolve

    tziyon "Luar biasa, Kalista. Kamu berhasil menyelesaikan seluruh 10 permasalahan program OSIS dengan logika yang sangat matang."
    
    mc "Sudah kubilang, kepemimpinan bukan cuma soal pidato manis, tapi juga tentang kepastian dan eksekusi yang terukur."

    tziyon "Aku mengaku kalah. Kamu sangat pantas memimpin OSIS periode ini!"

    hide screen bkt_tracker_overlay
    "SELAMAT! KAMU TELAH MENYELESAIKAN SELURUH PROGRAM DAN TANTANGAN KEPEMIMPINAN OSIS."
    return