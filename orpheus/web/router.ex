defmodule Orpheus.Router do
  use Phoenix.Router

  get "/", Orpheus.PageController, :index, as: :pages

end
