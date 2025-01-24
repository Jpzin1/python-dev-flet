# Hashzap
# flet -> Constrói backend/frontend
# Botão de iniciar o chat
# Popup para entrar no chat 
# Quando entrar no chat: (aparece para todo mundo)
    # A mensagem que você entrou no chat
    # O campo e o botão de enviar mensagem
# A cada mensagem que você envia (aparece para todo mundo)
    # Nome: Texto da mensagem

import flet as ft

def main(pagina):
    texto = ft.Text("ZapZap do Sherek", color=ft.colors.GREEN_500)

    chat = ft.Column()

    nome_usuario = ft.TextField(label="Escreva seu nome")

    def enviar_mensagem_tunel(mensagem):
        tipo = mensagem["tipo"]
        if tipo == "mensagem":
            texto_mensagem = mensagem["texto"]
            usuario_mensagem = mensagem["usuario"]
            # Adicionar a mensagem no chat
            chat.controls.append(ft.Text(f"{usuario_mensagem}: {texto_mensagem}"))
        else:
             usuario_mensagem = mensagem["usuario"]
             chat.controls.append(ft.Text(f"{usuario_mensagem} entrou no chat!",
                                          size=12, italic=True, color=ft.colors.GREEN_500))
        pagina.update()

    # PUBSUB -> tunel de comunicação
    pagina.pubsub.subscribe(enviar_mensagem_tunel)

    def enviar_mensagem(evento):
        pagina.pubsub.send_all({"texto": campo_mensagem.value, "usuario": nome_usuario.value, "tipo": "mensagem"})
        # Limpar o campo de mensagem
        campo_mensagem.value = ""
        # Update da página
        pagina.update()
        
    campo_mensagem = ft.TextField(label="Digite uma mensagem", on_submit=enviar_mensagem)

    botao_enviar_mensagem = ft.ElevatedButton("Enviar", on_click=enviar_mensagem, color=ft.colors.GREEN_500)

    def entrar_popup(evento):
        pagina.pubsub.send_all({"usuario": nome_usuario.value, "tipo": "entrada"})
        # Adicionar o chat
        pagina.add(chat)
        # Fechar o popup
        popup.open=False
        # Remover o botão iniciar chat
        pagina.remove(botao_iniciar)
        # Remover o titulo
        pagina.remove(texto)
        # Adicionar o campo de mensagem do usuario
        # Adicionar o botao de enviar mensagem
        pagina.add(ft.Row(
            [campo_mensagem, botao_enviar_mensagem]
        ))
        # Update da página
        pagina.update()

    popup = ft.AlertDialog(
        open=False,
        modal=True,
        title=ft.Text("Bem vindo ao ZapZap do Sherek!", color=ft.colors.GREEN_500),
        content=nome_usuario,
        actions=[ft.ElevatedButton("Entrar", on_click=entrar_popup)],

    )

    def entrar_chat(evento):
        pagina.dialog = popup
        popup.open = True
        pagina.update()    

    botao_iniciar = ft.ElevatedButton("Iniciar chat", on_click=entrar_chat, color=ft.colors.GREEN_500)

    pagina.add(texto)
    pagina.add(botao_iniciar)

ft.app(target=main, view=ft.WEB_BROWSER, port=8000)



