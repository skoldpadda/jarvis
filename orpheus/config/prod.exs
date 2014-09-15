use Mix.Config

# NOTE: To get SSL working, you will need to set:
#
#     ssl: true,
#     keyfile: System.get_env("SOME_APP_SSL_KEY_PATH"),
#     certfile: System.get_env("SOME_APP_SSL_CERT_PATH"),
#
# Where those two env variables point to a file on disk
# for the key and cert

config :phoenix, Orpheus.Router,
  port: System.get_env("PORT"),
  ssl: false,
  host: "example.com",
  cookies: true,
  session_key: "_orpheus_key",
  session_secret: "9(HC1B11&6B4KLBO0^+EV26_0YMXI$TKOP1_DE6GW911*_O1*8^W!PZ#4Z&IH7@_QL2C6!#1"

config :logger, :console,
  level: :info,
  metadata: [:request_id]

