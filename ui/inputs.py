import flet as ft

def fsociety_input(hint: str, default: str = "", width: int = 222, font_family: str = "JetMedium", color: str = "#00FF00") -> ft.TextField:
    return ft.TextField(
        hint_text=hint,
        value=default,
        width=width,
        text_style=ft.TextStyle(font_family=font_family, size=15, color=color),
        hint_style=ft.TextStyle(color="#FF0000", font_family=font_family),
        border_width=1,
        border_color="#FF0000",
        border_radius=5,
        bgcolor="black",
        focused_bgcolor="black",
        cursor_color="#FF0000",
        selection_color="#FF0000",
        content_padding=10,
        text_align=ft.TextAlign.CENTER
    )
