import flet as ft
from flet import FilePicker, FilePickerResultEvent

def main(pagina):
    # Exibir imagem do Sherek
    img = ft.Image(
        src="sherek.png",
        width=200,
        height=200,
        fit=ft.ImageFit.CONTAIN,
    )

    pagina.add(img)

    # Texto de título
    texto = ft.Text("ZapZap do Sherek", color=ft.colors.GREEN_500)

    # Área do chat
    chat = ft.Column()

    # Campo para o nome do usuário
    nome_usuario = ft.TextField(label="Escreva seu nome")

    # Função para receber mensagens enviadas pelo túnel PubSub
    def enviar_mensagem_tunel(mensagem):
        tipo = mensagem["tipo"]
        if tipo == "mensagem":
            texto_mensagem = mensagem["texto"]
            usuario_mensagem = mensagem["usuario"]
            chat.controls.append(ft.Text(f"{usuario_mensagem}: {texto_mensagem}"))
        elif tipo == "arquivo":
            usuario_mensagem = mensagem["usuario"]
            arquivo_nome = mensagem["arquivo"]
            chat.controls.append(ft.Text(f"{usuario_mensagem} enviou um arquivo: {arquivo_nome}",
                                          italic=True, color=ft.colors.BLUE_500))
        else:  # Tipo "entrada"
            usuario_mensagem = mensagem["usuario"]
            chat.controls.append(ft.Text(f"{usuario_mensagem} entrou no chat!",
                                          size=12, italic=True, color=ft.colors.GREEN_500))
        pagina.update()

    # Inscrever-se no túnel de comunicação PubSub
    pagina.pubsub.subscribe(enviar_mensagem_tunel)

    # Função para enviar mensagem de texto
    def enviar_mensagem(evento):
        if campo_mensagem.value.strip():
            pagina.pubsub.send_all({"texto": campo_mensagem.value, "usuario": nome_usuario.value, "tipo": "mensagem"})
            campo_mensagem.value = ""  # Limpar o campo de mensagem
            pagina.update()

    # Campo de entrada para mensagem
    campo_mensagem = ft.TextField(label="Digite uma mensagem", on_submit=enviar_mensagem)

    # Botão de enviar mensagem
    botao_enviar_mensagem = ft.ElevatedButton("Enviar", on_click=enviar_mensagem, color=ft.colors.GREEN_500)

    # Função para enviar arquivo
    def enviar_arquivo(evento: FilePickerResultEvent):
        if evento.files:
            for f in evento.files:
                pagina.pubsub.send_all({"usuario": nome_usuario.value, "arquivo": f.name, "tipo": "arquivo"})

    # FilePicker para selecionar arquivos
    file_picker = FilePicker(on_result=enviar_arquivo)
    pagina.overlay.append(file_picker)

    # Botão de enviar arquivo
    botao_enviar_arquivo = ft.ElevatedButton(
        "Enviar arquivo",
        on_click=lambda _: file_picker.pick_files(allow_multiple=True),
        color=ft.colors.GREEN_500
    )

    # Função chamada ao entrar no popup
    def entrar_popup(evento):
        pagina.pubsub.send_all({"usuario": nome_usuario.value, "tipo": "entrada"})
        pagina.add(chat)  # Adicionar o chat à página
        popup.open = False  # Fechar o popup
        pagina.remove(botao_iniciar)  # Remover o botão de iniciar chat
        pagina.remove(texto)  # Remover o título
        # Adicionar campo de mensagem, botão de enviar mensagem e botão de enviar arquivo
        pagina.add(
            ft.Row(
                [campo_mensagem, botao_enviar_mensagem, botao_enviar_arquivo]
            )
        )
        pagina.update()

    # Popup para entrar no chat
    popup = ft.AlertDialog(
        open=False,
        modal=True,
        title=ft.Text("Bem vindo ao ZapZap do Sherek!", color=ft.colors.GREEN_500),
        content=nome_usuario,
        actions=[ft.ElevatedButton("Entrar", on_click=entrar_popup)],
    )

    # Função chamada ao clicar em "Iniciar chat"
    def entrar_chat(evento):
        pagina.dialog = popup  # Exibir o popup
        popup.open = True
        pagina.update()

    # Botão de iniciar chat
    botao_iniciar = ft.ElevatedButton("Iniciar chat", on_click=entrar_chat, color=ft.colors.GREEN_500)

    # Adicionar título e botão de iniciar chat à página
    pagina.add(texto)
    pagina.add(botao_iniciar)

ft.app(target=main, assets_dir="imagens", view=ft.WEB_BROWSER, port=8000)