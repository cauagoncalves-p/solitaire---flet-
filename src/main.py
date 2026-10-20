
import flet as ft


class Solitaire:
    def __init__(self):
        self.start_top = 0
        self.start_left = 0
        
def main(page: ft.Page):
    solitaire = Solitaire()

    def drag(e: ft.DragUpdateEvent):
        e.control.top = max(0, e.control.top + e.local_delta.y)
        e.control.left = max(0, e.control.left + e.local_delta.x)
        e.control.update()

    def move_on_top(card):
        """Move a carta arrastada para o topo da pilha"""
        stack.controls.remove(card)
        stack.controls.append(card)
        stack.update()

    def start_drag(e: ft.DragStartEvent):
        move_on_top(e.control)
        solitaire.start_top = e.control.top
        solitaire.start_left = e.control.left

    def place(card, slot):
        """Encaixa a carta no slot"""
        card.top = slot.top
        card.left = slot.left

    def bounce_back(card):
        """Devolve a carta para a posição original"""
        card.top = solitaire.start_top
        card.left = solitaire.start_left

    def drop(e: ft.DragEndEvent):
        for slot in slots:
            if (
                abs(e.control.top - slot.top) < 20
                and abs(e.control.left - slot.left) < 20
            ):
                place(e.control, slot)
                break
        else:
            bounce_back(e.control)
        e.control.update()

    def make_card(image_src, left, top):
        return ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.MOVE,
            drag_interval=5,
            on_pan_start=start_drag,
            on_pan_update=drag,
            on_pan_end=drop,
            left=left,
            top=top,
            content=ft.Container(
                width=70,
                height=100,
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,  # corta a imagem nos cantos arredondados
                content=ft.Image(
                    src=image_src,  # relativo a assets, ex: "carta1.png"
                    width=70,
                    height=100,
                    fit=ft.BoxFit.FILL
                ),
            ),
        )

    def make_slot(left, top, color=ft.Colors.BLUE_100):
        return ft.Container(
            width=70,
            height=100,
            left=left,
            top=top,
            bgcolor=color,
            border=ft.Border.all(1, ft.Colors.BLUE_400), 
        )

    card1 = make_card("logo_fatec.png", 0, 0)
    card2 = make_card("logo_fiap.png", 100, 0)
    slots = [make_slot(0, 0), make_slot(200, 0), make_slot(300, 0)]

    stack = ft.Stack(
        controls=[*slots, card1, card2],  # slots primeiro (fundo), cartas depois
        width=1000,
        height=500,
    )
    page.add(stack)


ft.run(main, assets_dir="assets")