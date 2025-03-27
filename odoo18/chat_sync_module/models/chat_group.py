from odoo import models, fields, api
import requests

class ChatGroup(models.Model):
    _name = 'chat.group'
    _description = 'Grupo de Chat'

    name = fields.Char(string="Nombre del Grupo", required=True)
    user_ids = fields.Many2many('res.users', string="Usuarios")

    client_odoo_url = fields.Char(string="URL del Cliente", required=True)
    client_db = fields.Char(string="Base de Datos del Cliente", required=True)
    client_username = fields.Char(string="Usuario del Cliente", required=True)
    client_password = fields.Char(string="Contraseña del Cliente", required=True)
    client_version = fields.Char(string="Versión del Cliente", readonly=True)
    client_chat_id = fields.Char(string="ID del Grupo en Cliente", readonly=True)

    def _authenticate_client(self):
        for record in self:
            auth_data = {"db": record.client_db, "login": record.client_username, "password": record.client_password}
            response = requests.post(f"{record.client_odoo_url}/web/session/authenticate", json={"params": auth_data})

            if response.status_code == 200 and response.json().get("result"):
                session_id = response.cookies.get("session_id")
                headers = {"Cookie": f"session_id={session_id}"}

                version_response = requests.get(f"{record.client_odoo_url}/web/webclient/version_info", headers=headers)
                if version_response.status_code == 200:
                    record.client_version = version_response.json().get("server_version")

                return headers
        return None

    def create_client_chat_group(self):
        for record in self:
            headers = record._authenticate_client()
            if not headers:
                return False

            chat_data = {"jsonrpc": "2.0", "method": "call", "params": {
                "model": "mail.channel",
                "method": "create",
                "args": [{"name": "SAT", "channel_type": "group", "public": "private"}],
                "kwargs": {}
            }}

            response = requests.post(f"{record.client_odoo_url}/web/dataset/call_kw", json=chat_data, headers=headers)
            if response.status_code == 200:
                record.client_chat_id = response.json().get("result")

    def send_message_to_client_chat(self, message):
        for record in self:
            if not record.client_chat_id:
                return False

            headers = record._authenticate_client()
            if not headers:
                return False

            message_data = {"jsonrpc": "2.0", "method": "call", "params": {
                "model": "mail.message",
                "method": "create",
                "args": [{"body": message, "model": "mail.channel", "res_id": record.client_chat_id, "message_type": "comment"}],
                "kwargs": {}
            }}

            requests.post(f"{record.client_odoo_url}/web/dataset/call_kw", json=message_data, headers=headers)