
# ============================================
# Projet : Signature Numerique Simple
# Auteur : Marwa Maqsoudi (code apogee: 23512157)
#          Safaa Mounkid (code apogee: 23502171)
# Ce programme permet :
# 1. Generation des cles RSA
# 2. Signature d'un message
# 3. Verification de la signature
# ============================================

import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature


# =========================================================
# COULEURS
# =========================================================

PRIMARY = "#2F2FE4"
SECONDARY = "#162E93"
CARD = "#1A1953"
BACKGROUND = "#080616"
TEXT = "#FFFFFF"

SUCCESS = "#00FF99"
ERROR = "#FF4C4C"


# =========================================================
# FONCTIONS HOVER
# =========================================================

def on_enter(e):
    e.widget["background"] = "#4A4AFF"


def on_leave(e, color):
    e.widget["background"] = color


# =========================================================
# GÉNÉRATION DES CLÉS
# =========================================================

def generate_keys():

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    public_key = private_key.public_key()

    # Sauvegarde clé privée
    with open("private_key.pem", "wb") as private_file:
        private_file.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

    # Sauvegarde clé publique
    with open("public_key.pem", "wb") as public_file:
        public_file.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )

    result_label.config(
        text="Clés RSA générées avec succès",
        fg=SUCCESS
    )


# =========================================================
# CHARGEMENT DES CLÉS
# =========================================================

def load_private_key():
    with open("private_key.pem", "rb") as key_file:
        return serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )


def load_public_key():
    with open("public_key.pem", "rb") as key_file:
        return serialization.load_pem_public_key(
            key_file.read()
        )


# =========================================================
# SIGNATURE
# =========================================================

