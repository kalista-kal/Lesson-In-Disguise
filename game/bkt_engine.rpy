# game/bkt_engine.rpy

init python:
    import random

    MASTERY_THRESHOLD = 0.85
    HINT_TRIGGER_THRESHOLD = 0.20

    kc_order = ["KC-01", "KC-02", "KC-03", "KC-04", "KC-05", "KC-06"]

    # Initial Knowledge Components state matching your JS setup
    default_kcs = {
        "KC-01": {"name": "Term & Sign Mgt.", "pL": 0.10, "pT": 0.15, "pS": 0.10, "pG": 0.30, "fluency": 0, "target": 3, "mastered": False},
        "KC-02": {"name": "Coeff. Clearance", "pL": 0.10, "pT": 0.15, "pS": 0.10, "pG": 0.30, "fluency": 0, "target": 3, "mastered": False},
        "KC-03": {"name": "Collect Like Terms", "pL": 0.10, "pT": 0.10, "pS": 0.15, "pG": 0.15, "fluency": 0, "target": 3, "mastered": False},
        "KC-04": {"name": "Distributive Prop.", "pL": 0.05, "pT": 0.08, "pS": 0.20, "pG": 0.10, "fluency": 0, "target": 3, "mastered": False},
        "KC-05": {"name": "Var. Substitution", "pL": 0.05, "pT": 0.05, "pS": 0.25, "pG": 0.05, "fluency": 0, "target": 4, "mastered": False},
        "KC-06": {"name": "Eq. Elimination", "pL": 0.05, "pT": 0.05, "pS": 0.25, "pG": 0.05, "fluency": 0, "target": 4, "mastered": False}
    }

    # Full Question Bank translated from JS
    question_bank = [
        # LEVEL 1 (KC-01, KC-02)
        {"id": 101, "steps": [{"state": "x + 5 = 12", "kcs": ["KC-01"], "hint": "(Kurangkan 5 di kedua ruas) x + 5 - 5 = 12 - 5", "options": ["x = 7", "x = 17", "x = -7", "x = 60"], "correct": 0}]},
        {"id": 102, "steps": [{"state": "x - 4 = -10", "kcs": ["KC-01"], "hint": "(Tambahkan 4 di kedua ruas) x - 4 + 4 = -10 + 4", "options": ["x = -6", "x = -14", "x = 6", "x = 14"], "correct": 0}]},
        {"id": 103, "steps": [{"state": "8 + x = 3", "kcs": ["KC-01"], "hint": "(Kurangkan 8 di kedua ruas) 8 - 8 + x = 3 - 8", "options": ["x = -5", "x = 5", "x = 11", "x = 24"], "correct": 0}]},
        {"id": 104, "steps": [{"state": "6x = 24", "kcs": ["KC-02"], "hint": "(Bagi kedua ruas dengan 6) 6x / 6 = 24 / 6", "options": ["x = 4", "x = 18", "x = 30", "x = 144"], "correct": 0}]},
        {"id": 105, "steps": [{"state": "x / 3 = 7", "kcs": ["KC-02"], "hint": "(Kalikan kedua ruas dengan 3) x/3 * 3 = 7 * 3", "options": ["x = 21", "x = 10", "x = 4", "x = 2.33"], "correct": 0}]},
        {"id": 106, "steps": [{"state": "-2x = 10", "kcs": ["KC-02"], "hint": "(Bagi kedua ruas dengan -2) -2x / -2 = 10 / -2", "options": ["x = -5", "x = 5", "x = -20", "x = 12"], "correct": 0}]},
        {"id": 107, "steps": [
            {"state": "3x + 1 = 10", "kcs": ["KC-01"], "hint": "(Kurangkan 1 di kedua ruas) 3x + 1 - 1 = 10 - 1", "options": ["3x = 9", "3x = 11", "4x = 10", "3x = -9"], "correct": 0},
            {"state": "3x = 9", "kcs": ["KC-02"], "hint": "(Bagi kedua ruas dengan 3) 3x / 3 = 9 / 3", "options": ["x = 3", "x = 6", "x = 12", "x = 27"], "correct": 0}
        ]},

        # LEVEL 2 (KC-03, KC-04)
        {"id": 201, "steps": [
            {"state": "4x + 3x = 21", "kcs": ["KC-03"], "hint": "(Jumlahkan suku bervariabel sama) contoh: 4x + 3x = (4+3)x", "options": ["7x = 21", "x = 21", "12x = 21", "7x² = 21"], "correct": 0},
            {"state": "7x = 21", "kcs": ["KC-02"], "hint": "(Bagi kedua ruas dengan 7) 7x / 7 = 21 / 7", "options": ["x = 3", "x = 14", "x = 28", "x = 147"], "correct": 0}
        ]},
        {"id": 202, "steps": [
            {"state": "8x - 2x = 36", "kcs": ["KC-03"], "hint": "(Kurangkan suku bervariabel sama) contoh: 8x - 2x = (8-2)x", "options": ["6x = 36", "10x = 36", "4x = 36", "-6x = 36"], "correct": 0},
            {"state": "6x = 36", "kcs": ["KC-02"], "hint": "(Bagi kedua ruas dengan 6) 6x / 6 = 36 / 6", "options": ["x = 6", "x = 30", "x = 42", "x = 216"], "correct": 0}
        ]},
        {"id": 203, "steps": [
            {"state": "x + 5x - 4 = 14", "kcs": ["KC-03"], "hint": "(Jumlahkan suku bervariabel sama) ingat x = 1x", "options": ["6x - 4 = 14", "5x - 4 = 14", "4x - 4 = 14", "6x = 10"], "correct": 0},
            {"state": "6x - 4 = 14", "kcs": ["KC-01"], "hint": "(Tambahkan 4 di kedua ruas) 6x - 4 + 4 = 14 + 4", "options": ["6x = 18", "6x = 10", "10x = 14", "6x = -18"], "correct": 0},
            {"state": "6x = 18", "kcs": ["KC-02"], "hint": "(Bagi kedua ruas dengan 6) 6x / 6 = 18 / 6", "options": ["x = 3", "x = 12", "x = 24", "x = 108"], "correct": 0}
        ]},
        {"id": 204, "steps": [
            {"state": "2(x + 4) = 18", "kcs": ["KC-04"], "hint": "(Kalikan masuk ke dalam kurung) 2*x + 2*4 = 18", "options": ["2x + 8 = 18", "2x + 4 = 18", "x + 8 = 18", "2x - 8 = 18"], "correct": 0},
            {"state": "2x + 8 = 18", "kcs": ["KC-01"], "hint": "(Kurangkan 8 di kedua ruas) 2x + 8 - 8 = 18 - 8", "options": ["2x = 10", "2x = 26", "10x = 18", "2x = -10"], "correct": 0},
            {"state": "2x = 10", "kcs": ["KC-02"], "hint": "(Bagi kedua ruas dengan 2) 2x / 2 = 10 / 2", "options": ["x = 5", "x = 8", "x = 12", "x = 20"], "correct": 0}
        ]},
        {"id": 205, "steps": [
            {"state": "4(2x - 1) = 12", "kcs": ["KC-04"], "hint": "(Kalikan masuk ke dalam kurung) 4*2x - 4*1 = 12", "options": ["8x - 4 = 12", "8x - 1 = 12", "6x - 4 = 12", "8x + 4 = 12"], "correct": 0},
            {"state": "8x - 4 = 12", "kcs": ["KC-01"], "hint": "(Tambahkan 4 di kedua ruas) 8x - 4 + 4 = 12 + 4", "options": ["8x = 16", "8x = 8", "4x = 12", "8x = -16"], "correct": 0},
            {"state": "8x = 16", "kcs": ["KC-02"], "hint": "(Bagi kedua ruas dengan 8) 8x / 8 = 16 / 8", "options": ["x = 2", "x = 8", "x = 24", "x = 128"], "correct": 0}
        ]},

        # LEVEL 3 (KC-05, KC-06)
        {"id": 301, "steps": [
            {"state": "y = 2x\nx + y = 9", "kcs": ["KC-05"], "hint": "(Ganti nilai y dengan 2x pada persamaan kedua) x + (2x) = 9", "options": ["x + 2x = 9", "2x + y = 9", "x + 2 = 9", "x + y = 2x"], "correct": 0},
            {"state": "x + 2x = 9", "kcs": ["KC-03"], "hint": "(Jumlahkan suku bervariabel sama) ingat x = 1x", "options": ["3x = 9", "2x² = 9", "x = 9", "4x = 9"], "correct": 0},
            {"state": "3x = 9", "kcs": ["KC-02"], "hint": "(Bagi kedua ruas dengan 3) 3x / 3 = 9 / 3", "options": ["x = 3", "x = 6", "x = 12", "x = 27"], "correct": 0}
        ]},
        {"id": 302, "steps": [
            {"state": "x = y + 3\n2x + y = 15", "kcs": ["KC-05"], "hint": "(Ganti nilai x dengan y+3 pada persamaan kedua) 2(y+3) + y = 15", "options": ["2(y + 3) + y = 15", "2y + 3 + y = 15", "x + 2x = 15", "2(y) + 3 = 15"], "correct": 0},
            {"state": "2(y + 3) + y = 15", "kcs": ["KC-04"], "hint": "(Kalikan masuk ke dalam kurung) 2*y + 2*3 + y = 15", "options": ["2y + 6 + y = 15", "2y + 3 + y = 15", "4y + y = 15", "2y - 6 + y = 15"], "correct": 0},
            {"state": "2y + 6 + y = 15", "kcs": ["KC-03"], "hint": "(Jumlahkan suku bervariabel sama) 2y + y = 3y", "options": ["3y + 6 = 15", "2y + 6y = 15", "8y = 15", "y + 6 = 15"], "correct": 0},
            {"state": "3y + 6 = 15", "kcs": ["KC-01"], "hint": "(Kurangkan 6 di kedua ruas) 3y + 6 - 6 = 15 - 6", "options": ["3y = 9", "3y = 21", "9y = 15", "3y = -9"], "correct": 0},
            {"state": "3y = 9", "kcs": ["KC-02"], "hint": "(Bagi kedua ruas dengan 3) 3y / 3 = 9 / 3", "options": ["y = 3", "y = 6", "y = 12", "y = 27"], "correct": 0}
        ]},
        {"id": 303, "steps": [
            {"state": "x + y = 10\nx - y = 2\n(Jumlahkan Kedua Pers.)", "kcs": ["KC-06"], "hint": "(Tambahkan kedua persamaan secara vertikal) x + y + x - y = 10 + 2", "options": ["2x = 12", "2y = 12", "2x = 8", "x = 12"], "correct": 0},
            {"state": "2x = 12", "kcs": ["KC-02"], "hint": "(Bagi kedua ruas dengan 2) 2x / 2 = 12 / 2", "options": ["x = 6", "x = 10", "x = 14", "x = 24"], "correct": 0},
            {"state": "Jika x = 6,\nx + y = 10", "kcs": ["KC-05"], "hint": "(Ganti variabel x dengan 6) 6 + y = 10", "options": ["6 + y = 10", "y - 6 = 10", "6 - y = 10", "10 + y = 6"], "correct": 0},
            {"state": "6 + y = 10", "kcs": ["KC-01"], "hint": "(Kurangkan 6 di kedua ruas) 6 - 6 + y = 10 - 6", "options": ["y = 4", "y = 16", "y = -4", "y = 60"], "correct": 0}
        ]},
        {"id": 304, "steps": [
            {"state": "2x + y = 11\n2x - y = 5\n(Jumlahkan Kedua Pers.)", "kcs": ["KC-06"], "hint": "(Tambahkan kedua persamaan secara vertikal) 2x + y + 2x - y = 11 + 5", "options": ["4x = 16", "4x = 6", "2y = 16", "x = 16"], "correct": 0},
            {"state": "4x = 16", "kcs": ["KC-02"], "hint": "(Bagi kedua ruas dengan 4) 4x / 4 = 16 / 4", "options": ["x = 4", "x = 12", "x = 20", "x = 64"], "correct": 0},
            {"state": "Jika x = 4,\n2x + y = 11", "kcs": ["KC-05"], "hint": "(Ganti variabel x dengan 4) 2(4) + y = 11", "options": ["2(4) + y = 11", "4 + y = 11", "8x + y = 11", "2(y) + 4 = 11"], "correct": 0},
            {"state": "2(4) + y = 11", "kcs": ["KC-02"], "hint": "(Kalikan angka yang ada di dalam kurung) 2 * 4", "options": ["8 + y = 11", "6 + y = 11", "24 + y = 11", "11 + y = 8"], "correct": 0},
            {"state": "8 + y = 11", "kcs": ["KC-01"], "hint": "(Kurangkan 8 di kedua ruas) 8 - 8 + y = 11 - 8", "options": ["y = 3", "y = 19", "y = -3", "y = 88"], "correct": 0}
        ]}
    ]

    class BKTSystem:
        def __init__(self):
            # Deep copy default state so it can reset per playthrough
            self.kcs = {k: v.copy() for k, v in default_kcs.items()}
            self.solved_ids = []
            self.current_question = None
            self.current_step_index = 0
            self.step_history = []

        def update_bkt(self, kc_id, is_correct):
            kc = self.kcs[kc_id]
            pL, pS, pG, pT = kc["pL"], kc["pS"], kc["pG"], kc["pT"]

            if is_correct:
                kc["fluency"] = min(kc["target"] + 2, kc["fluency"] + 1)
                pL_obs = (pL * (1.0 - pS)) / ((pL * (1.0 - pS)) + ((1.0 - pL) * pG))
            else:
                kc["fluency"] = max(0, kc["fluency"] - 1)
                pL_obs = (pL * pS) / ((pL * pS) + ((1.0 - pL) * (1.0 - pG)))

            kc["pL"] = pL_obs + (1.0 - pL_obs) * pT
            kc["pL"] = max(0.01, min(0.99, kc["pL"]))

            if kc["pL"] >= MASTERY_THRESHOLD and kc["fluency"] >= kc["target"]:
                kc["mastered"] = True
            elif kc["pL"] < 0.75 or kc["fluency"] < (kc["target"] - 2):
                kc["mastered"] = False

        def get_next_question(self):
            self.step_history = []
            
            # Find first unmastered KC in order
            target_kc = next((id_ for id_ in kc_order if not self.kcs[id_]["mastered"]), None)

            if not target_kc:
                self.current_question = None
                return None  # All mastered!

            target_index = kc_order.index(target_kc)
            allowed_kcs = kc_order[:target_index + 1]

            # Filter valid questions matching active level
            available = []
            for q in question_bank:
                q_kcs = set(kc for step in q["steps"] for kc in step["kcs"])
                is_allowed = all(kc in allowed_kcs for kc in q_kcs)
                has_unmastered = any(not self.kcs[kc]["mastered"] for kc in q_kcs)
                if is_allowed and has_unmastered:
                    available.append(q)

            unsolved = [q for q in available if q["id"] not in self.solved_ids]

            if unsolved:
                available = unsolved
            elif not available:
                available = [q for q in question_bank if all(kc in allowed_kcs for step in q["steps"] for kc in step["kcs"])]

            self.current_question = random.choice(available)
            self.current_step_index = 0
            self.step_history.append(self.current_question["steps"][0]["state"])
            return self.current_question

        def get_current_step(self):
            if self.current_question and self.current_step_index < len(self.current_question["steps"]):
                return self.current_question["steps"][self.current_step_index]
            return None

        def submit_answer(self, selected_index):
            step = self.get_current_step()
            if not step:
                return False, False

            is_correct = (selected_index == step["correct"])
            
            # Update BKT for all KCs tied to this step
            for kc_id in step["kcs"]:
                self.update_bkt(kc_id, is_correct)

            correct_option_text = step["options"][step["correct"]]
            self.step_history.append(correct_option_text)

            is_question_finished = False
            if is_correct:
                if self.current_step_index == len(self.current_question["steps"]) - 1:
                    if self.current_question["id"] not in self.solved_ids:
                        self.solved_ids.append(self.current_question["id"])
                    is_question_finished = True
                else:
                    self.current_step_index += 1
            else:
                # Direct correction path logic
                if self.current_step_index == len(self.current_question["steps"]) - 1:
                    is_question_finished = True
                else:
                    self.current_step_index += 1

            return is_correct, is_question_finished