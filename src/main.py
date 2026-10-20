import flet as ft


def main(page: ft.Page):
    # Aqui eu guardo a posição de onde a carta estava antes de eu começar
    # a arrastar. Assim, se eu soltar num lugar inválido, ela volta pra cá.
    inicio = {}

    def start_drag(e):
        # Quando eu clico na carta e começo a arrastar, essa função roda.
        # e.control é a carta que eu estou segurando.
        card = e.control

        # Salvo a posição atual (top = distância do topo, left = distância da esquerda)
        # pra poder voltar depois, se precisar.
        inicio["pos"] = (card.top, card.left)

        # No Stack, quem está por último na lista aparece por cima.
        # Então tiro a carta da lista e coloco no final, pra ela ficar
        # na frente das outras enquanto eu arrasto.
        stack.controls.remove(card)
        stack.controls.append(card)
        stack.update()

    def drag(e):
        # Essa função roda toda vez que o mouse se mexe durante o arraste.
        # local_delta é "o quanto o mouse andou" desde o último movimento.
        # Somo isso na posição da carta pra ela acompanhar o mouse.
        # O max(0, ...) impede a carta de sair pra fora da área (não fica negativa).
        e.control.top = max(0, e.control.top + e.local_delta.y)
        e.control.left = max(0, e.control.left + e.local_delta.x)
        e.control.update()

    def drop(e):
        # Essa função roda quando eu solto o botão do mouse.
        card = e.control

        # Vou olhar todos os "alvos" possíveis: as outras cartas e os slots.
        # Coloquei as cartas primeiro na lista pra elas terem prioridade.
        for alvo in [*cards, *slots]:
            # Não faz sentido comparar a carta com ela mesma, então pulo.
            if alvo is card:
                continue

            # Se a carta está a menos de 20 pixels do alvo (na vertical e na
            # horizontal), considero que eu quis soltar ali.
            if abs(card.top - alvo.top) < 20 and abs(card.left - alvo.left) < 20:
                # Encaixo a carta na mesma posição horizontal do alvo.
                card.left = alvo.left

                # Na vertical: se o alvo for outra carta, desço 20 pixels
                # pra dar pra ver que tem uma carta embaixo. Se for um slot, fica
                # na mesma altura dele.
                card.top = alvo.top + (20 if alvo in cards else 0)

                # Já encontrei onde encaixar, então paro de procurar.
                break
        else:
            # Esse "else" é do "for": ele só roda se o loop terminou SEM dar
            # break, ou seja, não achei nenhum alvo perto.
            # Então devolvo a carta pra posição onde ela estava antes.
            card.top, card.left = inicio["pos"]

        card.update()

    def make_card(src, left, top):
        # Essa função cria uma carta. Eu uso ela pra não repetir código
        # toda vez que quiser uma carta nova.
        # O GestureDetector é o que "escuta" o mouse: clicar, arrastar e soltar.
        return ft.GestureDetector(
            left=left,  # posição inicial na horizontal
            top=top,    # posição inicial na vertical
            mouse_cursor=ft.MouseCursor.MOVE,  # cursor vira setinha de mover
            drag_interval=5,  # de quantos em quantos ms ele avisa que o mouse se moveu
            on_pan_start=start_drag,   # quando começo a arrastar -> start_drag
            on_pan_update=drag,        # enquanto arrasto -> drag
            on_pan_end=drop,           # quando solto -> drop
            # O conteúdo da carta é só uma imagem, que vem da pasta assets.
            content=ft.Image(src=src, width=70, height=100, fit=ft.BoxFit.FILL),
        )

    def make_slot(left):
        # Cria um slot: o "espaço vazio" onde as cartas podem ser colocadas.
        # É só um retângulo azul clarinho com borda, pra eu enxergar onde fica.
        # O top é sempre 0, então só preciso informar o left.
        return ft.Container(
            left=left,
            top=0,
            width=70,
            height=100,
            bgcolor=ft.Colors.BLUE_100,
            border=ft.Border.all(1, ft.Colors.BLUE_400),
        )

    # Crio 3 slots, um em cada posição horizontal (0, 200 e 300).
    slots = [make_slot(0), make_slot(200), make_slot(300)]

    # Crio 2 cartas, cada uma com uma imagem diferente e posição inicial diferente.
    cards = [make_card("logo_fatec.png", 0, 0), make_card("logo_fiap.png", 100, 0)]

    # O Stack é a "mesa": um espaço onde posso colocar coisas em qualquer posição
    # e uma por cima da outra. Coloco os slots primeiro (ficam no fundo)
    # e as cartas depois (ficam na frente).
    stack = ft.Stack(controls=[*slots, *cards], width=1000, height=500)

    # Por fim, adiciono a mesa na página pra aparecer na tela.
    page.add(stack)


