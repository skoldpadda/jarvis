defmodule Orpheus.Router do
	use Phoenix.Router
	use Phoenix.Router.Socket, mount: "/kernel"

	get "/", Orpheus.PageController, :index, as: :pages

	channel "client", Orpheus.ClientChannel
end
