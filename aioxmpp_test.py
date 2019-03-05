import asyncio, datetime, uuid, json, aioxmpp.xso, aioxmpp.utils, aioxmpp.node, aioxmpp.security_layer
import aioxmpp.structs, aioxmpp.stanza


FCM_SERVER_URL = "fcm-xmpp.googleapis.com"
FCM_SERVER_PORT = 5235
RECIPIENT = 'test'
FCM_API_KEY = 'test'
FCM_JID = 'test'


class FCMPayload(aioxmpp.xso.XSO):
    TAG = ("google:mobile:data", "gcm")
    text = aioxmpp.xso.Text(default=None)


async def main(jid, password, recipient):
    aioxmpp.stanza.Message.fcm_payload = aioxmpp.xso.Child([FCMPayload])

    client = aioxmpp.node.PresenceManagedClient(
        aioxmpp.structs.JID.fromstr(jid),
        aioxmpp.security_layer.tls_with_password_based_authentication(password),
        override_peer=[(FCM_SERVER_URL, FCM_SERVER_PORT, aioxmpp.connector.XMPPOverTLSConnector())],
    )

    payload = FCMPayload()
    payload.text = json.dumps({
        "message_id": str(uuid.uuid4()),
        "to": recipient,
        "data": {
            "test": "test"
        }
    })

    async with aioxmpp.node.UseConnected(client, timeout=datetime.timedelta(seconds=30)) as stream:
        msg = aioxmpp.stanza.Message(type_="normal", id_="")
        msg.fcm_payload = payload
        await stream.send_and_wait_for_sent(msg)


asyncio.get_event_loop().run_until_complete(main(FCM_JID, FCM_API_KEY, RECIPIENT))
