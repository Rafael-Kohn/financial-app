from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from app.models.card import Card
import sqlite3
from app.utils.notify import Notify

class AddCardScreen(Screen):
    banco = ObjectProperty(None)
    responsavel = ObjectProperty(None)
    apelido = ObjectProperty(None)
    ultimos_digitos = ObjectProperty(None)

    def salvar_cartao(self):

        banco = self.banco.text.strip()
        responsavel = self.responsavel.text.strip()
        apelido = self.apelido.text.strip()
        ultimos = self.ultimos_digitos.text.strip()

        # --- obrigatórios ---
        if not banco or not responsavel or not apelido or not ultimos:
            Notify.push("warning", "Preencha todos os campos")
            return

        # --- valida últimos dígitos ---
        if not (ultimos.isdigit() and len(ultimos) == 4):
            Notify.push("warning", "Últimos dígitos devem ser 4 números")
            return

        try:
            Card(
                banco=banco,
                responsavel=responsavel,
                apelido=apelido,
                ultimos_digitos=ultimos
            ).save()

            Notify.push("notice", "Cartão salvo com sucesso")

            # limpa
            self.banco.text = ""
            self.responsavel.text = ""
            self.apelido.text = ""
            self.ultimos_digitos.text = ""

            self.manager.current = "menu"

        except sqlite3.IntegrityError:
            Notify.push("warning", "Já existe um cartão com esses dados")

        except Exception as e:
            Notify.push("error", "Erro ao salvar cartão")
            print("ERRO:", e)