def sign_message():

    message = message_box.get("1.0", tk.END).strip()

    if not message:
        messagebox.showwarning(
            "Attention",
            "Veuillez entrer un message."
        )
        return

    try:

        private_key = load_private_key()

        signature = private_key.sign(
            message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        with open("signature.bin", "wb") as sig_file:
            sig_file.write(signature)

        result_label.config(
            text="Message signé avec succès",
            fg=SUCCESS
        )

        message_box.delete("1.0", tk.END)

    except FileNotFoundError:

        messagebox.showerror(
            "Erreur",
            "Veuillez générer les clés d'abord."
        )


# =========================================================
# VÉRIFICATION
# =========================================================

def verify_signature():

    message = message_box.get("1.0", tk.END).strip()

    if not message:
        messagebox.showwarning(
            "Attention",
            "Veuillez entrer un message."
        )
        return

    try:

        public_key = load_public_key()

        with open("signature.bin", "rb") as sig_file:
            signature = sig_file.read()

        public_key.verify(
            signature,
            message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        result_label.config(
            text="Signature VALIDE",
            fg=SUCCESS
        )

        message_box.delete("1.0", tk.END)

    except InvalidSignature:

        result_label.config(
            text="Signature INVALIDE",
            fg=ERROR
        )

        message_box.delete("1.0", tk.END)

    except FileNotFoundError:

        messagebox.showerror(
            "Erreur",
            "Clés ou signature introuvables."
        )


# =========================================================
# QUITTER
# =========================================================

def quit_app():

    response = messagebox.askyesno(
        "Quitter",
        "Voulez-vous vraiment quitter ?"
    )

    if response:
        window.destroy()


# =========================================================
# FENÊTRE PRINCIPALE
# =========================================================

window = tk.Tk()

window.title("Signature Numérique")
window.geometry("1000x680")
window.configure(bg=BACKGROUND)
window.resizable(True, True)


# =========================================================
# HEADER
# =========================================================

header_frame = tk.Frame(
    window,
    bg=BACKGROUND
)

header_frame.pack(pady=20)

title_label = tk.Label(
    header_frame,
    text="🔐 SIGNATURE NUMÉRIQUE SIMPLE",
    font=("Segoe UI", 24, "bold"),
    bg=BACKGROUND,
    fg=PRIMARY
)

title_label.pack()

subtitle_label = tk.Label(
    header_frame,
    text="Protection de l'intégrité et authenticité des messages",
    font=("Segoe UI", 11),
    bg=BACKGROUND,
    fg="lightgray"
)

subtitle_label.pack(pady=5)


# =========================================================
# CARD PRINCIPALE
# =========================================================

card_frame = tk.Frame(
    window,
    bg=CARD,
    width=900,
    height=450
)

card_frame.pack(pady=20)

card_frame.pack_propagate(False)


# =========================================================
# LABEL MESSAGE
# =========================================================

message_label = tk.Label(
    card_frame,
    text="   Entrer le message",
    font=("Segoe UI", 14, "bold"),
    bg=CARD,
    fg=TEXT
)

message_label.pack(anchor="w", padx=40, pady=(30, 10))


# =========================================================
# ZONE TEXTE
# =========================================================

message_box = ScrolledText(
    card_frame,
    width=85,
    height=10,
    font=("Consolas", 12),
    bg="#101030",
    fg="white",
    insertbackground="white",
    relief="flat",
    bd=3
)

message_box.pack(padx=40)


# =========================================================
# FRAME BOUTONS
# =========================================================

button_frame = tk.Frame(
    card_frame,
    bg=CARD
)

button_frame.pack(pady=35)


# =========================================================
# STYLE BOUTONS
# =========================================================

button_style = {
    "font": ("Segoe UI", 11, "bold"),
    "width": 18,
    "height": 2,
    "bd": 0,
    "cursor": "hand2",
    "fg": "white"
}


# =========================================================
# BOUTON GÉNÉRER
# =========================================================

generate_button = tk.Button(
    button_frame,
    text="Générer clés",
    command=generate_keys,
    bg=PRIMARY,
    activebackground="#4A4AFF",
    **button_style
)

generate_button.grid(row=0, column=0, padx=10)

generate_button.bind("<Enter>", on_enter)
generate_button.bind(
    "<Leave>",
    lambda e: on_leave(e, PRIMARY)
)


# =========================================================
# BOUTON SIGNER
# =========================================================

sign_button = tk.Button(
    button_frame,
    text="Signer",
    command=sign_message,
    bg=SECONDARY,
    activebackground="#4A4AFF",
    **button_style
)

sign_button.grid(row=0, column=1, padx=10)

sign_button.bind("<Enter>", on_enter)
sign_button.bind(
    "<Leave>",
    lambda e: on_leave(e, SECONDARY)
)


# =========================================================
# BOUTON VÉRIFIER
# =========================================================

verify_button = tk.Button(
    button_frame,
    text="✔ Vérifier",
    command=verify_signature,
    bg=PRIMARY,
    activebackground="#4A4AFF",
    **button_style
)

verify_button.grid(row=0, column=2, padx=10)

verify_button.bind("<Enter>", on_enter)
verify_button.bind(
    "<Leave>",
    lambda e: on_leave(e, PRIMARY)
)


# =========================================================
# BOUTON QUITTER
# =========================================================

quit_button = tk.Button(
    button_frame,
    text="❌ Quitter",
    command=quit_app,
    bg="#B00020",
    activebackground="#D00030",
    **button_style
)

quit_button.grid(row=0, column=3, padx=10)

quit_button.bind(
    "<Enter>",
    lambda e: e.widget.config(bg="#D00030")
)

quit_button.bind(
    "<Leave>",
    lambda e: e.widget.config(bg="#B00020")
)


# =========================================================
# LABEL RÉSULTAT
# =========================================================

result_label = tk.Label(
    card_frame,
    text="",
    font=("Segoe UI", 14, "bold"),
    bg=CARD
)

result_label.pack(pady=15)


# =========================================================
# FOOTER
# =========================================================

footer = tk.Label(
    window,
    text="Projet Sécurité Informatique - Signature Numérique",
    font=("Segoe UI", 10),
    bg=BACKGROUND,
    fg="gray"
)

footer.pack(side="bottom", pady=15)


# =========================================================
# LANCEMENT
# =========================================================

window.mainloop()