# Inicia o app. O assets_dir diz onde estão as imagens das cartas.
ft.run(main, assets_dir="assets")


#Raphela Luz

# =====================================================================
# COMO O CÓDIGO FUNCIONA (explicação geral)
# =====================================================================
#
# A ideia do programa é simples: eu tenho uma "mesa" com alguns espaços
# vazios (slots) e algumas cartas, e posso arrastar as cartas com o mouse
# para encaixar nesses espaços ou em cima de outras cartas.
#
# ---------------------------------------------------------------------
# 1. A MESA (Stack)
# ---------------------------------------------------------------------
# Tudo fica dentro de um Stack. Ele funciona como uma mesa onde cada
# coisa tem uma posição (top e left) e uma pode ficar por cima da outra.
# A ordem da lista de controles define quem aparece na frente: o último
# da lista fica por cima. Por isso coloco os slots primeiro (fundo) e
# as cartas depois (frente).
#
# ---------------------------------------------------------------------
# 2. OS ELEMENTOS
# ---------------------------------------------------------------------
# - Slot: um retângulo azul claro, só pra mostrar onde posso soltar
#   uma carta. Ele não se mexe.
# - Carta: uma imagem dentro de um GestureDetector. O GestureDetector é
#   quem "escuta" o mouse e avisa quando eu comecei a arrastar, quando
#   estou arrastando e quando soltei.
#
# --------------------------------------------SS-------------------------
# 3. O QUE ACONTECE QUANDO EU ARRASTO UMA CARTA
# ---------------------------------------------------------------------
# Passo 1 - Clico e começo a arrastar (start_drag):
#   Guardo a posição original da carta e a levo para o final da lista
#   do Stack, para ela ficar na frente de todo mundo enquanto me mexo.
#
# Passo 2 - Movo o mouse (drag):
#   A cada pequeno movimento, somo o quanto o mouse andou na posição da
#   carta. Assim ela acompanha o cursor. O max(0, ...) impede que ela
#   saia da área da mesa.
#
# Passo 3 - Solto o botão (drop):
#   Verifico se a carta está a menos de 20 pixels de algum alvo
#   (outra carta ou um slot).
#   - Se estiver perto de um alvo: a carta encaixa na posição dele. Se
#     o alvo for uma carta, ela fica 20 pixels mais abaixo, para eu
#     conseguir ver que tem uma carta embaixo.
#   - Se não estiver perto de nada: a carta volta para a posição que eu
#     tinha guardado no início.
#
# ---------------------------------------------------------------------
# 4. COMO COLOCO UMA CARTA EM CIMA DA OUTRA E TIRO DE LÁ
# ---------------------------------------------------------------------
# Para empilhar, basta soltar uma carta perto de outra: o drop trata as
# cartas como alvos também, e encaixa a carta em cima da outra.
# Para tirar, é só pegar a carta de cima e arrastar de novo. Como o
# start_drag já leva a carta para a frente, ela sempre fica visível
# durante o movimento e posso soltá-la em outro lugar.
#
# ---------------------------------------------------------------------
# 5. O "for ... else" DO DROP
# ---------------------------------------------------------------------
# O else do for só roda quando o loop termina sem nenhum break. Ou seja:
# se eu percorri todos os alvos e nenhum estava perto, entra no else e
# devolve a carta ao lugar original. Se achei um alvo, o break pula o
# else.
#
# ---------------------------------------------------------------------
# 6. RESUMINDO
# ---------------------------------------------------------------------
# Clico na carta -> ela vai pra frente (start_drag)
# Arrasto        -> ela acompanha o mouse (drag)
# Solto          -> encaixa no que estiver perto ou volta (drop)
#
# =====================================================================