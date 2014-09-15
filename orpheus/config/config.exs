# This file is responsible for configuring your application
use Mix.Config

# Note this file is loaded before any dependency and is restricted
# to this project. If another project depends on this project, this
# file won't be loaded nor affect the parent project.

config :phoenix, Orpheus.Router,
  port: System.get_env("PORT"),
  ssl: false,
  static_assets: true,
  cookies: true,
  session_key: "_orpheus_key",
  session_secret: "9(HC1B11&6B4KLBO0^+EV26_0YMXI$TKOP1_DE6GW911*_O1*8^W!PZ#4Z&IH7@_QL2C6!#1",
  catch_errors: true,
  debug_errors: false,
  error_controller: Orpheus.PageController

config :phoenix, :code_reloader,
  enabled: false

config :logger, :console,
  format: "$time $metadata[$level] $message\n",
  metadata: [:request_id]

# Import environment specific config. Note, this must remain at the bottom of
# this file to properly merge your previous config entries.
import_config "#{Mix.env}.exs"
