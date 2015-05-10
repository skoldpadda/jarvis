defmodule Orpheus.ClientChannel do
	use Orpheus.Web, :channel

	# @TODO: Check out https://github.com/bbense/pluginator
	def join("client:" <> module, auth_msg, socket) do
		IO.puts "Attempting to join " <> module
		# Load module in cache
		module_path = "../modules/" <> module <> "/server"
		if File.exists?(module_path <> "/main.ex") do
			send self, %{after_join: module}
			{:ok, socket}
		else
			{:error, socket, :module_not_found}
		end
	end

	@doc """
	Swallow empty input. Ideally client implementations should handle this,
	but we do it here to reduce the chance of false positives.
	"""
	def handle_in(_, %{"data" => ""}, socket) do
		{:noreply, socket}
	end

	def handle_in(module, message, socket) do
		# @TODO This is terrible because it loads the thing every time
		#       We had to do this for now because Elixir's immutable state sucks
		module_path = "../modules/" <> module <> "/server"
		loaded_module = elem(Code.load_file("main.ex", module_path) |> List.first, 0)
		if loaded_module do
			push socket, "return_event", loaded_module.run(message)
		end
		{:noreply, socket}
	end

	def handle_info(%{:after_join => module}, socket) do
		push socket, "join", %{data: "Successfully joined " <> module}
		{:noreply, socket}
	end
end
