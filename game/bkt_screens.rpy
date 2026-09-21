# game/bkt_screens.rpy

# Persistent bottom bar showing live KC mastery (Vertical Layout with Fluency)
screen bkt_tracker_overlay(bkt):
    zorder 100 # Keep on top of normal UI elements
    
    frame:
        xalign 0.5
        yalign 0.98
        xsize 1080
        ysize 400 # Height increased to account for larger text & spacing
        background Solid("#101820ee")
        padding (20, 15)

        vbox:
            xalign 0.5
            spacing 10
            text "📊 BKT Knowledge Mastery Tracker (Target: >85%)" size 22 color "#00e676" bold True xalign 0.5

            # Display all 6 KCs vertically (1 column, 6 rows)
            vbox:
                xalign 0.5
                spacing 8
                for key in kc_order:
                    $ kc_data = bkt.kcs[key]
                    $ pl_val = int(kc_data['pL'] * 100)
                    $ status_icon = "✅" if kc_data['mastered'] else "🔒"
                    
                    hbox:
                        xalign 0
                        spacing 14
                        
                        # KC ID
                        text "[key]":
                            size 18
                            color "#ffffff"
                            xsize 85
                        
                        # Progress Bar
                        bar:
                            value pl_val
                            range 100
                            xsize 340
                            ysize 20 # Thicker bar for higher visibility
                            left_bar Solid("#2ecc71" if kc_data['mastered'] else "#3498db")
                            right_bar Solid("#445566")

                        # Percentage
                        text "[pl_val]%" size 18 color "#ffffff" xsize 65

                        # Fluency Display
                        text "Fluency: [kc_data['fluency']]/[kc_data['target']]" size 18 color "#f1c40f" xsize 160

                        # Status Icon
                        text "[status_icon]" size 18 color "#ffffff"

# Modal hint popup window
screen bkt_hint_window(hint_text):
    modal True
    zorder 200

    frame:
        xalign 0.5
        yalign 0.4
        xsize 800
        ysize 250
        background Solid("#fff9c4e6")
        padding (25, 20)

        vbox:
            spacing 15
            xalign 0.5
            text "💡 PETUNJUK PENYELESAIAN" size 22 color "#f57f17" bold True xalign 0.5
            text "[hint_text]" size 22 color "#333333" text_align 0.5 xalign 0.5
            
            null height 10
            
            textbutton "Tutup / Paham":
                xalign 0.5
                text_size 20
                text_color "#ffffff"
                background Solid("#f57f17")
                hover_background Solid("#fbc02d")
                padding (20, 8)
                action Hide("bkt_hint_window")