# ==============================================================================
# CHARACTER DEFINITIONS
# ==============================================================================
define mc = Character("[player_name]", color="#78d6b9")
define tziyon = Character("Tziyon", color="#94a8f3")

# ==============================================================================
# GAME VARIABLES
# ==============================================================================
default player_name = "Kalista"

# ==============================================================================
# MAIN STORY
# ==============================================================================
label start:

    scene bg ruangosis with fade

    show tziyon normal at left with dissolve
    show mc default at right with dissolve

    show mc default at center:
        zoom 0.5

    tziyon "MC, kemarin kamu mengadakan makan besar, dan tersebar poket digital untuk bagi-bagi uang? Perlukah sampai melakukan politik uang?"

    show mc smirk

    mc "Ck. JENNI NGETEST PUSH"

    show tziyon bingung

    tziyon "Kamu melakukannya?"

    mc "Ya, kenapa? Iri karena tidak bisa melakukannya? Aku punya uang—"

    return

#XYZ------hehe.