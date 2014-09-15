use Mix.Config

config :phoenix, Orpheus.Router,
  port: System.get_env("PORT") || 4001,
  ssl: false,
  cookies: true,
  session_key: "_orpheus_key",
  session_secret: "9(HC1B11&6B4KLBO0^+EV26_0YMXI$TKOP1_DE6GW911*_O1*8^W!PZ#4Z&IH7@_QL2C6!#1"

config :phoenix, :code_reloader,
  enabled: true

config :logger, :console,
  level: :debug


